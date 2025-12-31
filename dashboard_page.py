import streamlit as st
import database as db
import altair as alt
from datetime import date

# 定义通用图标
gold_icon = '<img src="https://img.icons8.com/color/48/gold-bars.png" style="width: 18px; vertical-align: text-bottom;" title="金">'


@st.dialog("📝 记一笔工资")
def show_add_modal(user_id):
    chars_df = db.get_all_characters(user_id)
    char_list = chars_df['name'].tolist() if not chars_df.empty else []

    with st.form("add_raid_form"):
        char_name = st.selectbox("🎮 角色选择", options=char_list)

        d_type = st.selectbox("⚔️ 副本名称", ["25人普通弓月城一之窟", "25人英雄弓月城一之窟", "挑战本", "10人周常", "其他"])
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


def show(u_info):
    """渲染总览看板"""
    # 欢迎卡片
    st.markdown(
        f"""<div class="neo-card bg-pink"><h2 style="margin:0; font-style:italic;">HELLO, {u_info['name']}!</h2><p style="margin:0; opacity: 0.9;">今天也是充满希望的一天，不去打个本吗？</p></div>""",
        unsafe_allow_html=True)

    # 顶部数据
    total_income, total_expenditure, total_special, total_count, df_all = db.get_user_stats(u_info['id'])
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
    st.markdown("### 📝 记账本")
    if st.button("➕ 记一笔工资 (点击弹窗)", type="primary", use_container_width=True):
        show_add_modal(u_info['id'])

    # 心法计算器链接 (可选，之前写的那个模块)
    # ==========================================
    st.markdown("### 🧮 门派计算器 (点击直达)")

    # 1. 定义心法数据 (模拟截图中的数据)
    # 提示：你可以把 url 换成真实的计算器链接，把 icon 换成剑三真实的图片链接
    # 这里我使用了在线图标作为示例
    flagship_xinfas = [
        {"name": "无方", "icon": "https://icon.jx3box.com/icon/15594.png", "url": "https://dps.btcsg.top/?xf=wf"},
        {"name": "周天功", "icon": "https://icon.jx3box.com/icon/22823.png", "url": "https://dps.btcsg.top/?xf=ztg"},
        {"name": "山海心决", "icon": "https://icon.jx3box.com/icon/19664.png", "url": "https://dps.btcsg.top/?xf=shxj"},
        {"name": "毒经", "icon": "https://icon.jx3box.com/icon/2766.png", "url": "https://dps.btcsg.top/?xf=dj"},
        {"name": "分山劲", "icon": "https://icon.jx3box.com/icon/6314.png", "url": "https://dps.btcsg.top/?xf=fsj"},
        {"name": "花间游", "icon": "https://icon.jx3box.com/icon/406.png", "url": "https://dps.btcsg.top/?xf=hjy"},
        {"name": "幽罗引", "icon": "https://icon.jx3box.com/icon/24896.png", "url": "https://dps.btcsg.top/?xf=xly"},
        {"name": "孤锋决", "icon": "https://icon.jx3box.com/icon/17633.png", "url": "https://dps.btcsg.top/?xf=gfj"},
        {"name": "凌海决", "icon": "https://icon.jx3box.com/icon/10709.png", "url": "https://dps.btcsg.top/?xf=lhj"},
        {"name": "太玄经", "icon": "https://icon.jx3box.com/icon/13894.png", "url": "https://dps.btcsg.top/?xf=txj"},
        {"name": "易筋经", "icon": "https://icon.jx3box.com/icon/425.png", "url": "https://dps.btcsg.top/?xf=yjj"},
        {"name": "北傲决", "icon": "https://icon.jx3box.com/icon/8424.png", "url": "https://dps.btcsg.top/?xf=baj"},
        {"name": "紫霞功", "icon": "https://icon.jx3box.com/icon/627.png", "url": "https://dps.btcsg.top/?xf=zxg"},
        {"name": "笑尘决", "icon": "https://icon.jx3box.com/icon/4610.png", "url": "https://dps.btcsg.top/?xf=xcj"},
        {"name": "天罗诡道", "icon": "https://icon.jx3box.com/icon/3184.png", "url": "https://dps.btcsg.top/?xf=tlgd"},
    ]

    mobile_xinfas = [
        {"name": "无方·悟", "icon": "https://icon.jx3box.com/icon/101355.png", "url": "https://dps.btcsg.top/?xf=w_wf"},
        {"name": "周天功·悟", "icon": "https://icon.jx3box.com/icon/102278.png",
         "url": "https://dps.btcsg.top/?xf=w_ztg"},
        {"name": "孤锋决·悟", "icon": "https://icon.jx3box.com/icon/101375.png",
         "url": "https://dps.btcsg.top/?xf=w_gfj"},
    ]


    # 2. 构建 HTML 网格布局
    # 样式：黑边框卡片，悬停变色，Grid 布局自动适应宽度
    def render_links_section(title, items):
        html = f"""
            <div style="margin-bottom: 20px;">
                <div style="font-weight: bold; margin-bottom: 10px; color: #555;">{title}</div>
                <div style="
                    display: grid; 
                    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); 
                    gap: 15px;
                ">
            """
        for item in items:
            html += f"""
                    <a href="{item['url']}" target="_blank" style="text-decoration: none; color: black;">
                        <div style="
                            display: flex; 
                            align-items: center; 
                            background-color: white; 
                            border: 2px solid black; 
                            border-radius: 8px; 
                            padding: 10px; 
                            box-shadow: 3px 3px 0px 0px black; 
                            transition: transform 0.1s;
                            cursor: pointer;
                        " onmouseover="this.style.transform='translate(-2px, -2px)'; this.style.boxShadow='5px 5px 0px 0px black';" 
                          onmouseout="this.style.transform='translate(0px, 0px)'; this.style.boxShadow='3px 3px 0px 0px black';">

                            <img src="{item['icon']}" style="width: 32px; height: 32px; margin-right: 10px;">
                            <span style="font-weight: bold; font-size: 14px;">{item['name']}</span>
                        </div>
                    </a>
                """
        html += "</div></div>"
        return html


    with st.container(border=True):
        st.html(render_links_section("旗舰版", flagship_xinfas))
        st.html(render_links_section("无界", mobile_xinfas))

    # (如果需要保留之前的计算器模块，请把那段代码粘贴到这里)

    # 详细报表
    st.markdown("---")
    st.markdown("### 📊 各角色小金库")
    char_stats_df = db.get_character_stats_by_user(u_info['id'])

    if not char_stats_df.empty:
        with st.container(height=450, border=False):
            melted_df = char_stats_df.melt(id_vars=['角色'], value_vars=['总收入', '总支出'], var_name='类型',
                                           value_name='金额')
            chart = alt.Chart(melted_df).mark_bar(stroke='black', strokeWidth=1).encode(
                y=alt.Y('角色', axis=alt.Axis(title=None)),
                x=alt.X('金额', axis=alt.Axis(title='金额')),
                color=alt.Color('类型', scale=alt.Scale(domain=['总收入', '总支出'], range=['#baff7d', '#ff7675'])),
                yOffset='类型', tooltip=['角色', '类型', '金额']
            ).properties(height=max(300, len(char_stats_df) * 80)).configure_view(stroke='transparent').configure_axis(
                grid=False, domainColor='black')
            st.altair_chart(chart, use_container_width=True)

        # 详细表格
        st.markdown("<br>", unsafe_allow_html=True)
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
            html_table += f"""<tr style="border-bottom: 1px solid #eee;"><td style="padding:10px; border-bottom:1px solid #eee;">{row['角色']}</td><td style="padding:10px; text-align:right; border-bottom:1px solid #eee; color:#2e7d32;">+{row['总收入']:,.0f} {gold_icon}</td><td style="padding:10px; text-align:right; border-bottom:1px solid #eee; color:#c62828;">-{row['总支出']:,.0f} {gold_icon}</td><td style="padding:10px; text-align:right; border-bottom:1px solid #eee; color:{color}; font-weight:bold;">{net:,.0f} {gold_icon}</td><td style="padding:10px; text-align:center; border-bottom:1px solid #eee;">{sp}</td><td style="padding:10px; text-align:center; border-bottom:1px solid #eee;">{row['打本次数']}</td></tr>"""

        # 合计行 (简写)
        t_inc, t_exp = char_stats_df['总收入'].sum(), char_stats_df['总支出'].sum()
        t_net = t_inc - t_exp
        html_table += f"""</tbody><tfoot style="font-weight:bold; color:black;"><tr><td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; border-top:3px solid black;">∑ 总计</td><td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; text-align:right; border-top:3px solid black;">+{t_inc:,.0f}</td><td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; text-align:right; border-top:3px solid black;">-{t_exp:,.0f}</td><td style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; padding:12px; text-align:right; border-top:3px solid black;">{t_net:,.0f}</td><td colspan="2" style="position:sticky; bottom:0; z-index:20; background-color:#ffeaa7; border-top:3px solid black;"></td></tr></tfoot></table></div>"""

        st.html(html_table)
    else:
        st.info("暂无数据")