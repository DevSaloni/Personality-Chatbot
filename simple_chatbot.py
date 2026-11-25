
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage
)

load_dotenv()

# Page configuration

st.set_page_config(
    page_title="Funny AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Initialize model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=256
)

# Short-term memory
if "message" not in st.session_state:
    st.session_state.message = [
        SystemMessage(content="you are a funny Ai agent")
    ]

# UI
st.title("🤖 Funny AI Chatbot")
st.caption("Chat with your funny AI assistant!")

st.divider()

# Display previous messages
for msg in st.session_state.message[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# User input
prompt = st.chat_input("Type your message...")

if prompt:
    if prompt == "0":
        st.session_state.message = [
            SystemMessage(content="you are a funny Ai agent")
        ]
        st.rerun()

    # Add user message
    st.session_state.message.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user"):
        st.write(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.invoke(st.session_state.message)
            st.write(response.content)

    # Add AI response to memory
    st.session_state.message.append(
        AIMessage(content=response.content)
    )
