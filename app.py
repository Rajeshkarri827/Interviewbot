# import streamlit as st
# from prompts.question_generator import generate_questions
# from utils.conversation_flow import get_initial_prompt, update_conversation_state
# from dotenv import load_dotenv
# import os

# load_dotenv()
# print("Your OpenAI Key:", os.getenv("OPENAI_API_KEY"))
# print("Loaded OpenAI Key:", os.getenv("OPENAI_API_KEY"))


# load_dotenv()

# st.set_page_config(page_title="TalentScout InterviewBot", layout="centered")
# st.title("🤖 TalentScout AI Interview Assistant")

# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     st.session_state.step = 0
#     st.session_state.user_data = {}

# # Show chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Bot response logic
# def get_bot_response(user_input):
#     step = st.session_state.step
#     user_data = st.session_state.user_data

#     if step == 0:
#         st.session_state.user_data["name"] = user_input
#         st.session_state.step += 1
#         return "Nice to meet you! What's your email address?"

#     elif step == 1:
#         st.session_state.user_data["email"] = user_input
#         st.session_state.step += 1
#         return "Thanks! What's your phone number?"

#     elif step == 2:
#         st.session_state.user_data["phone"] = user_input
#         st.session_state.step += 1
#         return "Awesome. Which role are you looking for? (e.g., Frontend Developer, Python Developer, Data Analyst)"

#     elif step == 3:
#         st.session_state.user_data["role"] = user_input
#         st.session_state.step += 1
#         return "Great choice! Let me fetch some interview questions for that role..."

#     elif step == 4:
#         role = user_data["role"]
#         questions = generate_questions(role)
#         st.session_state.step += 1
#         return questions

#     else:
#         return "I’ve already given you the interview questions. Restart the app to try again!"

# # User input
# if prompt := st.chat_input("Say something..."):
#     # Show user message
#     st.chat_message("user").markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Bot response
#     if len(st.session_state.messages) == 1:
#         bot_msg = get_initial_prompt()
#     else:
#         bot_msg = get_bot_response(prompt)

#     st.chat_message("assistant").markdown(bot_msg)
#     st.session_state.messages.append({"role": "assistant", "content": bot_msg})


# import streamlit as st
# from dotenv import load_dotenv
# import os

# from prompts.question_generator import generate_questions
# from utils.conversation_flow import get_initial_prompt

# load_dotenv()

# st.set_page_config(page_title="TalentScout AI", layout="centered")
# st.title("🤖 TalentScout - AI InterviewBot")

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     st.session_state.step = 0
#     st.session_state.user_data = {}
#     st.session_state.questions = []
#     st.session_state.current_q_index = 0

# # Show previous messages
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Define how the bot responds
# def get_bot_response(user_input):
#     step = st.session_state.step
#     user_data = st.session_state.user_data

#     if step == 0:
#         user_data["name"] = user_input
#         st.session_state.step += 1
#         return "Nice to meet you! What's your email address?"

#     elif step == 1:
#         user_data["email"] = user_input
#         st.session_state.step += 1
#         return "Thanks! What's your phone number?"

#     elif step == 2:
#         user_data["phone"] = user_input
#         st.session_state.step += 1
#         return "Great! What role are you looking for? (e.g., Python Developer, JavaScript, React, etc.)"

#     elif step == 3:
#         user_data["role"] = user_input
#         st.session_state.step += 1

#         # Get questions from LLM or fallback
#         question_text = generate_questions(user_input)
#         question_list = question_text.split("\n")
#         st.session_state.questions = [q.strip("- ").strip() for q in question_list if q.strip()]
#         st.session_state.current_q_index = 0

#         if st.session_state.questions:
#             return f"Let's begin your interview for *{user_input}*.\n\n**Question 1:** {st.session_state.questions[0]}"
#         else:
#             return "Sorry, I couldn’t find any questions for that role."

#     elif step == 4:
#         idx = st.session_state.current_q_index
#         if idx < len(st.session_state.questions) - 1:
#             st.session_state.current_q_index += 1
#             return f"**Question {idx + 2}:** {st.session_state.questions[idx + 1]}"
#         else:
#             st.session_state.step += 1
#             return "🎉 Thank you for answering all the questions! We'll get back to you shortly."

#     else:
#         return "✅ You've completed the interaction. Refresh the page to restart."

# # Handle user input
# if prompt := st.chat_input("Your response..."):
#     # Display user message
#     st.chat_message("user").markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Bot logic
#     if len(st.session_state.messages) == 1:
#         bot_response = get_initial_prompt()
#     else:
#         bot_response = get_bot_response(prompt)

#     st.chat_message("assistant").markdown(bot_response)
#     st.session_state.messages.append({"role": "assistant", "content": bot_response})


import streamlit as st
from dotenv import load_dotenv
import os

from prompts.question_generator import generate_questions
from utils.conversation_flow import get_initial_prompt

load_dotenv()

st.set_page_config(page_title="TalentScout AI", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 TalentScout - AI InterviewBot</h1>", unsafe_allow_html=True)

# Inject CSS to style chat alignment
st.markdown("""
<style>
.chat-left .element-container:nth-child(1) {
    justify-content: flex-start;
}
.chat-right .element-container:nth-child(1) {
    justify-content: flex-end;
}
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0
    st.session_state.user_data = {}
    st.session_state.questions = []
    st.session_state.current_q_index = 0

    # Add bot's initial greeting
    initial_greeting = get_initial_prompt()
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Display messages
for msg in st.session_state.messages:
    align = "chat-left" if msg["role"] == "assistant" else "chat-right"
    with st.container():
        with st.chat_message(msg["role"]):
            st.markdown(f"<div class='{align}'>{msg['content']}</div>", unsafe_allow_html=True)

# Bot logic
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
        idx = st.session_state.current_q_index
        if idx < len(st.session_state.questions) - 1:
            st.session_state.current_q_index += 1
            return f"**Question {idx + 2}:** {st.session_state.questions[idx + 1]}"
        else:
            st.session_state.step += 1
            return "🎉 Thank you for answering all the questions! We'll get back to you shortly."

    else:
        return "✅ You've completed the interaction. Refresh the page to restart."

# Handle user input
if prompt := st.chat_input("Your response..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    bot_response = get_bot_response(prompt)
    st.chat_message("assistant").markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
