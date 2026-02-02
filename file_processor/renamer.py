import os
import re
from pathlib import Path
from typing import List, Tuple


class Renamer:
    """批量文件重命名器"""

    def __init__(self, dry_run: bool = False):
        """
        Args:
            dry_run: True=只预览不执行，False=真正重命名
        """
        self.dry_run = dry_run
        self.operations: List[Tuple[str, str]] = []  # (原路径, 新路径)

    def rename_with_pattern(self, directory: str, pattern: str, replacement: str) -> List[str]:
        r"""
        批量正则替换文件名
        示例：rename_with_pattern('./docs', r'report_(\d{4})', r'report_\1_final')
              report_2024.txt -> report_2024_final.txt
        """
        path = Path(directory)
        if not path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")

        self.operations = []  # 清空上次记录

        for file_path in path.iterdir():
            if file_path.is_file():
                new_name = re.sub(pattern, replacement, file_path.name)
                if new_name != file_path.name:
                    new_path = file_path.parent / new_name
                    self.operations.append((str(file_path), str(new_path)))

                    if not self.dry_run:
                        file_path.rename(new_path)

        return [f"{old} -> {new}" for old, new in self.operations]

    def add_sequence(self, directory: str, prefix: str = "", start: int = 1, digits: int = 3) -> List[str]:
        """
        给文件添加序号前缀
        示例：add_sequence('./pics', 'img_', start=1, digits=3)
              photo.jpg -> img_001_photo.jpg
        """
        path = Path(directory)
        if not path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")

        self.operations = []
        counter = start

        for file_path in sorted(path.iterdir()):
            if file_path.is_file():
                # 保留原扩展名
                suffix = file_path.suffix
                name_without_suffix = file_path.stem

                # 生成新名字：前缀 + 序号 + 原名字
                seq = str(counter).zfill(digits)
                new_name = f"{prefix}{seq}_{name_without_suffix}{suffix}"
                new_path = file_path.parent / new_name

                self.operations.append((str(file_path), str(new_path)))

                if not self.dry_run:
                    file_path.rename(new_path)

                counter += 1

        return [f"{old} -> {new}" for old, new in self.operations]

    def get_operations(self) -> List[Tuple[str, str]]:
        """获取上次操作记录"""
        return self.operations
