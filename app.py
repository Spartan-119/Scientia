import streamlit as st
import streamlit_ace as st_ace
import sys
import io
from chatbot.agent import generate_response
from chatbot.utils import write_message

# Set up the page layout with two columns
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Add custom CSS for layout and styling
st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Overall dark theme */
    .stApp {
        background-color: #1E1E1E;
        height: 100vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 0.5rem 0;
        margin-bottom: 0.5rem;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #E0E0E0;
        margin-bottom: 0.25rem;
        font-family: 'Arial Black', sans-serif;
    }
    
    .sub-title {
        font-size: 1.2rem;
        color: #B0B0B0;
        font-weight: bold;
        font-family: Arial, sans-serif;
    }

    /* Fix for panel containment */
    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
        height: calc(100vh - 120px);  /* Adjust for header */
    }
    
    .stColumn {
        background-color: #2D2D2D !important;
        border-radius: 10px;
        padding: 1rem !important;
        height: 100%;
        position: relative;
        display: flex;
        flex-direction: column;
    }

    /* Remove default padding from columns */
    [data-testid="column"] {
        padding: 1rem !important;
    }

    /* Chat panel containment and scrolling */
    .chat-container {
        flex-grow: 1;
        overflow-y: auto;
        max-height: 100%;  /* Ensure container only takes full height */
        padding-bottom: 80px;  /* Space for input */
    }

    /* Chat messages styling */
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 15px;
        max-width: 80%;
    }

    .assistant {
        background-color: #363636;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }

    .user {
        background-color: #0B93F6;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }

    /* Input container at bottom of the right panel */
    .input-container {
        position: sticky;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background-color: #2D2D2D;
        border-top: 1px solid #404040;
        z-index: 100;
    }

    /* Input field styling */
    .stTextInput {
        background-color: #2D2D2D;
    }

    .stTextInput > div > div > input {
        background-color: #363636;
        color: #E0E0E0;
        border: 1px solid #404040;
        border-radius: 20px;
        padding: 10px 15px;
    }

    /* Button styling */
    .stButton > button {
        background-color: #0B93F6;
        color: white;
        border-radius: 20px;
        border: none;
    }

    /* Code editor adjustments */
    .ace_editor {
        border-radius: 8px;
        margin: 1rem 0;
    }

    /* Output area */
    .stTextArea > div {
        background-color: #363636;
        color: #E0E0E0;
        border-radius: 8px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Custom Header
st.markdown("""
    <div class="main-header">
        <div class="main-title">Scientia</div>
        <div class="sub-title">AI Tutor for Data Science and Machine Learning</div>
    </div>
""", unsafe_allow_html=True)

# Create two columns with proper containment
left_col, right_col = st.columns(2)

# Left Column (Code Editor)
with left_col:
    st.markdown("### Code Editor")
    
    code = st_ace.st_ace(
        placeholder="Write your Python code here...",
        language='python',
        theme='monokai',
        key='ace_editor',
        height=400,
        font_size=14,
        tab_size=4,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
    )

    if st.button("Run Code"):
        output = io.StringIO()
        error = None
        
        try:
            sys.stdout = output
            exec(code, {})
        except Exception as e:
            error = str(e)
        finally:
            sys.stdout = sys.__stdout__

        if error:
            st.error(f"Error: {error}")
        else:
            st.code(output.getvalue(), language='python')

# Right Column (Chatbot)
with right_col:
    st.markdown("### AI-Tutor Chatbot")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi, I'm Scientia! How can I assist you today?"}
        ]

    # Create a container for chat messages
    chat_container = st.container()
    
    with chat_container:
        # Make chat container scrollable
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            st.markdown(
                f'<div class="chat-message {role}">{content}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat input and send button in a fixed container at the bottom of the right panel
    with st.container():
        input_container = st.empty()
        with input_container.container():
            col1, col2 = st.columns([5, 1])
            
            with col1:
                user_input = st.text_input("", placeholder="Type your message here...", key="chat_input")
            
            with col2:
                send_pressed = st.button("Send")

            if send_pressed and user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                combined_input = f"User message: {user_input}\n\nUser code:\n{code}\n\nOutput/Errors:\n{output.getvalue() if 'output' in locals() else ''}{error if 'error' in locals() else ''}"
                response = generate_response(combined_input)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
