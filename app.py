import streamlit as st
from streamlit_ace import st_ace
import sys
import io

# Set up the page layout with two columns
st.set_page_config(layout="wide")

# Page Title
st.title("Scientia - AI Tutor for Data Science and Machine Learning")

# Create two columns, left for code editor and output, right for the chatbot (placeholder for now)
col1, col2 = st.columns([2, 1])

# Left Column: Code Editor and Output
with col1:
    st.subheader("Code Editor")
    
    # Use st_ace to create an Ace code editor with VS Code Dark theme
    code = st_ace(
        language='python',
        theme='github',  # Set the theme to VS Code Dark
        key='ace_editor',
        height=300,
        font_size=14,
        tab_size=4,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
    )
    
    # Button to run code
    if st.button("Run Code"):
        output = io.StringIO()  # Create a string buffer to capture output
        error = None
        
        try:
            # Redirect stdout to capture print statements
            sys.stdout = output
            exec(code, {})  # Execute the user's code
        except Exception as e:
            error = str(e)
        finally:
            # Reset stdout to default
            sys.stdout = sys.__stdout__

        # If there was an error, show it in the output
        if error:
            st.text_area("Output", value=f"Error: {error}", height=200)
        else:
            # Show the captured output
            st.text_area("Output", value=output.getvalue(), height=200)

# Right Column: Placeholder for AI Chatbot
with col2:
    st.subheader("AI-Tutor Chatbot (Coming Soon)")
    st.write("This space is reserved for the chatbot that will assist in learning.")
