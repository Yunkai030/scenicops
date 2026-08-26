# P0 学习与验收清单

完成 P0 后，应当能不用背诵术语，自己解释并演示以下内容：

- 为什么系统 Python 与项目 `.venv` 必须分开。
- `pyproject.toml` 中运行依赖、可选依赖和开发依赖的区别。
- `src` 布局如何避免从仓库根目录误导入未安装代码。
- FastAPI Application Factory 与 Lifespan 分别解决什么问题。
- Liveness 为什么不访问外部依赖，Readiness 为什么需要检查依赖。
- Trace ID 如何从 HTTP 请求贯穿到日志，为什么要校验客户端传入值。
- Ruff、Mypy、Pytest、Coverage 各自拦截哪一类问题。
- ADR 为什么记录“为什么这样做”，而不只是重复代码结构。

## P0 自动验收

```bash
bash scripts/check.sh
```

必须满足：

1. Ruff 检查通过。
2. Ruff 格式检查通过。
3. Mypy strict 通过。
4. Pytest 全部通过。
5. 分支覆盖率不低于 90%。
6. `/health/live`、`/health/ready` 与 `/docs` 可访问。
