import streamlit as st
import database as db


def show():
    """渲染登录和注册页面"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            """<div class="neo-card bg-pink" style="text-align:center;"><h1>🔒 JX3 RAID LOGIN</h1><p>请出示你的江湖身份凭证</p></div>""",
            unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["登录", "注册"])

        with tab1:
            with st.form("login_form"):
                user = st.text_input("账号")
                pwd = st.text_input("密码", type="password")
                if st.form_submit_button("🚀 进入江湖"):
                    res = db.login_user(user, pwd)
                    if res:
                        st.session_state['logged_in'] = True
                        st.session_state['user_info'] = {'id': res[0][0], 'name': res[0][1], 'role': res[0][3]}
                        st.rerun()
                    else:
                        st.error("账号或密码错误")

        with tab2:
            with st.form("signup_form"):
                new_u = st.text_input("新账号")
                new_p = st.text_input("新密码", type="password")
                new_role = st.selectbox("身份", ["团长", "团员/老板"])
                if st.form_submit_button("📝 注册"):
                    if db.create_user(new_u, new_p, new_role):
                        st.success("注册成功！请返回登录。")
                    else:
                        st.error("账号已存在")