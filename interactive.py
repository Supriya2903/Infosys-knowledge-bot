import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init_page():
    st.set_page_config(
        page_title="Infosys Chatbot"
    )
    st.header("Infosys Chatbot")

def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful AI assistant that helps users with information about Infosys.")
        ]

def get_openai_key():
    return os.getenv("OPENAI_API_KEY")

def get_chatbot():
    openai_api_key = get_openai_key()
    if not openai_api_key:
        st.error("Please set the OPENAI_API_KEY environment variable.")
        st.stop()
    
    return ChatOpenAI(
        temperature=0.7,
        openai_api_key=openai_api_key,
        model_name="gpt-3.5-turbo"
    )

def main():
    init_page()
    init_messages()
    chat = get_chatbot()

    if user_input := st.chat_input("Input your question!"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Bot is typing ..."):
            answer = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=answer.content))

    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)

if __name__ == '__main__':
    main()
