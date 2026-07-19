import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define color schema for consistent rendering
EMOTION_COLORS = {
    "Happy": "#eab308",
    "Sad": "#3b82f6",
    "Angry": "#ef4444",
    "Stressed": "#a855f7",
    "Anxious": "#f97316",
    "Motivated": "#22c55e",
    "Confused": "#06b6d4",
    "Neutral": "#6b7280"
}

def render_dashboard():
    st.header("📊 Student Analytics Dashboard")
    
    LOG_FILE = "data/emotion_logs.csv"
    if not os.path.exists(LOG_FILE):
        st.info("No records are currently logged. Head to the Learning Hub to start a session!")
        return

    try:
        df = pd.read_csv(LOG_FILE)
        df.columns = [col.strip() for col in df.columns]
        
        # Check if 'Emotion' is present, or if headers are missing (and we have 5 columns)
        has_emotion = any(col.lower() == 'emotion' for col in df.columns)
        if not has_emotion and len(df.columns) == 5:
            # Re-read treating the first row as actual data instead of a header
            df = pd.read_csv(LOG_FILE, header=None, names=["Timestamp", "User Input", "Emotion", "Confidence", "AI Response"])
    except Exception as e:
        st.error(f"Error reading logs: {e}")
        return

    if df.empty:
        st.info("Your log CSV is empty. Start a conversation with your mentor!")
        return

    # Normalize column names to strip whitespace and match case-insensitively
    df.columns = [col.strip() for col in df.columns]
    
    # Locate 'Emotion' column robustly (case-insensitive)
    emotion_col = None
    for col in df.columns:
        if col.lower() == 'emotion':
            emotion_col = col
            break
            
    if not emotion_col:
        st.error(f"Could not find 'Emotion' column in the logs CSV. Available columns: {list(df.columns)}")
        st.warning("To fix this, please delete the local CSV file at 'data/emotion_logs.csv' and send a message in the chat. The assistant will automatically recreate it with correct column headers!")
        return

    # Total conversations stat
    total_convs = len(df)
    st.metric("Total Learning Sessions Logged", total_convs)

    # Split into two columns for plots
    col1, col2 = st.columns(2)

    # 1. Bar Chart: Emotion Frequencies
    with col1:
        st.subheader("Emotion Prevalence")
        emotion_counts = df[emotion_col].value_counts()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        # Map colors based on index
        colors = [EMOTION_COLORS.get(emo, "#cccccc") for emo in emotion_counts.index]
        emotion_counts.plot(kind='bar', color=colors, ax=ax)
        ax.set_ylabel("Occurrences")
        ax.set_xlabel("Emotion")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    # 2. Pie Chart: Mix Percentage
    with col2:
        st.subheader("Emotional Distribution Mix")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        colors = [EMOTION_COLORS.get(emo, "#cccccc") for emo in emotion_counts.index]
        ax2.pie(
            emotion_counts, 
            labels=emotion_counts.index, 
            autopct='%1.1f%%', 
            colors=colors,
            startangle=90,
            textprops={'fontsize': 10}
        )
        ax2.axis('equal')  
        plt.tight_layout()
        st.pyplot(fig2)

    # Recent Records Table
    st.subheader("Recent CSV Logs")
    # Show last 10 entries reversed (latest first)
    st.dataframe(df.tail(10).iloc[::-1], use_container_width=True)