[![Tests](https://github.com/tuntun114514/python_unittest_learning/actions/workflows/python-test.yml/badge.svg)](https://github.com/tuntun114514/python_unittest_learning/actions)

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
```
**重构后（健壮，跨平台兼容）**：

```python 
def setUp(self):
    fd, self.temp_path = tempfile.mkstemp(suffix='.yaml')
    os.close(fd)  # 关键：立即释放 Windows 句柄

def tearDown(self):
    if os.path.exists(self.temp_path):
        os.unlink(self.temp_path)  # 现在可以安全删除

def test_xxx(self):
    with open(self.temp_path, 'w') as f:
        # 只写业务逻辑，不操心资源清理
```


### 3. Mock 测试实战

**为什么要 Mock？**  
测试"过滤大于 1GB 的文件"时，不需要真的创建 1GB 文件：
- 节省时间和磁盘空间
- 测试更稳定（不依赖真实文件系统）
- 可以模拟极端情况（如磁盘错误）

核心技巧：
```Python
@patch('file_processor.filters.os.path.getsize')
@patch.object(Path, 'exists', return_value=True)
def test_filter_by_size(self, mock_exists, mock_getsize):
  mock_getsize.return_value = 500  # 假装文件 500 字节
```    
###测试逻辑
**关键概念**：
- `@patch`：把目标函数替换为 Mock 对象
- `return_value`：设定假返回值  
- `assert_called_once_with`：验证函数确实被调用（确保逻辑覆盖）


#### 4. 测试覆盖情况

- `test_config.py`: 3/3 测试通过（Fixture 重构）
- `test_filters.py`: 3/3 测试通过（含 2 个 Mock 测试）
  - `test_nonexistent_file`：真实测试，验证文件不存在逻辑
  - `test_filter_by_size`：Mock 测试，验证小文件被过滤
  - `test_large_file_pass`：Mock 测试，验证大文件通过

**下一步计划（Day 3）**
- [ ] **GitHub Actions CI/CD**：配置自动测试流水线
- [ ] **测试覆盖率报告**：使用 coverage.py 生成可视化报告
- [ ] **批量重命名功能**：实现完整的文件批处理逻辑（集成测试）

##完成后的总测试
运行全部测试，确认 6/6 通过：
```
bash
python -m unittest discover -v
```
输出结果：
```
test_file_not_exists ... ok
test_missing_version ... ok
test_valid_config ... ok
test_filter_by_size ... ok
test_large_file_pass ... ok
test_nonexistent_file ... ok
----------------------------------------------------------------------
Ran 6 tests in 0.015s
```

## Day 3: CI/CD 自动化测试（2026/1/31）

### 今日完成
- [x] **配置 GitHub Actions**：实现自动化测试流水线
  - 每次 push/pull_request 自动触发测试
  - 使用 Ubuntu 环境 + Python 3.12
  - 6 个测试全部通过 ✅（10 秒内完成）

### 关键技术点

#### GitHub Actions 工作流配置
```yaml
# .github/workflows/python-test.yml
name: Python Tests
on: [push, pull_request]  # 触发条件：推送或提 PR 时自动运行
jobs:
  test:
    runs-on: ubuntu-latest  # 运行环境：云端 Linux 虚拟机
    steps:
      - uses: actions/checkout@v4      # 拉取代码
      - uses: actions/setup-python@v5  # 安装 Python 3.12
      - run: pip install pyyaml        # 安装依赖
      - run: python -m unittest discover -v  # 执行测试

OK
```

