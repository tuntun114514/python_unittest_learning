import unittest
import tempfile
import os
import sys
from pathlib import Path

# 获取项目根目录（pycharm兼容处理）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from file_processor.config import Config, ConfigError


class TestConfig(unittest.TestCase):

    def test_file_not_exists(self):
        """测试：配置文件不存在时抛出异常"""
        with self.assertRaises(ConfigError) as context:
            Config("不存在的文件.yaml")
        self.assertIn("不存在", str(context.exception))

    def test_missing_version(self):
        """测试：配置缺少version字段时抛出异常"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            f.write("name: test\n")  # 写了name，但没写version
            temp_path = f.name

        try:
            with self.assertRaises(ConfigError) as context:
                Config(temp_path)
            self.assertIn("version", str(context.exception))
        finally:
            os.unlink(temp_path)

    def test_valid_config(self):
        """测试：正常读取配置"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            f.write("version: 1.0\nname: my_processor\n")
            temp_path = f.name

        try:
            config = Config(temp_path)
            self.assertEqual(config.get_version(), 1.0)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()