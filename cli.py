#!/usr/bin/env python3
"""
命令行入口 - 让文件处理器可以在终端直接运行
"""
import argparse
import sys
from pathlib import Path

# 确保能找到 file_processor 包
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_processor.renamer import Renamer


def main():
    parser = argparse.ArgumentParser(
        description="智能文件批处理工具 - 支持正则重命名",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 预览模式（先看效果，不真的改）
  python cli.py ./我的文件 --pattern "report_(\\d+)" --replace "backup_\\1" --dry-run

  # 真正执行
  python cli.py ./我的文件 --pattern "old" --replace "new"
        """
    )

    parser.add_argument(
        "directory",
        help="要处理的目录路径"
    )
    parser.add_argument(
        "--pattern", "-p",
        required=True,
        help="正则匹配模式，如 'report_(\\\\d+)'"
    )
    parser.add_argument(
        "--replace", "-r",
        required=True,
        help="替换内容，如 'backup_\\\\1'"
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="预览模式：只显示会修改什么，不真的改"
    )

    args = parser.parse_args()

    # 验证目录存在
    target_dir = Path(args.directory)
    if not target_dir.exists():
        print(f"❌ 错误：目录不存在 {args.directory}", file=sys.stderr)
        sys.exit(1)

    if not target_dir.is_dir():
        print(f"❌ 错误：{args.directory} 不是目录", file=sys.stderr)
        sys.exit(1)

    # 执行重命名
    try:
        renamer = Renamer(dry_run=args.dry_run)
        result = renamer.rename_with_pattern(
            args.directory,
            args.pattern,
            args.replace
        )

        if not result:
            print("⚠️  没有匹配的文件需要处理")
            return

        # 显示结果
        mode = "【预览】" if args.dry_run else "【已执行】"
        print(f"\n{mode} 成功处理 {len(result)} 个文件：")
        for item in result:
            print(f"  {item}")

    except Exception as e:
        print(f"❌ 处理失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()