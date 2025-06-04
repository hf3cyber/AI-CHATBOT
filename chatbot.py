from dotenv import load_dotenv
from openai import OpenAI  
import streamlit as st
import os 


# Load environment variables 
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client instance
client = OpenAI(api_key=api_key)

# Initial system and assistant message
initial_message = [
    {
        "role": "system",
        "content": "You are a trip planner in Dubai. You are an expert in Dubai tourism, locations, food, events, hotels, etc. Your name is Dubai Genie, or DG for short. You respond professionally in under 200 words. Always ask users questions to help plan their trip, and finally provide a day-wise itinerary."
    },
    {
        "role": "assistant",
        "content": "Hello, I am Dubai Genie, your expert trip planner. How can I help you?"
    }
]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = initial_message

# Function to get AI response
def get_response_from_llm(messages):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or use "" if you don't have GPT-4 access
        messages=messages
    )
    return completion.choices[0].message.content

# Streamlit app title
st.title("Dubai Trip Assistant")

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
user_message = st.chat_input("Enter your message")

if user_message:
    # Append user's message
    new_message = {
        "role": "user",
        "content": user_message
    }
    st.session_state.messages.append(new_message)

    with st.chat_message("user"):
        st.markdown(user_message)

    # Get assistant response
    response = get_response_from_llm(st.session_state.messages)
    if response:
        response_message = {
            "role": "assistant",
            "content": response
        }
        # Append assistant's response
        st.session_state.messages.append(response_message)

        with st.chat_message(response_message["role"]):
            st.markdown(response_message["content"])
