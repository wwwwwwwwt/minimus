# Minimus API

一个基于 FastAPI 的迷你 API 项目，采用领域驱动设计（DDD）架构。

## 项目结构

```
api/
├── app/                    # 应用主目录
│   ├── application/        # 应用层（服务、错误处理）
│   ├── domain/             # 领域层（模型、仓储接口、服务接口）
│   ├── infrastructure/     # 基础设施层（存储、日志、外部服务）
│   ├── interfaces/         # 接口层（端点、中间件、模式）
│   └── main.py            # 应用入口
├── core/                   # 核心配置
├── test/                   # 测试目录
└── pyproject.toml         # 项目配置
```

## 技术栈

- Python 3.12+
- FastAPI
- Pydantic
- Uvicorn

## 安装

使用 uv 安装依赖：

```bash
uv sync
```

## 运行

```bash
uvicorn app.main:app --reload
```

## 开发

```bash
# 安装开发依赖
uv sync --dev

# 运行测试
pytest
```

## License

MIT
