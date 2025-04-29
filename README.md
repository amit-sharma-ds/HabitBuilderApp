# 🌟 Life Quest Habit: A Habit Builder App

A gamified habit-tracking app where you earn points for good habits and spend them on fun rewards. Stay consistent, visualize your progress, and make habit-building exciting!

🔗 **Live App**: [https://habitbuilderapp.streamlit.app/](https://habitbuilderapp.streamlit.app/)

---

## 🚀 Features

- 🔐 **User Authentication**  
  Secure login/signup using Gmail (demo-based, in-memory authentication).

- ✅ **Daily Habit Tracking**  
  Complete tasks like:
  - Wake Up Early (+10 pts)
  - Study for 2 hours (+20 pts)
  - Meditate (+10 pts)
  - Gym Workout (+15 pts)

- 🎁 **Reward System**  
  Redeem your points on:
  - Watch Netflix (-10 pts)
  - Instagram 30 min (-10 pts)
  - Play Game 30 min (-10 pts)

- 📊 **Progress Visualization** *(via Plotly)*  
  - Donut Chart: Completed vs Remaining Points  
  - Bar Chart: Task-wise progress

- 🛠️ **Customization**  
  Add or delete your own habits and rewards.

- 🕒 **Daily Auto Reset**  
  All progress resets at the start of a new day to maintain consistency.

- 💾 **Session Memory**  
  Uses Streamlit’s session state to remember habits, rewards, and progress.

- 🌈 **Custom UI with CSS**  
  Stylish gradient background, colored buttons, and a smooth interface.

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit + custom CSS
- **Charts & Visualization**: Plotly
- **Backend Logic**: Python
- **User Data Management**: In-memory database using `st.session_state`
- **Authentication**: Custom login/signup system (demo purpose)
- **Deployment**: Streamlit Cloud

---

## 🔗 Links

- **GitHub Repo**: [https://github.com/your-username/life-quest-habit](https://github.com/your-username/life-quest-habit)
- **Live Demo**: [https://habitbuilderapp.streamlit.app/](https://habitbuilderapp.streamlit.app/)
