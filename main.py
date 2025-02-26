import streamlit as st
import anthropic
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Claude Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Sidebar for API key and model selection
with st.sidebar:
    st.title("Claude Chatbot Settings")
    
    # API key input with secure handling
    api_key = st.text_input("Enter your Anthropic API Key:", type="password")
    
    # Model selection
    model_options = [
        "claude-3-7-sonnet-20250219",
        "claude-3-5-sonnet-20240620", 
        "claude-3-opus-20240229",
        "claude-3-5-haiku-20240307"
    ]
    model = st.selectbox("Select Claude Model:", model_options)
    
    st.divider()
    
    # Display the current date
    current_date = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"Current date: {current_date}")

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Claude. How can I help you today?"}
    ]

# Initialize Claude client when API key is provided
@st.cache_resource(show_spinner=False)
def get_client(api_key):
    return anthropic.Anthropic(api_key=api_key)

# Main chatbot interface
st.title("💬 Chat with Claude")

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate Claude's response
    with st.chat_message("assistant"):
        if not api_key:
            st.error("Please enter your Anthropic API key in the sidebar.")
        else:
            with st.spinner("Claude is thinking..."):
                try:
                    # Create the client
                    client = get_client(api_key)
                    
                    # Format the conversation history for Claude
                    messages = []
                    for msg in st.session_state.messages:
                        messages.append(
                            {"role": msg["role"], "content": msg["content"]}
                        )
                    
                    # Get response from Claude
                    response = client.messages.create(
                        model=model,
                        max_tokens=4000,
                        messages=messages,
                        system="You are Claude, an AI assistant created by Anthropic. You're helpful, harmless, and honest."
                    )
                    
                    # Display and store Claude's response
                    claude_response = response.content[0].text
                    st.markdown(claude_response)
                    st.session_state.messages.append({"role": "assistant", "content": claude_response})
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Add a button to clear the conversation
if st.button("Clear Conversation"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Claude. How can I help you today?"}
    ]
    st.experimental_rerun()

# CSS to improve the chat interface - removed background color for dark mode compatibility
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stChatInput {
        padding: 0.5rem;
    }
    /* Removed background color from chat messages */
    div[data-testid="stChatMessageContent"] {
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)