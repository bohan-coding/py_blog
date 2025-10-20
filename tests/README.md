# 测试目录说明

本目录用于存放项目的各类测试代码，按照测试类型进行组织。

## 目录结构

- `unit/` - 单元测试
- `integration/` - 集成测试
- `utils/` - 测试工具和辅助函数

## 测试运行方式

### 单元测试
```bash
# 运行所有单元测试
python -m pytest tests/unit/

# 运行特定测试文件
python -m pytest tests/unit/test_weather.py
```

### 集成测试
```bash
# 运行所有集成测试
python -m pytest tests/integration/
```

## 测试代码规范

1. 测试文件命名：`test_*.py` 或 `*_test.py`
2. 测试函数命名：`test_*`
3. 每个测试函数应该只测试一个功能点
4. 测试代码应该独立，不依赖外部环境（除非是集成测试）
5. 测试结束后删除临时数据和文件

## 注意事项

- 测试代码仅供开发阶段使用
- 不要将测试代码提交到生产环境
- 定期清理过时的测试代码