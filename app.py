import streamlit as st
from dotenv import load_dotenv
import os
from prompts.generate_feedback import generate_feedback 
from prompts.question_generator import generate_questions
from utils.conversation_flow import get_initial_prompt

# Load environment variables
load_dotenv()

# Streamlit config
st.set_page_config(page_title="TalentScout AI", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Title
st.markdown("<h1 style='text-align: center;'>🤖 TalentScout - AI InterviewBot</h1>", unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0
    st.session_state.user_data = {}
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.current_q_index = 0
    st.session_state.feedback_rating = None  # For storing the feedback rating

    initial_greeting = get_initial_prompt()
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Sidebar summary and feedback rating
with st.sidebar:
    st.markdown("### 🧾 Interview Summary")
    user_data = st.session_state.user_data
    if "name" in user_data:
        st.markdown(f"👤 **Name:** {user_data['name']}")
    if "email" in user_data:
        st.markdown(f"📧 **Email:** {user_data['email']}")
    if "phone" in user_data:
        st.markdown(f"📱 **Phone:** {user_data['phone']}")
    if "role" in user_data:
        st.markdown(f"💼 **Role:** {user_data['role']}")

    if st.session_state.questions:
        st.markdown("---")
        st.markdown("### 🧠 Interview Q&A")
        for i, (q, a) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
            st.markdown(f"**Q{i+1}:** {q}")
            st.markdown(f"*A{i+1}:* {a}")
    
    if st.session_state.feedback_rating is not None:
        st.markdown("---")
        st.markdown("### 📊 Interview Rating")
        st.markdown(f"⭐ **Rating:** {st.session_state.feedback_rating}")

# Display chat messages
for msg in st.session_state.messages:
    role_class = "message-bot" if msg["role"] == "assistant" else "message-user"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# Chat logic
def get_bot_response(user_input):
    step = st.session_state.step
    user_data = st.session_state.user_data

    if step == 0:
        user_data["name"] = user_input
        st.session_state.step += 1
        return "Nice to meet you! What's your email address?"

    elif step == 1:
        user_data["email"] = user_input
        st.session_state.step += 1
        return "Thanks! What's your phone number?"

    elif step == 2:
        user_data["phone"] = user_input
        st.session_state.step += 1
        return "Great! What role are you looking for? (e.g., Python Developer, JavaScript, React, etc.)"

    elif step == 3:
        user_data["role"] = user_input
        st.session_state.step += 1

        question_text = generate_questions(user_input)
        question_list = question_text.split("\n")
        st.session_state.questions = [q.strip("- ").strip() for q in question_list if q.strip()]
        st.session_state.current_q_index = 0

        if st.session_state.questions:
            return f"Let's begin your interview for *{user_input}*.\n\n**Question 1:** {st.session_state.questions[0]}"
        else:
            return "Sorry, I couldn’t find any questions for that role."

    elif step == 4:
        st.session_state.answers.append(user_input)
        idx = st.session_state.current_q_index

        if idx < len(st.session_state.questions) - 1:
            st.session_state.current_q_index += 1
            return f"**Question {idx + 2}:** {st.session_state.questions[idx + 1]}"
        else:
            st.session_state.step += 1
            return "🎉 Thank you for answering all the questions! Generating your feedback..."

    elif step == 5:
        # Generate feedback
        feedback = generate_feedback(
            st.session_state.questions,
            st.session_state.answers,
            st.session_state.user_data.get("role", "unknown role")
        )
        
        # Extract rating from feedback
        # Assuming the feedback has a rating in the format: "Rating: 4/5" (adjust as per actual feedback format)
        rating = "⭐ 4/5"  # Replace with actual extraction logic from the feedback if available
        st.session_state.feedback_rating = rating
        
        st.session_state.step += 1
        return f"✅ Here's your feedback:\n\n{feedback}"

    else:
        return "✅ You've completed the interaction. Refresh the page to restart."

# Handle user input
if prompt := st.chat_input("Your response..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    bot_response = get_bot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.rerun()

