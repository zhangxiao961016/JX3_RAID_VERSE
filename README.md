# ⚔️ JX3 RAID VERSE | 剑网3团本账本

> **一款基于 Python Streamlit 的新野兽派（Neo-Brutalism）风格剑网3金团记账与数据分析工具。**
>
> *轻量级 • 移动端适配 • 多角色管理 • 欧皇检测器*

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-ff4b4b.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📖 项目简介

**JX3 RAID VERSE** 是一款专为《剑网3》玩家设计的现代化记账工具。不同于传统的 Excel 表格，它提供了一个**高颜值、响应式**的 Web 界面，支持手机端随时随地记录工资。

核心设计理念是 **"视觉化"** 与 **"多号管理"**。它采用高对比度的**新野兽派设计语言**（黑粗边框、硬阴影、撞色配色），支持多用户独立登录，并能针对账号下的不同角色（小号）分别统计工资、装备支出、净收入及特殊掉落（玄晶/大铁）。

## ✨ 核心功能

*   **🎨 新野兽派 UI**：独特的 CSS 注入，带来黑粗边框、硬阴影、高饱和度配色（粉/青/黄）的视觉体验。
*   **📱 移动端适配**：针对手机竖屏优化的布局，隐藏式侧边栏与自适应卡片。
*   **🔐 多用户系统**：支持注册/登录，数据基于 User ID 隔离，保障隐私。
*   **👥 角色管理**：
    *   **多号维护**：支持添加/删除多个游戏角色。
    *   **独立报表**：单独查看每个角色的收支详情与流水。
    *   **数据可视化**：集成 Altair 绘制收支对比柱状图与趋势折线图。
*   **💰 智能记账**：
    *   **净收入计算**：自动计算 `工资 - 支出`，盈亏一目了然。
    *   **沉浸式体验**：金砖图标 (🧱) 展示，支持千分位格式化。
    *   **欧皇记录**：专门的玄晶/大铁开关，统计表自动标记 💎。
*   **🧮 工具箱导航**：内置各门派计算器/配装器快捷入口卡片。
*   **💾 数据持久化**：基于 SQLite 本地存储，支持数据库表结构自动迁移。

## 📸 界面预览

https://jx3raidverse-long.streamlit.app/

账号：long

密码：123

## 🛠️ 技术栈

*   **前端/框架**: [Streamlit](https://streamlit.io/) (Python Web UI)
*   **数据处理**: Pandas
*   **可视化**: Altair (Vega-Lite)
*   **数据库**: SQLite3 (Python 原生支持)
*   **AI**: Gemini3 几乎全由AI生成

## 🚀 快速开始

### 1. 环境准备
确保你的电脑已安装 Python 3.8 或更高版本。

### 2. 获取代码
```bash
git clone https://github.com/zhangxiao961016/JX3_RAID_VERSE.git
```
### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 运行项目
```bash
streamlit run app.py
```

启动后，浏览器会自动打开 http://localhost:8501。

首次运行时，程序会自动在目录下生成 jx3_verse_v2.db 数据库文件。

## 📂 项目结构

本项目采用模块化结构设计，便于维护和扩展。
```text
jx3-raid-tool/
├── app.py              # 【主入口】路由分发、Session管理、页面调度
├── app_old.py          # 【旧版本】可忽略
├── database.py         # 【数据层】SQLite 连接、CRUD 操作、自动迁移逻辑
├── styles.py           # 【样式层】全局 CSS、Neo-Brutalism 风格定义
├── login_page.py       # 【视图】登录与注册页面
├── dashboard_page.py   # 【视图】总览看板 (记账入口、汇总统计)
├── character_page.py   # 【视图】角色详情 (角色管理、单号报表)
├── jx3_verse_v2.db     # 【数据库】自动生成的数据文件 (请勿直接删除)
└── README.md           # 项目说明文档
```

## ⚙️ 部署指南

### 推荐：云服务器 (VPS)

为了保证数据持久化（不丢失），建议部署在腾讯云/阿里云的轻量服务器上。

后台运行命令：
```bash
nohup streamlit run app.py --server.port 80 > log.txt 2>&1 &
```

### 注意事项

*   **不建议使用 Streamlit Community Cloud 免费托管，因为其容器休眠机制会导致 SQLite 数据库文件被重置，导致记账数据丢失。**

*   **如需重置数据库，直接删除目录下的 .db 文件并重启程序即可。**