# import openai
# import os

# openai.api_key = os.getenv("OPENAI_API_KEY")

# def generate_questions(role):
#     prompt = (
#         f"Generate 5 short, relevant technical interview questions for the role: {role}.\n"
#         f"Keep them concise and clear."
#     )

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are an expert HR interviewer."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.7,
#             max_tokens=400
#         )
#         return response["choices"][0]["message"]["content"]

#     except Exception as e:
#         return f"⚠️ Error generating questions: {str(e)}"

# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()  # ⬅️ This must be before accessing env vars

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_questions(role):
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are an expert HR interviewer."},
#                 {"role": "user", "content": f"Generate 5 technical interview questions for the role: {role}"}
#             ],
#             temperature=0.7,
#             max_tokens=400
#         )
#         return response.choices[0].message.content

#     except Exception as e:
#         return f"⚠️ Error generating questions:\n\n{str(e)}"

# 

import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts.fallback_questions import get_fallback_questions

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def generate_questions(role):
    if not api_key:
        return get_fallback_questions(role)

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert HR interviewer."},
                {"role": "user", "content": f"Generate 5 technical interview questions for the role: {role}"}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content

    except Exception:
        return get_fallback_questions(role)
