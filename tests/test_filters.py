import unittest
from unittest.mock import patch
import sys
import os
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from file_processor.filters import FileFilter

class TestFileFilter(unittest.TestCase):
    def test_nonexistent_file(self):
        """测试：文件不存在时返回False"""
        filter = FileFilter()
        result = filter.is_valid("不存在的文件.txt")
        self.assertFalse(result)

    @patch('file_processor.filters.os.path.getsize')
    @patch.object(Path,'exists',return_value =True)
    def test_filter_by_size(self , mock_exists,mock_getsize):
        """
                测试：按大小过滤（使用Mock）

                场景：要求至少1KB，但文件只有500字节，应该返回False
                """
        mock_getsize.return_value = 500  # 假装文件大小为500字节

        filter = FileFilter(min_size=1024)  # 要求1024字节
        result = filter.is_valid("任意路径.txt")

        self.assertFalse(result)  # 500 < 1024，应该被过滤
        mock_getsize.assert_called_once_with("任意路径.txt")  # 验证确实调用了size检查

    @patch('file_processor.filters.os.path.getsize')
    @patch.object(Path, 'exists', return_value=True)
    def test_large_file_pass(self, mock_exists, mock_getsize):
        """测试：大文件通过过滤"""
        mock_getsize.return_value = 2048  # 2KB

        filter = FileFilter(min_size=1024)
        result = filter.is_valid("大文件.zip")

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()