import streamlit as st
from datetime import date
import database as db
import styles
import altair as alt
import pandas as pd

# 1. 页面配置
st.set_page_config(page_title="JX3 RAID VERSE", page_icon="⚔️", layout="wide")
st.markdown(styles.get_css(), unsafe_allow_html=True)
db.init_db()

# Session 初始化
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_info' not in st.session_state: st.session_state['user_info'] = None

# 金砖图标定义
gold_icon = '<img src="https://img.icons8.com/color/48/gold-bars.png" style="width: 18px; vertical-align: text-bottom;" title="金">'


# ==========================================
# 模态框：记账 (供总览页使用)
# ==========================================
@st.dialog("📝 记一笔工资")
def show_add_modal(user_id):
    # 获取现有角色列表供选择，也可以手输
    chars_df = db.get_all_characters(user_id)
    char_list = chars_df['name'].tolist() if not chars_df.empty else []

    with st.form("add_raid_form"):
        # 支持选择或手输
        char_name = st.selectbox("🎮 角色选择 (或直接输入新名字)", options=char_list + ["手写输入..."])
        if char_name == "手写输入...":
            char_name = st.text_input("输入新角色名")

        d_type = st.selectbox("⚔️ 副本名称", ["25人一之窟", "冷龙峰", "普通一之窟", "10人周常", "其他"])
        c1, c2 = st.columns(2)
        d_sal = c1.number_input("💰 工资收入", step=1000, min_value=0)
        d_exp = c2.number_input("💸 装备支出", step=1000, min_value=0)
        c3, c4 = st.columns(2)
        d_date = c3.date_input("📅 日期", value=date.today())
        is_special = c4.toggle("💎 出玄晶了？")
        note = st.text_input("📝 备注")

        if st.form_submit_button("✅ 确认入账", use_container_width=True):
            final_name = char_name if char_name and char_name != "手写输入..." else "侠士"
            db.add_raid_record(user_id, d_date, d_type, d_sal, final_name, d_exp, is_special, note)
            st.success("记账成功！")
            st.rerun()


# ==========================================
# 页面 1: 总览看板 (原有的逻辑)
# ==========================================
def render_dashboard(u_info):
    total_income, total_expenditure, total_special, total_count, df_all = db.get_user_stats(u_info['id'])

    # 顶部卡片
    z_icon_lg = '<img src="https://img.icons8.com/color/48/gold-bars.png" style="width: 24px; vertical-align: bottom;">'
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""<div class="neo-card bg-yellow"><div class="card-title">💰 全部收入</div><div class="card-value">{total_income:,.0f} {z_icon_lg}</div></div>""",
            unsafe_allow_html=True)
    with c2:
        st.markdown(
            f"""<div class="neo-card" style="background-color:#ffcccc;"><div class="card-title">💸 全部支出</div><div class="card-value">-{total_expenditure:,.0f} {z_icon_lg}</div></div>""",
            unsafe_allow_html=True)
    with c3:
        st.markdown(
            f"""<div class="neo-card bg-yellow"><div class="card-title">💎 玄晶/大铁</div><div class="card-value">{total_special} <span style="font-size:16px">个</span></div></div>""",
            unsafe_allow_html=True)
    with c4:
        st.markdown(
            f"""<div class="neo-card bg-yellow"><div class="card-title">⚔️ 参与团本</div><div class="card-value">{total_count} <span style="font-size:16px">次</span></div></div>""",
            unsafe_allow_html=True)

    # 快捷操作
    st.markdown("### 📝 快捷操作")
    if st.button("➕ 记一笔工资 (点击弹窗)", type="primary", use_container_width=True):
        show_add_modal(u_info['id'])

    # 详细数据表
    st.markdown("---")
    st.markdown("### 📊 各角色小金库")
    char_stats_df = db.get_character_stats_by_user(u_info['id'])

    if not char_stats_df.empty:
        # 收支对比图
        with st.container(height=450, border=False):
            melted_df = char_stats_df.melt(id_vars=['角色'], value_vars=['总收入', '总支出'], var_name='类型',
                                           value_name='金额')
            chart = alt.Chart(melted_df).mark_bar(stroke='black', strokeWidth=1).encode(
                y=alt.Y('角色', axis=alt.Axis(title=None, labelFontWeight='bold')),
                x=alt.X('金额', axis=alt.Axis(title='金额')),
                color=alt.Color('类型', scale=alt.Scale(domain=['总收入', '总支出'], range=['#baff7d', '#ff7675'])),
                yOffset='类型', tooltip=['角色', '类型', alt.Tooltip('金额', format=',.0f')]
            ).properties(height=max(300, len(char_stats_df) * 80)).configure_view(stroke='transparent').configure_axis(
                grid=False, domainColor='black')
            st.altair_chart(chart, use_container_width=True)

        # 详细HTML表格
        st.markdown("<br>", unsafe_allow_html=True)
        t_inc, t_exp = char_stats_df['总收入'].sum(), char_stats_df['总支出'].sum()
        t_net = t_inc - t_exp

        html_table = f"""
        <div style="height: 500px; overflow-y: auto; border: 3px solid black; border-radius: 12px; box-shadow: 6px 6px 0px 0px black; background-color: white; font-family: 'Helvetica Neue'; font-size: 14px;">
            <table style="width: 100%; border-collapse: separate; border-spacing: 0;">
                <thead style="position: sticky; top: 0; z-index: 10; background-color: #00f0ff; color: black;">
                    <tr><th style="padding:12px; border-bottom:3px solid black;">🎮 角色</th><th style="padding:12px; text-align:right; border-bottom:3px solid black;">💰 收入</th><th style="padding:12px; text-align:right; border-bottom:3px solid black;">💸 支出</th><th style="padding:12px; text-align:right; border-bottom:3px solid black;">⚖️ 净收入</th><th style="padding:12px; text-align:center; border-bottom:3px solid black;">💎</th><th style="padding:12px; text-align:center; border-bottom:3px solid black;">⚔️</th></tr>
                </thead>
                <tbody>
        """
        for _, row in char_stats_df.iterrows():
            net = row['总收入'] - row['总支出']
            color = "#2e7d32" if net >= 0 else "#c62828"
            sp = "💎" * int(row['特殊掉落']) if row['特殊掉落'] > 0 else "-"
            html_table += f"""
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding:10px; border-bottom:1px solid #eee;">{row['角色']}</td>
                    <td style="padding:10px; text-align:right; border-bottom:1px solid #eee; color:#2e7d32;">+{row['总收入']:,.0f} {gold_icon}</td>
                    <td style="padding:10px; text-align:right; border-bottom:1px solid #eee; color:#c62828;">-{row['总支出']:,.0f} {gold_icon}</td>
                    <td style="padding:10px; text-align:right; border-bottom:1px solid #eee; color:{color}; font-weight:bold;">{net:,.0f} {gold_icon}</td>
                    <td style="padding:10px; text-align:center; border-bottom:1px solid #eee;">{sp}</td>
                    <td style="padding:10px; text-align:center; border-bottom:1px solid #eee;">{row['打本次数']}</td>
                </tr>
            """
        html_table += f"""
                </tbody>
                <tfoot style="font-weight:bold; color:black;">
                    <tr><td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; border-top:3px solid black;">∑ 总计</td>
                    <td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; text-align:right; border-top:3px solid black; color:#2e7d32;">+{t_inc:,.0f} {gold_icon}</td>
                    <td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; text-align:right; border-top:3px solid black; color:#c62828;">-{t_exp:,.0f} {gold_icon}</td>
                    <td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; text-align:right; border-top:3px solid black; color:{"#2e7d32" if t_net >= 0 else "#c62828"};">{t_net:,.0f} {gold_icon}</td>
                    <td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; text-align:center; border-top:3px solid black;">-</td>
                    <td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; text-align:center; border-top:3px solid black;">-</td></tr>
                </tfoot>
            </table></div>
        """
        st.html(html_table)
    else:
        st.info("暂无数据")


# ==========================================
# 页面 2: 角色管理与详情 (新功能)
# ==========================================
def render_character_page(u_info):
    st.markdown("## 👤 角色管理与详情")

    # 1. 角色维护 (添加/删除)
    with st.expander("🛠️ 维护角色列表 (添加/删除)", expanded=False):
        c1, c2 = st.columns([2, 1])
        with c1:
            new_char = st.text_input("新增角色名")
            new_sect = st.selectbox("门派",
                                    ["天策", "纯阳", "万花", "七秀", "五毒", "唐门", "明教", "丐帮", "苍云", "长歌",
                                     "霸刀", "蓬莱", "凌雪", "衍天", "药宗", "刀宗", "万灵", "其他"])
            if st.button("➕ 添加新角色"):
                if db.add_character_manual(u_info['id'], new_char, new_sect):
                    st.success(f"角色 {new_char} 创建成功"); st.rerun()
                else:
                    st.error("角色名已存在")

        with c2:
            all_chars = db.get_all_characters(u_info['id'])
            if not all_chars.empty:
                del_char = st.selectbox("删除角色 (仅删列表，不删账本)", all_chars['name'].tolist())
                # 找到该角色的ID
                char_id = all_chars[all_chars['name'] == del_char]['id'].values[0]
                if st.button("🗑️ 删除选定角色"):
                    db.delete_character(char_id, u_info['id'])
                    st.warning(f"已删除 {del_char}");
                    st.rerun()

    # 2. 角色选择器
    chars_df = db.get_all_characters(u_info['id'])
    if chars_df.empty:
        st.info("还没有角色，请在上方添加或在总览页记账时自动创建。")
        return

    # 使用 pills 或 radio 来选择角色
    st.markdown("### 👉 请选择要查看的角色：")
    # 获取角色列表，把 'name' 作为选项
    selected_char = st.selectbox("选择角色", chars_df['name'].tolist(), index=0)

    st.markdown("---")

    # 3. 单角色详细统计
    if selected_char:
        # 获取该角色的所有记录
        char_df = db.get_single_character_details(u_info['id'], selected_char)

        if char_df.empty:
            st.warning(f"角色【{selected_char}】暂无记账记录。")
        else:
            # --- 核心指标 ---
            c_inc = char_df['salary'].sum()
            c_exp = char_df['expenditure'].sum()
            c_net = c_inc - c_exp
            c_sp = char_df['is_special'].sum()

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💰 累计收入", f"{c_inc:,.0f}")
            c2.metric("💸 累计支出", f"-{c_exp:,.0f}")
            c3.metric("⚖️ 净收益", f"{c_net:,.0f}", delta_color="normal")
            c4.metric("⚔️ 打本次数", f"{len(char_df)}")

            # --- 收支趋势图 ---
            st.markdown("#### 📈 近期收支趋势")
            # 简单处理日期，按日期聚合
            trend_df = char_df.groupby('raid_date')[['salary', 'expenditure']].sum().reset_index()
            trend_df = trend_df.melt('raid_date', var_name='类型', value_name='金额')

            chart = alt.Chart(trend_df).mark_line(point=True).encode(
                x=alt.X('raid_date', title='日期'),
                y=alt.X('金额', title='金额 (金)'),
                color=alt.Color('类型', scale=alt.Scale(domain=['salary', 'expenditure'], range=['#baff7d', '#ff7675']),
                                legend=alt.Legend(title="类型")),
                tooltip=['raid_date', '类型', '金额']
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)

            # --- 详细流水记录 ---
            st.markdown(f"#### 📜 {selected_char} 的账本流水")

            # 使用原生表格展示详细记录
            def fmt(row):
                res = f"+{row['salary']:,}"
                if row['expenditure'] > 0: res += f" / -{row['expenditure']:,}"
                if row['is_special']: res += " 💎"
                return res

            char_df['收支详情'] = char_df.apply(fmt, axis=1)
            char_df['note'] = char_df['note'].fillna('-')

            st.dataframe(
                char_df[['raid_date', 'dungeon_type', '收支详情', 'note']],
                column_config={
                    "raid_date": "日期",
                    "dungeon_type": "副本",
                    "收支详情": "收 / 支",
                    "note": "备注"
                },
                use_container_width=True,
                hide_index=True
            )


# ==========================================
# 主程序入口
# ==========================================
if not st.session_state['logged_in']:
    # --- 登录注册部分 (保持不变) ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            """<div class="neo-card bg-pink" style="text-align:center;"><h1>🔒 JX3 RAID LOGIN</h1><p>请出示你的江湖身份凭证</p></div>""",
            unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["登录", "注册"])
        with tab1:
            with st.form("login_form"):
                user = st.text_input("账号");
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
                new_u = st.text_input("新账号");
                new_p = st.text_input("新密码", type="password");
                new_role = st.selectbox("身份", ["团长", "团员/老板"])
                if st.form_submit_button("📝 注册"):
                    if db.create_user(new_u, new_p, new_role):
                        st.success("注册成功");
                    else:
                        st.error("账号已存在")
else:
    # --- 登录后界面 ---
    u_info = st.session_state['user_info']

    # 侧边栏导航
    with st.sidebar:
        st.markdown(f"""
        <h1 style='font-style: italic; font-weight: 900; font-size: 40px; color: #d6336c; line-height: 1; margin-bottom: 20px;'>JX3<br>RAID<br>VERSE</h1>
        <div class="neo-card bg-white" style="padding:10px;"><b>ID:</b> {u_info['name']}<br><b>身份:</b> {u_info['role']}</div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        # 导航菜单
        page = st.radio("📍 导航菜单", ["📊 总览看板", "👤 角色详情"], index=0)

        st.markdown("---")
        if st.button("🚪 退出登录"):
            st.session_state['logged_in'] = False;
            st.rerun()

    # 路由分发
    if page == "📊 总览看板":
        # 欢迎语只在总览显示
        st.markdown(
            f"""<div class="neo-card bg-pink"><h2 style="margin:0; font-style:italic;">HELLO, {u_info['name']}!</h2><p style="margin:0; opacity: 0.9;">今天也是充满希望的一天，不去打个本吗？</p></div>""",
            unsafe_allow_html=True)
        render_dashboard(u_info)
    elif page == "👤 角色详情":
        render_character_page(u_info)