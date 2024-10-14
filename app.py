import streamlit as st
import google.generativeai as genai

# Function to initialize the Gemini API client
def initialize_gemini():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Function to interact with Gemini Chatbot
def chat_with_gemini(user_message, chat_session):
    # Send the user message to the chat session
    response = chat_session.send_message(user_message)
    return response.text.strip()

# Streamlit app UI
def main():
    st.title("Gemini AI Chatbot")
    st.write("Chat with the AI-powered chatbot below.")

    # Initialize Gemini API and create a chat session
    initialize_gemini()
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    chat_session = model.start_chat(history=[])

    # Initialize session state for storing conversation history and user input
    if 'history' not in st.session_state:
        st.session_state.history = []

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Get user input
    user_input = st.text_input("You:", key="user_input")

    # When the user submits a message
    if st.button("Send"):
        if user_input.strip() != "":
            # Append user message to history
            st.session_state.history.append(("You", user_input))

            # Get chatbot's response
            with st.spinner("Thinking..."):
                bot_response = chat_with_gemini(user_input, chat_session)
            
            # Append bot response to history
            st.session_state.history.append(("Bot", bot_response))

            # Clear the input after sending
            st.session_state.user_input = ""

    # Display the conversation history
    if st.session_state.history:
        st.write("## Conversation:")
        for speaker, message in st.session_state.history:
            st.markdown(f"**{speaker}:** {message}")

if __name__ == "__main__":
    main()
