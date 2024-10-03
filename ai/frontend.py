import streamlit as st
from graph import run_vendor_inference, vendor  # Importing necessary components from graph.py
import time
from collections import deque

# Streamed response emulator, now utilizing the real response generator from your graph
def response_generator(message, user_id="123"):
    events = run_vendor_inference(vendor, message, user_id)
    # breakpoint()
    return events
    # for word in events.split():
    #     yield word + " "
    #     time.sleep(0.05)


st.title("Assistente de Vendas Drop 🎾🏖️ - Demo 02/10")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("O que gostaria de comprar hoje? 🎾"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response using your actual AI model
    with st.chat_message("assistant"):
        response = response_generator(prompt)
        st.markdown(response)
        # for chunk in response_generator(prompt):
        #     response += chunk
        #     st.markdown(chunk)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})