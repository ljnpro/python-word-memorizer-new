# Word Memorizer (FastAPI + SQLite)

本项目是一个本地运行的背单词小工具，采用 FastAPI + SQLite，提供今日复习卡片、单词列表管理、CSV 导入/导出等功能，界面为暗色系卡片风格。

## 功能概览
- 间隔重复：根据熟悉度字段自动安排 `next_review_date`，支持“认识/不认识”操作与快捷键（J/Enter、F）。
- 今日复习：卡片式体验，显示进度、释义显示/隐藏、键盘操作。
- 单词管理：新增、编辑、删除、搜索、按创建时间/字母/熟悉度排序。
- CSV 导入/导出：支持字段 `word, meaning, phonetic, example, tags`，已存在的单词会被跳过并统计。
- 本地存储：所有数据保存在仓库根目录的 `wordmemorizer.db`。

## 快速开始（macOS / Linux / Windows）
1. 创建并激活虚拟环境（示例为 macOS/Linux）：
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   在 Windows PowerShell 下：
   ```powershell
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 启动应用（热重载开发模式）：
   ```bash
   uvicorn app.main:app --reload
   ```
4. 浏览器访问 [http://localhost:8000](http://localhost:8000) 即可使用。

## 项目结构
```
app/
  main.py          # FastAPI 入口，挂载路由、静态资源
  database.py      # SQLite 连接 & Session 管理
  models.py        # SQLAlchemy 模型（Word）
  schemas.py       # Pydantic 数据结构
  routers/
    review.py      # 今日复习、答题接口
    words.py       # 单词列表、增删改查、导入导出
  services/
    review.py      # 间隔重复算法与复习队列生成
    import_export.py # CSV 导入导出逻辑
  templates/       # Jinja2 模板（复习页、列表页、完成页）
  static/          # 样式文件
requirements.txt    # 项目依赖
wordmemorizer.db    # 运行后生成的本地数据库文件
```

## 使用提示
- 复习页面支持快捷键：`J` 或 `Enter` = 认识，`F` = 不认识；释义可点击“显示/隐藏”。
- CSV 导入：字段缺失会被跳过，已存在的单词也会跳过；导入结果在页面弹窗提示。
- 导出：点击单词列表页右上角“导出 CSV”可下载当前所有单词。

## 后续可扩展方向
- 生词本页与加练能力（基于熟悉度阈值）。
- 复习/学习统计与折线图展示。
- 支持设置每日新词上限、熟悉度阈值等个性化参数。
- 数据清空、备份与多端同步等增强功能。
