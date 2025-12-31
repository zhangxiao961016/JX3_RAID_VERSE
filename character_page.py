import streamlit as st
import database as db
import altair as alt


def show(u_info):
    """渲染角色管理与详情页"""
    st.markdown("## 👤 角色管理与详情")

    # ========================================================
    # 1. 角色维护 (添加/删除) - 核心修改区域
    # ========================================================
    with st.expander("🛠️ 维护角色列表 (添加/删除)", expanded=False):
        c1, c2 = st.columns([2, 1], gap="large")

        # --- 左侧：添加新角色 (增加非空判断) ---
        with c1:
            st.caption("新增角色")
            new_char = st.text_input("输入角色名", placeholder="例如：李忘生")
            new_sect = st.selectbox("门派",
                                    ["天策", "纯阳", "万花", "七秀", "五毒", "唐门", "明教", "丐帮", "苍云", "长歌",
                                     "霸刀", "蓬莱", "凌雪", "衍天", "药宗", "刀宗", "万灵", "其他"])

            if st.button("➕ 添加新角色", type="primary"):
                # 【修复】增加 .strip() 去除空格，并判断是否为空
                if not new_char or not new_char.strip():
                    st.error("⚠️ 角色名不能为空！")
                else:
                    if db.add_character_manual(u_info['id'], new_char.strip(), new_sect):
                        st.success(f"✅ 角色 {new_char} 创建成功")
                        st.rerun()
                    else:
                        st.error("❌ 该角色名已存在，请勿重复添加")

        # --- 右侧：删除角色 (逻辑重构：基于ID删除) ---
        with c2:
            st.caption("删除角色")
            all_chars = db.get_all_characters(u_info['id'])

            if not all_chars.empty:
                # 【修复】构建一个字典: { "显示文本": 角色ID }
                # 这样即使名字是空的，我们也能显示 "ID:5 - (空名) - 天策" 让用户选
                char_options = {}
                for _, row in all_chars.iterrows():
                    # 如果名字为空，显示为 (未命名)
                    display_name = row['name'] if row['name'] and row['name'].strip() else "(未命名/空)"
                    label = f"#{row['id']} {display_name} [{row['sect']}]"
                    char_options[label] = row['id']

                # 下拉框选择的是 Label (字符串)，我们通过字典拿到 ID
                selected_label = st.selectbox("选择要删除的角色", list(char_options.keys()))
                target_id = char_options[selected_label]

                # 删除按钮
                if st.button("🗑️ 确认删除", type="secondary"):
                    db.delete_character(target_id, u_info['id'])
                    st.toast(f"已删除角色：{selected_label}")
                    st.rerun()
            else:
                st.info("暂无角色可删")

    # ========================================================
    # 2. 角色选择器
    # ========================================================
    chars_df = db.get_all_characters(u_info['id'])

    # 过滤掉空名字的角色用于展示详情 (虽然数据库里可能还有，但详情页不想展示脏数据)
    valid_chars = chars_df[chars_df['name'].str.strip() != '']

    if valid_chars.empty:
        st.info("👉 请先在上方添加一个角色（名字不能为空）。")
        return

    st.markdown("### 👉 选择角色查看报表：")
    # 这里依然使用名字作为 key，因为展示看报表不需要 ID 那么麻烦
    selected_char = st.selectbox("选择角色", valid_chars['name'].tolist(), index=0, label_visibility="collapsed")

    st.markdown("---")

    # ========================================================
    # 3. 单角色详细统计 (保持不变)
    # ========================================================
    if selected_char:
        char_df = db.get_single_character_details(u_info['id'], selected_char)

        if char_df.empty:
            st.warning(f"角色【{selected_char}】暂无记账记录。")
        else:
            c_inc = char_df['salary'].sum()
            c_exp = char_df['expenditure'].sum()
            c_net = c_inc - c_exp

            c1, c2, c3, c4 = st.columns(4)
            # ... (上文的 指标卡 代码保持不变) ...
            c1.metric("💰 累计收入", f"{c_inc:,.0f}")
            c2.metric("💸 累计支出", f"-{c_exp:,.0f}")
            c3.metric("⚖️ 净收益", f"{c_net:,.0f}", delta_color="normal")
            c4.metric("⚔️ 打本次数", f"{len(char_df)}")

            # === 修复开始：柱状图代码 ===
            st.markdown("#### 📈 近期收支趋势")

            # 1. 数据预处理
            # 按日期分组求和
            trend_df = char_df.groupby('raid_date')[['salary', 'expenditure']].sum().reset_index()

            # 【关键修改 1】在此处重命名列名，把英文改成中文
            trend_df = trend_df.rename(columns={'salary': '收入', 'expenditure': '支出'})

            # 强制转字符串防止报错
            trend_df['raid_date'] = trend_df['raid_date'].astype(str)

            # 宽表转长表
            trend_df = trend_df.melt('raid_date', var_name='类型', value_name='金额')

            # 2. 绘制图表
            if not trend_df.empty:
                chart = alt.Chart(trend_df).mark_bar(
                    stroke='black',
                    strokeWidth=1,
                    cornerRadiusTopLeft=4,
                    cornerRadiusTopRight=4
                ).encode(
                    # X轴
                    x=alt.X('raid_date:O', axis=alt.Axis(
                        title=None,
                        labelColor='black',
                        labelFontWeight='bold',
                        labelAngle=-45,
                        tickColor='black',
                        domainColor='black'
                    )),

                    # Y轴
                    y=alt.Y('金额', axis=alt.Axis(
                        title='金额 (金)',
                        labelColor='black',
                        tickColor='black',
                        domainColor='black',
                        grid=False
                    )),

                    # 颜色映射 【关键修改 2】domain 里的名称也要改成中文
                    color=alt.Color('类型', scale=alt.Scale(
                        domain=['收入', '支出'],  # 这里对应上面的 rename
                        range=['#00b894', '#ff7675']  # 收入=绿，支出=红
                    ), legend=alt.Legend(title=None, orient="top")),

                    # 分组偏移
                    xOffset='类型:N',

                    # Tooltip (提示框)
                    tooltip=[
                        alt.Tooltip('raid_date', title='📅 日期'),
                        alt.Tooltip('类型', title='📊 类型'),
                        alt.Tooltip('金额', title='💰 金额', format=',.0f')
                    ]
                ).properties(
                    height=350
                ).configure_view(
                    stroke='transparent'
                )

                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("暂无足够的趋势数据。")

            st.markdown(f"#### 📜 {selected_char} 的账本流水")

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