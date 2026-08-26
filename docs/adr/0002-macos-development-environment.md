# ADR-0002：以 Apple Silicon Mac 作为主开发环境

- 状态：Accepted
- 日期：2026-08-26

## 背景

项目需要运行 PostgreSQL、Redis 和 Kafka 等 Linux 生态组件。开发者拥有 M1 Mac，并决定不在 Windows 上继续配置 Docker Hyper-V 权限。

项目源码位于同步目录时，仓库内虚拟环境会被 OneDrive 一并同步；Windows 和 macOS 的 Python 可执行文件及二进制依赖不能互相复用。

## 决策

1. M1 Mac 作为 ScenicOps 主开发设备。
2. 使用 Python 3.13 Universal2，在 Apple Silicon 上原生运行。
3. 使用 Apple Silicon 版 Docker Desktop，优先选择原生 `arm64` 或多架构容器镜像。
4. Python 虚拟环境默认放在 `$HOME/.virtualenvs/scenicops`，不放入仓库或 OneDrive。
5. 源码和依赖声明跨平台保留；PowerShell 脚本仅作为 Windows 备用入口。

## 结果

优点：避免 WSL/Hyper-V 权限问题，Linux 容器体验更直接，也避免跨系统同步虚拟环境。  
代价：需要在 Mac 上重新下载 Python 依赖和容器镜像，Windows 已安装的软件不再作为项目运行前提。

