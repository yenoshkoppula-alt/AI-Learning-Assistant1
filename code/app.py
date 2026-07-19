import streamlit as st
import os
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# Import local modules
from logger import init_logger, log_interaction
from emotion_detector import detect_emotion
from gemini_helper import generate_response
from dashboard import render_dashboard

# App config
st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize files
init_logger()

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4b5563;
        margin-bottom: 2rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 12px;
        background-color: #f3f4f6;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Sidebar
with st.sidebar:
    st.title("🎓 Navigation")
    view_mode = st.radio(
        "Select Section:",
        ["🏠 Learning Hub", "📊 Student Dashboard"]
    )
    
    st.divider()
    st.info("💡 **Mentor Tip:** Being honest with your learning assistant about your current mood helps tailors your advice!")

# Home page: Learning Hub
if view_mode == "🏠 Learning Hub":
    st.markdown("<h1 class='main-header'>AI Learning Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>A compassionate, AI-powered study mentor adapting to your emotional state.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("How are you feeling about your studies today?")
        user_input = st.text_area(
            "Share your thoughts, challenges, or plans:",
            placeholder="E.g., I'm so stressed out by tomorrow's calculus quiz. I keep forgetting formulas...",
            height=150
        )
        
        submit_btn = st.button("Analyze & Get Mentor Guidance", type="primary")

    if submit_btn and user_input.strip() != "":
        # 1. Detect Emotion
        res = detect_emotion(user_input)
        emotion = res["emotion"]
        confidence = res["confidence"]

        # 2. Generate Gemini response
        with st.spinner("Connecting with your AI study mentor..."):
            ai_response = generate_response(user_input, emotion, confidence)

        # 3. Save to local CSV database
        log_interaction(user_input, emotion, confidence, ai_response)

        # 4. Display results in column 2
        with col2:
            st.subheader("Your Study Mentor says:")
            
            # Show detected emotion with custom accenting
            emotion_emojis = {
                "Happy": "😊", "Sad": "😢", "Angry": "😠", 
                "Stressed": "😫", "Anxious": "😰", "Motivated": "🔥", 
                "Confused": "🤔", "Neutral": "😐"
            }
            emoji = emotion_emojis.get(emotion, "😐")
            
            st.info(f"**Detected Mood:** {emoji} **{emotion}** (Confidence: {confidence})")
            
            # Guidance block
            st.markdown(f"<div class='card'>{ai_response}</div>", unsafe_allow_html=True)
            st.success("Successfully logged interaction details inside data/emotion_logs.csv!")
            
    elif submit_btn:
        st.warning("Please type your thoughts before requesting guidance!")

# Dashboard page
else:
    render_dashboard()