import unittest
import tempfile
import os
from pathlib import Path
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from file_processor.renamer import Renamer


class TestRenamer(unittest.TestCase):
    """集成测试：使用真实临时目录操作真实文件"""

    def setUp(self):
        """创建临时目录和测试文件"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = self.temp_dir.name

        # 创建几个测试文件
        (Path(self.dir_path) / "report_2024.txt").write_text("content1")
        (Path(self.dir_path) / "report_2025.txt").write_text("content2")
        (Path(self.dir_path) / "data.csv").write_text("content3")

    def tearDown(self):
        """清理临时目录（自动删除所有文件）"""
        self.temp_dir.cleanup()

    def test_dry_run_mode(self):
        """测试：dry_run 模式只预览不修改"""
        renamer = Renamer(dry_run=True)

        # 执行重命名（应该不会真的改）
        result = renamer.rename_with_pattern(self.dir_path, r'report_(\d{4})', r'year_\1_report')

        # 验证返回了2条预览记录
        self.assertEqual(len(result), 2)

        # 验证包含正确的转换（检查子字符串，因为返回的是完整路径）
        # 注意：只需要检查 "旧文件名 -> 新文件名" 这部分出现在结果中
        self.assertTrue(
            any("report_2024.txt -> " in item and "year_2024_report.txt" in item for item in result),
            f"应该包含 report_2024 的转换，实际：{result}"
        )
        self.assertTrue(
            any("report_2025.txt -> " in item and "year_2025_report.txt" in item for item in result),
            f"应该包含 report_2025 的转换，实际：{result}"
        )

        # 关键：验证原文件还在（没被真的改）
        self.assertTrue((Path(self.dir_path) / "report_2024.txt").exists())
        self.assertFalse((Path(self.dir_path) / "year_2024_report.txt").exists())

    def test_real_rename(self):
        """测试：真正执行重命名"""
        renamer = Renamer(dry_run=False)

        # 执行
        renamer.rename_with_pattern(self.dir_path, r'report', r'document')

        # 验证旧文件消失，新文件出现
        self.assertFalse((Path(self.dir_path) / "report_2024.txt").exists())
        self.assertTrue((Path(self.dir_path) / "document_2024.txt").exists())

        # 验证内容还在
        content = (Path(self.dir_path) / "document_2024.txt").read_text()
        self.assertEqual(content, "content1")

    def test_add_sequence(self):
        """测试：添加序号功能"""
        renamer = Renamer(dry_run=False)

        result = renamer.add_sequence(self.dir_path, prefix="file_", digits=3)

        # 验证所有文件都加了序号（按字母排序）
        self.assertTrue((Path(self.dir_path) / "file_001_data.csv").exists())
        self.assertTrue((Path(self.dir_path) / "file_002_report_2024.txt").exists())
        self.assertTrue((Path(self.dir_path) / "file_003_report_2025.txt").exists())

    def test_invalid_directory(self):
        """测试：目录不存在时抛出异常"""
        renamer = Renamer()

        with self.assertRaises(FileNotFoundError):
            renamer.rename_with_pattern("不存在的目录", "pattern", "repl")


if __name__ == '__main__':
    unittest.main()