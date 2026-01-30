# python_unittest_learning

本项目用于系统学习 Python 标准库 unittest，涵盖测试用例编写、Fixture 使用、测试套件组织及 Mock 对象等核心知识点，适合单元测试初学者

## 当前进度

- [x] **Day 1: 项目初始化与配置管理**
  - 实现 `Config` 类：YAML 配置文件读取与验证
  - 掌握 `assertEqual`, `assertRaises` 断言
  - 掌握 `tempfile` 临时文件隔离测试
  - 编写 3 个测试用例，全部通过

## 快速开始

### 安装依赖
```bash
pip install pyyaml
``` 


## Day 2: 重构与踩坑记录（2026/1/30）

### 今日完成
- [x] **重构 test_config.py**：使用 `setUp`/`tearDown` 消除重复代码
  - 掌握 Fixture 生命周期：每个测试前自动创建资源，测试后自动清理
  - 代码行数减少 30%，可读性显著提升
  - 解决 Windows 文件锁定导致的 `PermissionError`

- [x] **学习 Mock 测试基础**：理解测试替身（Test Double）概念
  - 掌握 `@patch` 装饰器隔离外部依赖（文件系统）
  - 实现 `FileFilter` 文件过滤器（按大小过滤，无需创建真实大文件）

### 关键技术点

#### 1. setUp/tearDown 生命周期（Fixture）
setUp() → test_xxx() → tearDown() → [下一个测试循环]
- **执行保证**：无论测试通过与否，`tearDown` **一定会执行**（确保资源释放，类似 try-finally）
- **测试隔离**：每个测试独享全新的 `setUp` 实例，测试 A 的脏数据不会污染测试 B
- **DRY 原则**：把重复的临时文件创建/清理逻辑抽出，测试方法只关注业务断言

#### 2. Windows 文件锁定陷阱（WinError 32）
**问题现象**：
PermissionError: [WinError 32] 另一个程序正在使用此文件，进程无法访问

**根本原因**：Windows 对打开的文件句柄有严格锁定机制。`NamedTemporaryFile` 即使调用 `close()`，句柄释放也可能延迟几毫秒，导致 `tearDown` 中 `os.unlink()` 失败。

**解决方案**：
- 使用 `mkstemp()` 创建空文件后立即 `os.close(fd)`，只保留纯路径，不保持文件打开
- 各测试方法在需要写入时自行 `open()`，利用 `with` 语句确保关闭后再删除

**代码对比**：

**重构前（冗余，且 Windows 下会报错）**：
```python
def test_xxx(self):
    with tempfile.NamedTemporaryFile(...) as f:
        # 测试逻辑
        try:
            # ...
        finally:
            os.unlink(f.name)  # 每个测试都重复写，且句柄未完全释放

