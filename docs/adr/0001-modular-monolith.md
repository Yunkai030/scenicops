# ADR-0001：采用 Python 模块化单体与分进程运行

- 状态：Accepted
- 日期：2026-08-23

## 背景

项目需要展示后端领域建模、可靠事件、RAG 和 Agent 工程能力，但开发者是单人且需要在 1～3 个月内真正掌握实现。过早拆分微服务会增加部署、契约和分布式调试成本，也无法自然对应小型公司的团队规模。

## 决策

使用一个 Python 仓库和一套领域代码，按照 API、Application、Domain、Infrastructure、Agent、Workers 分模块。部署时运行三个后端进程：

1. FastAPI API。
2. Transactional Outbox Publisher。
3. Kafka Consumer。

模块间通过 Python 接口和 Pydantic 契约协作；数据库事务、状态机和权限规则只能由 Application 与 Domain 层维护。

## 结果

优点：本地开发和测试成本可控，规则只有一个实现来源，后台进程仍能独立重启和扩容。  
代价：模块边界需要通过 Code Review 和依赖规则主动维护；若未来拆服务，还需引入网络契约和独立部署流水线。

## 拆分触发条件

只有出现独立团队所有权、显著不同的扩缩容需求或部署节奏，并且已有指标证明模块化单体成为瓶颈时，才评估拆分服务。

