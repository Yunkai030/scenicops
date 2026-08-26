# ScenicOps

ScenicOps 是面向小型景区电动代步车租赁业务的内部运营与故障协同系统。项目采用“确定性业务底座先于 AI Agent”的实施顺序，所有演示业务数据均由脚本合成。

## 当前阶段

P0 工程地基：Python 工程结构、配置、日志、Trace ID、健康检查、测试和质量门禁。

当前还没有实现车辆、订单、Kafka 或 Agent 业务，不应把目录占位当成功能完成。

## 架构原则

- 一个 Python 模块化单体仓库。
- FastAPI API、Outbox Publisher、Kafka Consumer 分进程运行。
- PostgreSQL 是业务真相源，Redis 只保存热点与最新状态。
- LLM 只能调用类型化工具，不能直接访问数据库或自由执行 SQL。
- 写操作经过人工审批，并由应用服务进行权限、状态机和幂等校验。

## macOS 快速开始（主开发环境）

在 M1 Mac 安装 Python 3.13 后，进入本目录执行：

```bash
bash scripts/bootstrap.sh
bash scripts/check.sh
```

启动 API：

```bash
bash scripts/run-api.sh
```

浏览器访问：

- Swagger：<http://127.0.0.1:8000/docs>
- 存活检查：<http://127.0.0.1:8000/health/live>
- 就绪检查：<http://127.0.0.1:8000/health/ready>

## 质量检查

```bash
bash scripts/check.sh
```

该命令依次执行 Ruff 静态检查、格式检查、Mypy 严格类型检查和 Pytest。任何一步失败都不算验收通过。

默认虚拟环境位于 `$HOME/.virtualenvs/scenicops`，不放在 OneDrive 或仓库目录中。这样 Windows 与 macOS 不会同步并覆盖彼此不兼容的虚拟环境。可以通过 `SCENICOPS_VENV` 环境变量自定义位置。

Windows PowerShell 脚本仍保留在 `scripts/*.ps1`，仅作为备用开发入口。

## 目录说明

```text
src/scenicops/
├─ api/             HTTP 路由、DTO、鉴权与错误处理
├─ application/     用例编排、事务边界与 Agent Tool 门面
├─ domain/          实体、状态机、业务不变量与领域事件
├─ infrastructure/  PostgreSQL、Redis、Kafka 与模型适配器
├─ agent/           LangGraph、RAG、工具与审批流程
├─ core/            配置、日志、Trace 等跨模块基础设施
└─ workers/         Outbox Publisher 与 Kafka Consumer 入口
```

架构决定记录在 [`docs/adr`](docs/adr/)；个人学习验收记录在 [`docs/learning`](docs/learning/)。
