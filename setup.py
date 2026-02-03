from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="file-processor",
    version="1.0.0",
    author="tuntun114514",
    description="智能文件批处理工具，支持正则重命名、文件过滤与自动化测试",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuntun114514/python_unittest_learning",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "coverage>=7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "file-processor=cli:main",
        ],
    },
)