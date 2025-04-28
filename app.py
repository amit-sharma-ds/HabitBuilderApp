import streamlit as st
import datetime
from pathlib import Path
from auth import init_user_db, signup_page, login_page
import plotly.express as px  # <- For charts

# ---- Load custom CSS ----
def load_css():
    css_file = Path("style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---- Initialize user database ----
init_user_db()

# ---- Authentication Flow ----
if not st.session_state.logged_in:
    auth_mode = st.sidebar.selectbox("Choose Mode", ["Sign Up", "Login"])
    if auth_mode == "Login":
        login_page()
    else:
        signup_page()

    st.stop()  # <-- Stop until logged in

# ---- Main App Starts ----

# Initialize app state
def initialize_app_state():
    if "total_points" not in st.session_state:
        st.session_state.total_points = 0
    if "completed_habits" not in st.session_state:
        st.session_state.completed_habits = set()
    if "custom_habits" not in st.session_state:
        st.session_state.custom_habits = []
    if "custom_rewards" not in st.session_state:
        st.session_state.custom_rewards = []
    if "default_habits" not in st.session_state:
        st.session_state.default_habits = [
            {"habit": "Wake Up Early", "points": 10},
            {"habit": "Gym Workout", "points": 15},
            {"habit": "Meditate", "points": 10},
            {"habit": "Study for 2 hours", "points": 20},
            {"habit": "Study 8-11 AM", "points": 6},
            {"habit": "Study 2-4 PM", "points": 4},
            {"habit": "Study After 10 PM", "points": 2},
        ]
    if "default_rewards" not in st.session_state:
        st.session_state.default_rewards = [
            {"reward": "Watch Netflix before 8 PM", "cost": 10},
            {"reward": "Watch Netflix after 8 PM", "cost": 15},
            {"reward": "Play Game for 30 minutes", "cost": 10},
            {"reward": "Instagram for 30 minutes", "cost": 10},
        ]
    if "date" not in st.session_state:
        st.session_state.date = datetime.date.today()

initialize_app_state()

# Daily Reset
if st.session_state.date != datetime.date.today():
    st.session_state.total_points = 0
    st.session_state.completed_habits = set()
    st.session_state.custom_habits = []
    st.session_state.custom_rewards = []
    st.session_state.date = datetime.date.today()

# ---- UI Start ----
st.markdown("<h1 style='text-align: left;'>🌟 Life Quest Habit:<br> A Habit Builder App 🌟</h1>", unsafe_allow_html=True)
st.caption(f"Welcome to Life Quest Habit: A Habit Builder App - Today's Date: {st.session_state.date.strftime('%B %d, %Y')}")

# Sidebar Navigation
st.sidebar.title("Life Quest Habit: A Habit Builder App")
tabs = ["Life Quest Habit", "Rewards", "Customize", "Progress Viz", "Reset"]
tab = st.sidebar.radio("Select a Section", tabs)

# Points threshold for warning
POINTS_WARNING_THRESHOLD = 5

# Function to display warning when points are low
def show_low_points_warning():
    if st.session_state.total_points < POINTS_WARNING_THRESHOLD:
        st.warning("⚠️ You have low points! Complete more tasks or redeem fewer rewards.")

# ---- Tabs ----
if tab == "Life Quest Habit":
    st.subheader(f"🏅 Total Points: {st.session_state.total_points}")
    show_low_points_warning()  # Show the warning if points are low

    all_tasks = st.session_state.default_habits + st.session_state.custom_habits

    st.write("### ✅ Complete Your Habit Quest")
    for habit in all_tasks:
        is_checked = habit['habit'] in st.session_state.completed_habits
        checked = st.checkbox(f"{habit['habit']} (+{habit['points']} pts)", value=is_checked, key=f"task_{habit['habit']}")

        if checked and not is_checked:
            st.session_state.total_points += habit['points']
            st.session_state.completed_habits.add(habit['habit'])
            st.rerun()

        if not checked and is_checked:
            st.session_state.total_points -= habit['points']
            st.session_state.completed_habits.remove(habit['habit'])
            st.rerun()

elif tab == "Rewards":
    st.subheader(f"🏅 Total Points: {st.session_state.total_points}")
    show_low_points_warning()  # Show the warning if points are low

    all_rewards = st.session_state.default_rewards + st.session_state.custom_rewards

    st.write("### 🎁 Redeem Rewards")
    for reward in all_rewards:
        if st.button(f"{reward['reward']} (-{reward['cost']} pts)", key=f"reward_{reward['reward']}"):
            if st.session_state.total_points >= reward['cost']:
                st.session_state.total_points -= reward['cost']
                st.success(f"🎉 Enjoy {reward['reward']}!")
                st.rerun()
            else:
                st.error(f"❌ Not enough points!")

elif tab == "Customize":
    st.header("🛠️ Customize Tasks & Rewards")

    # Add new task
    st.subheader("📋 Add New Task")
    with st.expander("➕ Add Task"):
        task_name = st.text_input("Task Name", key="add_task_name")
        task_points = st.number_input("Task Points", min_value=1, value=5, key="add_task_points")
        if st.button("Add Task"):
            if task_name:
                st.session_state.custom_habits.append({"habit": task_name, "points": task_points})
                st.success(f"Task added!")
                st.rerun()
            else:
                st.error("Task name cannot be empty!")

    # Delete tasks
    st.write("### 🗑️ Delete Tasks")
    for habit in st.session_state.default_habits + st.session_state.custom_habits:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"{habit['habit']} ({habit['points']} pts)")
        with col2:
            if st.button("Delete", key=f"delete_task_{habit['habit']}"):
                if habit in st.session_state.custom_habits:
                    st.session_state.custom_habits.remove(habit)
                elif habit in st.session_state.default_habits:
                    st.session_state.default_habits.remove(habit)
                st.success(f"Deleted!")
                st.rerun()

    st.markdown("---")

    # Add new reward
    st.subheader("🎁 Add New Reward")
    with st.expander("➕ Add Reward"):
        reward_name = st.text_input("Reward Name", key="add_reward_name")
        reward_cost = st.number_input("Reward Cost", min_value=1, value=5, key="add_reward_cost")
        if st.button("Add Reward"):
            if reward_name:
                st.session_state.custom_rewards.append({"reward": reward_name, "cost": reward_cost})
                st.success(f"Reward added!")
                st.rerun()
            else:
                st.error("Reward name cannot be empty!")

    # Delete rewards
    st.write("### 🗑️ Delete Rewards")
    for reward in st.session_state.default_rewards + st.session_state.custom_rewards:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"{reward['reward']} ({reward['cost']} pts)")
        with col2:
            if st.button("Delete", key=f"delete_reward_{reward['reward']}"):
                if reward in st.session_state.custom_rewards:
                    st.session_state.custom_rewards.remove(reward)
                elif reward in st.session_state.default_rewards:
                    st.session_state.default_rewards.remove(reward)
                st.success(f"Deleted!")
                st.rerun()

elif tab == "Progress Viz":
    st.header("📊 Progress Visualization")

    # Donut chart: Overall Progress (Completed vs Remaining Points)
    all_tasks = st.session_state.default_habits + st.session_state.custom_habits
    total_tasks_points = sum(habit['points'] for habit in all_tasks)
    completed_points = st.session_state.total_points
    remaining_points = max(total_tasks_points - completed_points, 0)

    progress_data = {
        'Category': ['Completed Points', 'Remaining Points'],
        'Points': [completed_points, remaining_points]
    }

    fig_donut = px.pie(progress_data, names='Category', values='Points', hole=0.4, title="Overall Progress")
    st.plotly_chart(fig_donut)

    # Bar chart: Task-wise progress (Points accumulated per task)
    task_names = [habit['habit'] for habit in all_tasks]
    task_points = [
        habit['points'] if habit['habit'] in st.session_state.completed_habits else 0
        for habit in all_tasks
    ]

    task_progress = px.bar(
        x=task_names,
        y=task_points,
        labels={'x': 'Tasks', 'y': 'Points'},
        title="Progress on Tasks"
    )
    st.plotly_chart(task_progress)

elif tab == "Reset":
    st.header("🔄 Reset Section")

    if st.button("Reset Custom Tasks"):
        st.session_state.custom_habits = []
        st.session_state.completed_habits = set()
        st.success("✅ Custom tasks reset!")
        st.rerun()

    # Reset Custom Rewards
    if st.button("Reset Custom Rewards"):
        st.session_state.custom_rewards = []
        st.success("✅ Custom rewards reset!")
        st.rerun()

    # Reset All Tasks & Rewards (including custom and default tasks)
    if st.button("Reset All Tasks & Rewards"):
        st.session_state.total_points = 0
        st.session_state.completed_habits = set()
        st.session_state.custom_habits = []
        st.session_state.custom_rewards = []
        st.session_state.date = datetime.date.today()
        st.success("✅ All tasks and rewards reset!")
        st.rerun()
