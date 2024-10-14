import streamlit as st
import google.generativeai as genai

# Function to initialize the Gemini API client
def initialize_gemini():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def chat_with_gemini(input_query):
    # Initialize the model configuration
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 50,
        "max_output_tokens": 1000,
    }

    # Initialize the model with the specified configuration
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Start a new chat session
    chat_session = model.start_chat(history=[])

    # Send the message and get a response
    response = chat_session.send_message(input_query)

    # Return the generated response
    return response.text.strip()

# Streamlit app UI
def main():
    st.title("Chatbot AI Project")
    st.write("Welcome to the chatbot! Ask me anything.")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                initialize_gemini()
                response = chat_with_gemini(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()