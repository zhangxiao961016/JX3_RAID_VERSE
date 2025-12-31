def get_css():
    return """
<style>
    /* 1. 全局配置 */
    .stApp { background-color: #f0f0f0; font-family: 'Helvetica Neue', sans-serif; }

    /* 核心修复：强制撑满屏幕 */
    /* 3. 针对底层数据属性 (最稳的选择器) /
    [data-testid="stBlockContainer"] {
        max-width: 100vw !important;
        width: 100vw !important;
        padding-left: 0.5rem !important; / 几乎贴边 */
        padding-right: 0.5rem !important;
    }

    /* ==========================================
       2. 侧边栏 (Sidebar) 风格复刻
       ========================================== */

    /* 侧边栏整体背景 - 改为干净的白色，不再是粉色 */
    section[data-testid="stSidebar"] {
        background-color: #ffffff; 
        border-right: 3px solid black;
    }

    /* 侧边栏 Logo 区域样式 (粉色方块) */
    .sidebar-logo {
        background-color: #fff0f5; /* 浅粉底色 */
        border: 3px solid black;
        box-shadow: 4px 4px 0px 0px black;
        padding: 20px;
        margin-bottom: 30px;
        border-radius: 0px; /* 直角风格 */
    }

    /* === 3. 导航菜单魔改 (st.radio) === */

    /* 第一步：隐藏原本丑陋的圆圈单选框 */
    [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* 第二步：设置每个选项的基础样式 (透明背景) */
    [data-testid="stRadio"] label {
        padding: 12px 20px !important;
        margin-bottom: 12px !important;
        border-radius: 10px !important;
        border: 2px solid transparent !important; /* 默认无边框 */
        transition: all 0.2s !important;
        cursor: pointer !important;
    }

    /* 鼠标悬停时：微微变灰 */
    [data-testid="stRadio"] label:hover {
        background-color: #f5f5f5 !important;
    }

    /* 第三步：【选中状态】样式 (青色背景 + 黑框 + 阴影) */
    /* 使用 :has(input:checked) 选中被激活的那个 label */
    [data-testid="stRadio"] label:has(input:checked) {
        background-color: #00f0ff !important; /* 核心青色 */
        border: 2px solid black !important;
        box-shadow: 4px 4px 0px 0px black !important;
        color: black !important;
        transform: translate(-2px, -2px); /* 微微浮起 */
    }

    /* 调整文字样式 */
    [data-testid="stRadio"] label p {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: black !important;
        margin: 0 !important;
    }

    /* === 4. 底部用户信息栏 === */
    .user-footer {
        border-top: 3px solid black;
        padding-top: 20px;
        margin-top: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* ==========================================
       5. 其他通用样式 (保持不变)
       ========================================== */
    header[data-testid="stHeader"] { background-color: transparent !important; z-index: 1; }
    div[data-testid="stDecoration"] { display: none; }

    /* 侧边栏按钮修复 */
    button[data-testid="stSidebarCollapsedControl"] {
        display: block !important; visibility: visible !important;
        background-color: #ff6bb0 !important; border: 3px solid black !important;
        width: 50px !important; height: 50px !important; margin-top: 10px !important;
        z-index: 999999 !important;
    }
    button[data-testid="stSidebarCollapsedControl"] svg { fill: black !important; }

    /* 按钮通用样式 */
    div.stButton > button {
        background-color: white !important; color: black !important;
        border: 2px solid black !important; box-shadow: 4px 4px 0px 0px black !important;
        font-weight: bold !important; transition: all 0.1s;
    }
    div.stButton > button:active { transform: translate(2px, 2px); box-shadow: none !important; }
    div.stButton > button[kind="primary"] {
        background-color: #baff7d !important; border: 3px solid black !important;
        font-size: 18px !important; height: 60px !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #a3e665 !important; transform: translate(-1px, -1px);
        box-shadow: 6px 6px 0px 0px black !important;
    }

    /* 卡片与表格 */
    .neo-card {
        border: 3px solid black; box-shadow: 6px 6px 0px 0px black;
        border-radius: 12px; padding: 20px; margin-bottom: 20px; color: black;
    }
    .bg-pink { background-color: #ff6bb0; color: white; }
    .bg-yellow { background-color: #ffeaa7; }
    .bg-green { background-color: #baff7d; }
    .bg-white { background-color: white; }
    .card-title { font-size: 14px; font-weight: bold; }
    .card-value { font-size: 36px; font-weight: 900; text-align: right; }
    div[data-baseweb="input"] { border: 2px solid black !important; border-radius: 8px !important; }
</style>
"""