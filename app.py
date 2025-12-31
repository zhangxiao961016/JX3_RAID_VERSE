import streamlit as st
import styles
import database as db

# 引入我们拆分好的页面
import login_page
import dashboard_page
import character_page

# 1. 基础配置 (必须第一行)
st.set_page_config(page_title="JX3 RAID VERSE", page_icon="⚔️", layout="wide")

# 2. 加载样式和数据库
st.markdown(styles.get_css(), unsafe_allow_html=True)
db.init_db()

# 3. Session 状态检查
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None

# ==========================================
# 核心路由控制
# ==========================================

if not st.session_state['logged_in']:
    # 如果没登录，显示登录页
    login_page.show()

else:
    # 如果已登录，显示侧边栏和主内容
    u_info = st.session_state['user_info']
    # ... (上文代码不变)

    # 侧边栏导航 (复刻截图风格)
    with st.sidebar:
        # 1. Logo 区域 (粉色方块)
        st.markdown("""
            <div class="sidebar-logo">
                <h1 style='font-style: italic; font-weight: 900; font-size: 36px; color: #d6336c; line-height: 1.1; margin: 0;'>
                    JX3<br>RAID<br>VERSE
                </h1>
            </div>
            """, unsafe_allow_html=True)

        # 2. 导航菜单 (使用 st.radio，样式已被 styles.py 魔改)
        # 给选项加上 Emoji 图标，模仿截图里的图标
        page = st.radio(
            "导航",
            ["⚙️ 总览看板", "👤 角色详情", "⚔️ 团本招募"],
            index=0,
            label_visibility="collapsed"  # 隐藏标题
        )

        # 占位符，把底部信息推到最下面 (如果项目多的话会自动顶下去，不多的话可以用空行)
        st.markdown("<br>" * 5, unsafe_allow_html=True)

        # 3. 底部用户信息栏 (仿截图：ID + 切换按钮)
        st.markdown(f"""
            <div class="user-footer">
                <div style="font-weight:bold; font-size:14px;">
                    ID: {u_info['name']}...<br>
                    <span style="color:#666; font-size:12px;">({u_info['role']})</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 切换/退出按钮 (用原生按钮，样式已改为白底黑框)
        if st.button("切换账号", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # 路由分发 (注意要匹配上面 radio 里的新名字)
    if "总览看板" in page:
        dashboard_page.show(u_info)

    elif "角色详情" in page:
        character_page.show(u_info)

    elif "团本招募" in page:
        st.info("🚧 团本招募功能开发中...")