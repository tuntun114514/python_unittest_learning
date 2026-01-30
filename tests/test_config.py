import unittest
import tempfile
import os
import sys
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from file_processor.config import Config, ConfigError


class TestConfig(unittest.TestCase):

    def setUp(self):
        """创建临时文件路径（不保持打开，避免Windows句柄问题）"""
        # mkstemp 创建文件后立即关闭句柄，只保留路径
        fd, self.temp_path = tempfile.mkstemp(suffix='.yaml', text=True)
        os.close(fd)  # 立即关闭！这是关键

    def tearDown(self):
        """删除临时文件"""
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)

    def test_file_not_exists(self):
        """测试：配置文件不存在时抛出异常"""
        # 删除刚才创建的临时文件，让它真的不存在
        os.unlink(self.temp_path)

        with self.assertRaises(ConfigError) as context:
            Config(self.temp_path)
        self.assertIn("不存在", str(context.exception))

    def test_missing_version(self):
        """测试：配置缺少version字段时抛出异常"""
        # 需要自己打开写入（因为setUp没保持打开）
        with open(self.temp_path, 'w', encoding='utf-8') as f:
            f.write("name: test\n")

        with self.assertRaises(ConfigError) as context:
            Config(self.temp_path)
        self.assertIn("version", str(context.exception))

    def test_valid_config(self):
        """测试：正常读取配置"""
        with open(self.temp_path, 'w', encoding='utf-8') as f:
            f.write("version: 1.0\nname: processor\n")

        config = Config(self.temp_path)
        self.assertEqual(config.get_version(), 1.0)


if __name__ == '__main__':
    unittest.main()