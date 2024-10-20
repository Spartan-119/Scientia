import streamlit as st
import streamlit_ace as st_ace
import sys
import io
from chatbot.agent import generate_response  # Import the chatbot response function
from chatbot.utils import write_message  # Helper function to display messages

# Set up the page layout with two columns
st.set_page_config(layout="wide")

# Page Title
st.title("Scientia - AI Tutor for Data Science and Machine Learning")

# Create two columns, left for code editor and output, right for the chatbot
col1, col2 = st.columns([2, 1])

# Left Column: Code Editor and Output
with col1:
    st.subheader("Code Editor")

    code = st_ace.st_ace(
        language='python',
        theme='merbivore',
        key='ace_editor',
        height=300,
        font_size=14,
        tab_size=4,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
    )

    if st.button("Run Code"):
        output = io.StringIO()  # Create a string buffer to capture output
        error = None

        try:
            sys.stdout = output
            exec(code, {})
        except Exception as e:
            error = str(e)
        finally:
            sys.stdout = sys.__stdout__

        if error:
            st.text_area("Output", value=f"Error: {error}", height=200)
        else:
            st.text_area("Output", value=output.getvalue(), height=200)

# Right Column: Chatbot Integration
with col2:
    st.subheader("AI-Tutor Chatbot")

    # Initialize chat session state if not already done
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi, I'm Scientia! How can I assist you today?"}
        ]

    # Display chat history
    for message in st.session_state.messages:
        write_message(message['role'], message['content'], save=False)

    # Handle user input in the chat
    user_input = st.text_input("Your message", "")
    
    if st.button("Send"):
        if user_input:
            # Save user input to chat history
            write_message('user', user_input)
            
            # Call chatbot to generate a response
            response = generate_response(user_input)
            
            # Save the AI response to chat history
            write_message('assistant', response)
