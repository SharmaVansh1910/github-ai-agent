import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import ask

# Page config
st.set_page_config(
    page_title="GitHub AI Agent",
    page_icon="🤖",
    layout="centered"
)

# Header
st.title("🤖 GitHub AI Agent")
st.markdown("**Powered by Gemini + MCP** — Ask anything about your GitHub!")
st.divider()

# Suggested questions
st.markdown("**💡 Try asking:**")
col1, col2 = st.columns(2)
with col1:
    if st.button("📁 What repos do I have?"):
        st.session_state.suggested = "What repos do I have?"
    if st.button("👤 Show my GitHub profile"):
        st.session_state.suggested = "Show my GitHub profile"
with col2:
    if st.button("🐛 Show open issues in my latest repo"):
        st.session_state.suggested = "Show open issues in my latest repo"
    if st.button("🔀 Any open PRs in my repos?"):
        st.session_state.suggested = "Any open PRs in my repos?"

st.divider()

# Initialize chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggested" not in st.session_state:
    st.session_state.suggested = ""

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle suggested question click
if st.session_state.suggested:
    prompt = st.session_state.suggested
    st.session_state.suggested = ""

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Talking to GitHub via MCP..."):
            response = ask(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask about your GitHub repos, issues, PRs..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Talking to GitHub via MCP..."):
            response = ask(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})