import streamlit as st  # thư viện tạo web app
import pandas as pd     # xử lý dữ liệu dạng bảng
import plotly.express as px  # vẽ biểu đồ nhanh
import plotly.graph_objects as go  # vẽ biểu đồ nâng cao
from datetime import datetime, timedelta  # xử lý thời gian
import time as t_module  # dùng để làm timer
import os  # làm việc với file

st.set_page_config(page_title="Life Through Numbers", layout="wide", page_icon="💎")

def apply_custom_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=JetBrains+Mono:wght@500;700&display=swap');
        
        .stApp { background: #0b0f1a; color: #e2e8f0; font-family: 'Plus Jakarta Sans', sans-serif; }
        
        /* Glassmorphism Card */
        .glass-card {
            background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 25px; margin-bottom: 20px;
        }
        
        /* Timer Display */
        .timer-display {
            font-family: 'JetBrains Mono', monospace; font-size: 85px !important;
            font-weight: 800; color: #00f2fe; text-align: center;
            text-shadow: 0 0 30px rgba(0, 242, 254, 0.5); line-height: 1.2;
        }
        
        /* Skill Chip (Accumulation) */
        .skill-chip {
            background: rgba(0, 242, 254, 0.1); border-left: 4px solid #00f2fe;
            padding: 15px; border-radius: 12px; margin-bottom: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        /* Level Badge */
        .level-badge {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            padding: 20px; border-radius: 20px; text-align: center; color: white;
        }

        /* Marquee */
        .marquee-box {
            background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 10px; border-radius: 12px; overflow: hidden; margin-bottom: 25px;
        }
        .marquee-text {
            display: inline-block; white-space: nowrap;
            animation: marquee 40s linear infinite; font-weight: 600; color: #38bdf8;
        }
        @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
        </style>
    """, unsafe_allow_html=True)

apply_custom_theme()

DB_FILES = {
    "study": "ultimate_study_db.csv",
    "knowledge": "ultimate_knowledge_db.csv",
    "tasks": "ultimate_tasks_db.csv"
}

def init_db():
    for key, path in DB_FILES.items():
        if not os.path.exists(path) or os.stat(path).st_size == 0:
            if key == "study":
                pd.DataFrame(columns=["timestamp", "date", "minutes", "skills"]).to_csv(path, index=False)
            elif key == "knowledge":
                pd.DataFrame(columns=["date", "topic", "content", "category"]).to_csv(path, index=False)
            elif key == "tasks":
                pd.DataFrame(columns=["date", "task", "status", "priority"]).to_csv(path, index=False)

init_db()

def load_db(key):
    try:
        df = pd.read_csv(DB_FILES[key])
        if "date" in df.columns and not df.empty:
            df["date"] = pd.to_datetime(df["date"]).dt.date
        return df
    except: return pd.DataFrame()

def save_study_session(minutes, skills_list):
    df = load_db("study")
    skills_str = ", ".join(skills_list) if skills_list else "General"
    new_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().date(),
        "minutes": round(minutes, 2),
        "skills": skills_str
    }
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DB_FILES["study"], index=False)


def get_skill_totals():
    df = load_db("study")
    if df.empty: return {}
    # Phân rã kỹ năng và tính tổng phút
    df_exp = df.copy()
    df_exp['skills'] = df_exp['skills'].str.split(', ')
    df_exp = df_exp.explode('skills')
    totals = df_exp.groupby('skills')['minutes'].sum() / 60 # Đổi sang giờ
    return totals.to_dict()

def get_level_info(total_min):
    xp = int(total_min * 12)
    level = int((xp / 600)**0.6) + 1
    progress = (xp % 1200) / 1200
    return level, xp, min(max(float(progress), 0.0), 1.0)


with st.sidebar:
    st.markdown("<h1 style='color:#00f2fe; text-align:center'>💎 GLOW INFINITY</h1>", unsafe_allow_html=True)
    
    df_s_sidebar = load_db("study")
    total_m = df_s_sidebar["minutes"].sum() if not df_s_sidebar.empty else 0
    lv, total_xp, prog_val = get_level_info(total_m)
    
    st.markdown(f"""
        <div class="level-badge">
            <small>CURRENT RANK</small>
            <h2 style="margin:0">Level {lv}</h2>
            <div style="font-size:14px">{total_xp:,} XP</div>
        </div>
    """, unsafe_allow_html=True)
    st.progress(prog_val)
    
    st.divider()
    page = st.radio("ĐIỀU HƯỚNG", ["🏠 Dashboard", "⚡ Focus Hub", "🧠 Kho Kiến Thức", "📋 Nhiệm Vụ", "📈 Phân Tích"], label_visibility="collapsed")
    
    st.divider()
    with st.expander("🎵 Nhạc Tập Trung"):
        choice = st.selectbox("Chọn dòng nhạc:", ["None", "Lofi Jazz", "Deep Work", "Rain Sound"])
        if choice != "None":
            urls = {"Lofi Jazz": "https://www.youtube.com/watch?v=jfKfPfyJRdk", "Deep Work": "https://www.youtube.com/watch?v=17X2fMv_r4A", "Rain Sound": "https://www.youtube.com/watch?v=q76bEOTuyyM"}
            st.video(urls[choice])

    if st.button("🗑️ Xóa Toàn Bộ Dữ Liệu"):
        for p in DB_FILES.values(): 
            if os.path.exists(p): os.remove(p)
        st.rerun()

# Marquee Quotes
st.markdown('<div class="marquee-box"><div class="marquee-text">🚀 Kỷ luật là tự do • 💎 Áp lực tạo nên kim cương • 📚 Học tập là hành trình cả đời • 🔥 Thành công là tổng của những nỗ lực nhỏ.</div></div>', unsafe_allow_html=True)


if page == "🏠 Dashboard":
    st.title("Tổng quan năng suất")
    
    c1, c2, c3 = st.columns(3)
    today = datetime.now().date()
    today_m = df_s_sidebar[df_s_sidebar['date'] == today]['minutes'].sum() if not df_s_sidebar.empty else 0
    c1.metric("Hôm nay", f"{today_m:.0f} m", "Active")
    
    streak = 0
    if not df_s_sidebar.empty:
        dates = sorted(df_s_sidebar['date'].unique(), reverse=True)
        check = today
        for d in dates:
            if d == check: streak += 1; check -= timedelta(days=1)
            else: break
    c2.metric("Streak", f"{streak} Ngày", "🔥")
    c3.metric("XP Hệ thống", f"{total_xp:,}", "XP")

    st.divider()
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("⚖️ Quản Lý Thời Gian 24h")
        with st.container(border=True):
            s_h = st.slider("Học tập (Giờ)", 0, 15, 6)
            sl_h = st.slider("Ngủ (Giờ)", 0, 12, 😎
            f_h = st.slider("Giải trí (Giờ)", 0, 10, 2)
            fig_pie = go.Figure(data=[go.Pie(labels=['Học', 'Ngủ', 'Chơi', 'Khác'], values=[s_h, sl_h, f_h, 24-s_h-sl_h-f_h], hole=.5, marker_colors=['#00f2fe', '#6366f1', '#fb7185', '#1e293b'])])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=350, margin=dict(t=0, b=0))
            st.plotly_chart(fig_pie, use_container_width=True)
    with col_r:
        st.subheader("💡 AI Insights")
        if sl_h < 6: st.error("⚠️ Bạn đang thiếu ngủ! Hãy chú ý sức khỏe.")
        elif s_h > 10: st.warning("⚠️ Học quá nhiều dễ gây Burnout.")
        else: st.success("✅ Tỷ lệ vàng! Hãy duy trì phong độ.")

elif page == "⚡ Focus Hub":
    st.markdown("<h2 style='text-align:center'>⚡ PHIÊN TẬP TRUNG</h2>", unsafe_allow_html=True)
    
    if 't_on' not in st.session_state: st.session_state.t_on = False
    if 't_elapsed' not in st.session_state: st.session_state.t_elapsed = 0
    if 't_start' not in st.session_state: st.session_state.t_start = None

    selected_skills = st.multiselect("Nội dung học (Chọn trước khi Start):", ["Reading", "Listening", "Writing", "Speaking", "Vocabulary", "Grammar", "Coding", "Math", "Science"])
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    @st.fragment(run_every=1.0)
    def update_timer():
        if st.session_state.t_on:
            st.session_state.t_elapsed = t_module.time() - st.session_state.t_start
        secs = int(st.session_state.t_elapsed)
        st.markdown(f'<div class="timer-display">{timedelta(seconds=secs)}</div>', unsafe_allow_html=True)
    
    update_timer()
    
    c1, c2, c3 = st.columns(3)
    if not st.session_state.t_on:
        if c1.button("▶ START", use_container_width=True, type="primary"):
            st.session_state.t_on = True
            st.session_state.t_start = t_module.time() - st.session_state.t_elapsed
            st.rerun()
    else:
        if c1.button("⏸ PAUSE", use_container_width=True):
            st.session_state.t_on = False
            st.rerun()
    
    if c2.button("⏹ RESET", use_container_width=True):
        st.session_state.t_on = False
        st.session_state.t_elapsed = 0
        st.rerun()
            
    if c3.button("💾 SAVE SESSION", use_container_width=True):
        if st.session_state.t_elapsed > 10:
            save_study_session(st.session_state.t_elapsed / 60, selected_skills)
            st.session_state.t_on = False
            st.session_state.t_elapsed = 0
            st.balloons()
            st.success("Đã ghi nhận dữ liệu!")
            t_module.sleep(1)
            st.rerun()
        else: st.warning("Thời gian quá ngắn!")
    st.markdown('</div>', unsafe_allow_html=True)

    # PHẦN QUAN TRỌNG: TÍCH LŨY KỸ NĂNG (SKILL ACCUMULATION)
    st.divider()
    st.subheader("📊 TỔNG TÍCH LŨY THEO KỸ NĂNG (Tất cả phiên học)")
    
    skill_totals = get_skill_totals()
    if skill_totals:
        cols = st.columns(4)
        for i, (sk, hrs) in enumerate(skill_totals.items()):
            with cols[i % 4]:
                st.markdown(f"""
                    <div class="skill-chip">
                        <small style="color:#94a3b8">{sk.upper()}</small><br>
                        <b style="font-size:24px; color:#00f2fe">{hrs:.2f}</b> <small>Giờ</small>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Chưa có dữ liệu tích lũy.")


elif page == "🧠 Kho Kiến Thức":
    st.title("🧠 Kho tri thức Flashcards")
    t_add, t_rev = st.tabs(["✍️ Thêm kiến thức", "🗂️ Ôn tập"])
    
    with t_add:
        with st.form("k_f"):
            top = st.text_input("Chủ đề:"); cont = st.text_area("Giải nghĩa:"); cat = st.selectbox("Loại:", ["Vocabulary", "Grammar", "Note"])
            if st.form_submit_button("Lưu"):
                df_k = load_db("knowledge")
                new_k = pd.DataFrame([{"date": datetime.now().date(), "topic": top, "content": cont, "category": cat}])
                pd.concat([df_k, new_k]).to_csv(DB_FILES["knowledge"], index=False)
                st.success("Đã lưu!")
                
    with t_rev:
        df_k = load_db("knowledge")
        if not df_k.empty:
            if 'f_idx' not in st.session_state: st.session_state.f_idx = 0
            row = df_k.iloc[st.session_state.f_idx % len(df_k)]
            with st.container(border=True):
                st.markdown(f"<h1 style='text-align:center; color:#00f2fe'>{row['topic']}</h1>", unsafe_allow_html=True)
                with st.expander("Xem giải nghĩa"): st.write(row['content'])
            if st.button("Tiếp theo ➡️"): st.session_state.f_idx += 1; st.rerun()
        else: st.info("Trống.")


elif page == "📋 Nhiệm Vụ":
    st.title("📋 Checklist Kỷ Luật")
    with st.form("tk_f"):
        tk_n = st.text_input("Việc cần làm:"); tk_p = st.selectbox("Ưu tiên:", ["Cao", "Thấp"])
        if st.form_submit_button("Thêm Task"):
            df_t = load_db("tasks")
            new_t = pd.DataFrame([{"date": datetime.now().date(), "task": tk_n, "status": "Pending", "priority": tk_p}])
            pd.concat([df_t, new_t]).to_csv(DB_FILES["tasks"], index=False); st.rerun()
            
    df_t = load_db("tasks")
    if not df_t.empty:
        for idx, r in df_t.iterrows():
            c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
            is_done = c1.checkbox("", value=(r['status']=="Done"), key=f"tk_{idx}")
            if is_done != (r['status']=="Done"):
                df_t.at[idx, 'status'] = "Done" if is_done else "Pending"
                df_t.to_csv(DB_FILES["tasks"], index=False); st.rerun()
            c2.write(f"{r['task']} ({r['priority']})")
            if c3.button("🗑️", key=f"del_{idx}"):
                df_t.drop(idx).to_csv(DB_FILES["tasks"], index=False); st.rerun()

elif page == "📈 Phân Tích":
    st.title("📈 Phân tích học tập chuyên sâu")
    df_study = load_db("study")
    if not df_study.empty:
        st.subheader("📅 Tiến độ theo ngày (Phút)")
        daily = df_study.groupby('date')['minutes'].sum().reset_index()
        st.plotly_chart(px.bar(daily, x='date', y='minutes', color_discrete_sequence=['#00f2fe']), use_container_width=True)
        
        c_a, c_b = st.columns(2)
        df_exp = df_study.assign(skills=df_study['skills'].str.split(', ')).explode('skills')
        with c_a:
            st.subheader("🎯 Tỷ lệ kỹ năng")
            st.plotly_chart(px.pie(df_exp.groupby('skills')['minutes'].sum().reset_index(), values='minutes', names='skills', hole=0.4), use_container_width=True)
        with c_b:
            st.subheader("🔥 Kỹ năng qua các ngày")
            st.plotly_chart(px.bar(df_exp.groupby(['date', 'skills'])['minutes'].sum().reset_index(), x='date', y='minutes', color='skills'), use_container_width=True)
        
        st.subheader("📜 Nhật ký chi tiết")
        st.dataframe(df_study.sort_values(by='timestamp', ascending=False), use_container_width=True)
    else: st.info("Chưa có dữ liệu.")

st.markdown("---")
st.caption("GLOW INFINITY ULTIMATE v10.0 • Xây dựng bởi 05 Thái Bảo • 2024")




# cấu hình app
st.set_page_config(page_title="Life Through Numbers", layout="wide", page_icon="💎")

# ================== CUSTOM UI ==================
def apply_custom_theme():
    st.markdown("""
        <style>
        /* set font + nền */
        .stApp { background: #0b0f1a; color: #e2e8f0; }

        /* card kiểu kính */
        .glass-card {
            backdrop-filter: blur(10px);
            border-radius: 20px; padding: 25px;
        }

        /* timer to */
        .timer-display {
            font-size: 85px !important;
            color: #00f2fe; text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_theme()  # gọi hàm để áp dụng CSS

# ================== DATABASE ==================
DB_FILES = {
    "study": "ultimate_study_db.csv",
    "knowledge": "ultimate_knowledge_db.csv",
    "tasks": "ultimate_tasks_db.csv"
}

# tạo file nếu chưa có
def init_db():
    for key, path in DB_FILES.items():
        if not os.path.exists(path) or os.stat(path).st_size == 0:
            if key == "study":
                pd.DataFrame(columns=["timestamp", "date", "minutes", "skills"]).to_csv(path, index=False)
            elif key == "knowledge":
                pd.DataFrame(columns=["date", "topic", "content", "category"]).to_csv(path, index=False)
            elif key == "tasks":
                pd.DataFrame(columns=["date", "task", "status", "priority"]).to_csv(path, index=False)

init_db()

# load dữ liệu từ file
def load_db(key):
    try:
        df = pd.read_csv(DB_FILES[key])
        if "date" in df.columns and not df.empty:
            df["date"] = pd.to_datetime(df["date"]).dt.date  # convert về date
        return df
    except:
        return pd.DataFrame()  # nếu lỗi trả về bảng rỗng

# lưu phiên học
def save_study_session(minutes, skills_list):
    df = load_db("study")

    # chuyển list skill thành string
    skills_str = ", ".join(skills_list) if skills_list else "General"

    new_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().date(),
        "minutes": round(minutes, 2),
        "skills": skills_str
    }

    # thêm dòng mới
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DB_FILES["study"], index=False)

# tính tổng giờ mỗi skill
def get_skill_totals():
    df = load_db("study")
    if df.empty:
        return {}

    df_exp = df.copy()

    # tách skill thành list
    df_exp['skills'] = df_exp['skills'].str.split(', ')

    # explode: mỗi skill thành 1 dòng
    df_exp = df_exp.explode('skills')

    # group lại và tính tổng phút -> đổi sang giờ
    totals = df_exp.groupby('skills')['minutes'].sum() / 60
    return totals.to_dict()

# tính level
def get_level_info(total_min):
    xp = int(total_min * 12)  # mỗi phút = 12 XP
    level = int((xp / 600)**0.6) + 1  # công thức level
    progress = (xp % 1200) / 1200  # tiến trình level
    return level, xp, min(max(float(progress), 0.0), 1.0)

# ================== SIDEBAR ==================
with st.sidebar:
    st.markdown("<h1>💎 GLOW INFINITY</h1>", unsafe_allow_html=True)

    df_s_sidebar = load_db("study")

    # tổng phút
    total_m = df_s_sidebar["minutes"].sum() if not df_s_sidebar.empty else 0

    lv, total_xp, prog_val = get_level_info(total_m)

    # hiển thị level
    st.markdown(f"Level {lv}")
    st.progress(prog_val)

    # chọn page
    page = st.radio("Menu", ["Dashboard", "Focus", "Tasks"])

# ================== DASHBOARD ==================
if page == "Dashboard":
    st.title("Tổng quan")

    df = load_db("study")

    today = datetime.now().date()

    # tổng hôm nay
    today_m = df[df['date'] == today]['minutes'].sum() if not df.empty else 0

    st.metric("Hôm nay", f"{today_m:.0f} phút")

# ================== FOCUS HUB ==================
elif page == "Focus":

    # tạo state nếu chưa có
    if 't_on' not in st.session_state:
        st.session_state.t_on = False

    if 't_elapsed' not in st.session_state:
        st.session_state.t_elapsed = 0

    if 't_start' not in st.session_state:
        st.session_state.t_start = None

    # chọn skill
    selected_skills = st.multiselect("Skill", ["Reading", "Writing", "Coding"])

    # cập nhật timer mỗi giây
    @st.fragment(run_every=1.0)
    def update_timer():
        if st.session_state.t_on:
            st.session_state.t_elapsed = t_module.time() - st.session_state.t_start

        secs = int(st.session_state.t_elapsed)
        st.markdown(f"<h1>{timedelta(seconds=secs)}</h1>", unsafe_allow_html=True)

    update_timer()

    # START
    if st.button("START"):
        st.session_state.t_on = True
        st.session_state.t_start = t_module.time() - st.session_state.t_elapsed
        st.rerun()

    # PAUSE
    if st.button("PAUSE"):
        st.session_state.t_on = False
        st.rerun()

    # RESET
    if st.button("RESET"):
        st.session_state.t_on = False
        st.session_state.t_elapsed = 0
        st.rerun()

    # SAVE
    if st.button("SAVE"):
        if st.session_state.t_elapsed > 10:
            save_study_session(st.session_state.t_elapsed / 60, selected_skills)
            st.success("Đã lưu!")
        else:
            st.warning("Quá ngắn!")

# ================== TASK ==================
elif page == "Tasks":
    st.title("Checklist")

    df_t = load_db("tasks")

    # thêm task
    task_name = st.text_input("Task")

    if st.button("Thêm"):
        new_t = pd.DataFrame([{
            "date": datetime.now().date(),
            "task": task_name,
            "status": "Pending",
            "priority": "Cao"
        }])

        pd.concat([df_t, new_t]).to_csv(DB_FILES["tasks"], index=False)
        st.rerun()

    # hiển thị task
    for idx, r in df_t.iterrows():
        done = st.checkbox(r['task'], value=(r['status']=="Done"))

        if done:
            df_t.at[idx, 'status'] = "Done"
            df_t.to_csv(DB_FILES["tasks"], index=False)