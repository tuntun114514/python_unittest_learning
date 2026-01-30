import os
from pathlib import Path


class FileFilter:
    """文件过滤器：按条件筛选文件"""

    def __init__(self, min_size=None):
        self.min_size = min_size

    def is_valid(self, file_path):
        """检查文件是否符合条件"""
        path = Path(file_path)

        # 文件必须存在
        if not path.exists():
            return False

        # 检查大小限制
        if self.min_size is not None:
            file_size = os.path.getsize(file_path)
            if file_size < self.min_size:
                return False

        return True