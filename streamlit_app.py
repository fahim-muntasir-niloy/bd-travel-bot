import streamlit as st
from agent import agent
from langchain_core.messages import AIMessageChunk, HumanMessage
import time
import random

# Page configuration
st.set_page_config(
    page_title="BD Travel Bot",
    page_icon="🇧🇩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

# Enhanced CSS with modern design
st.markdown(
    """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .header-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        position: relative;
        z-index: 1;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: transparent;
        border: none;
        padding: 0;
        margin: 0 0 1rem 0;
    }
    
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px 20px 5px 20px;
        padding: 1rem 1.5rem;
        margin-left: 20%;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .stChatMessage[data-testid="assistant"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px 20px 20px 5px;
        padding: 1rem 1.5rem;
        margin-right: 20%;
        box-shadow: 0 5px 15px rgba(240, 147, 251, 0.3);
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Chat input styling */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7);
        font-weight: 400;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Welcome message styling */
    .welcome-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: float 3s ease-in-out infinite;
    }
    
    .welcome-message h3 {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        margin: 0 0 1rem 0;
    }
    
    .welcome-message p {
        font-size: 1rem;
        margin: 0;
        opacity: 0.9;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .feature-card h4 {
        color: #667eea;
        margin: 0 0 0.5rem 0;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
</style>
""",
    unsafe_allow_html=True,
)

# Enhanced Header
st.markdown(
    """
    <div class="header-container">
        <h1 class="header-title">🌏 BD Travel Bot</h1>
        <p class="header-subtitle">আপনার বাংলাদেশ ভ্রমণ গাইড - Ask me about tourist spots in Bangladesh!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Welcome message (only show once)
if not st.session_state.welcome_shown and len(st.session_state.messages) == 0:
    welcome_messages = [
        "🎉 Welcome to BD Travel Bot! I'm here to help you discover amazing places in Bangladesh!",
        "🌟 Ready to explore Bangladesh? Ask me about any tourist destination!",
        "🗺️ Let's plan your perfect Bangladesh adventure together!",
        "🏞️ Discover the beauty of Bangladesh with me as your guide!",
    ]

    st.markdown(
        f"""
        <div class="welcome-message">
            <h3>👋 {random.choice(welcome_messages)}</h3>
            <p>Try asking: "কুয়াকাটা সমুদ্র সৈকত সম্পর্কে বলুন" or "Tell me about Cox's Bazar"</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.welcome_shown = True

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Simple chat input
prompt = st.chat_input("Ask about tourist spots in Bangladesh...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display bot response with enhanced streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Add typing indicator
        typing_indicators = [
            "🤔 Thinking...",
            "🔍 Searching...",
            "✍️ Writing...",
            "📝 Preparing...",
        ]
        current_typing = random.choice(typing_indicators)
        message_placeholder.markdown(
            f"<div class='typing-indicator'>{current_typing}</div>",
            unsafe_allow_html=True,
        )

        # Stream the agent response
        try:
            chunk_count = 0
            for m, metadata in agent.stream(
                {"messages": [HumanMessage(content=prompt)]}, stream_mode="messages"
            ):
                if isinstance(m, AIMessageChunk):
                    full_response += m.content
                    chunk_count += 1

                    # Update display with streaming effect
                    if (
                        chunk_count % 3 == 0
                    ):  # Update every 3rd chunk for smoother effect
                        message_placeholder.markdown(full_response + "▌")
                        time.sleep(0.03)
                    else:
                        time.sleep(0.01)

            # Remove the cursor and display final response
            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "😔 Sorry, I encountered an error. Please try again.",
                }
            )

# Enhanced Sidebar
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: white; font-family: 'Poppins', sans-serif;">🇧🇩 BD Travel Bot</h2>
            <p style="color: rgba(255,255,255,0.8);">Your AI Travel Guide</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Feature cards
    st.markdown("### ✨ What I can help with:")

    features = [
        ("🏛️", "Historical Places", "Ancient monuments, heritage sites"),
        ("🏞️", "Natural Attractions", "Mountains, forests, waterfalls"),
        ("🏖️", "Beaches & Rivers", "Coastal areas, river destinations"),
        ("🍽️", "Local Cuisine", "Traditional food, restaurants"),
        ("🏨", "Accommodation", "Hotels, resorts, guesthouses"),
        ("🚗", "Transportation", "How to reach, travel tips"),
    ]

    for emoji, title, desc in features:
        st.markdown(
            f"""
            <div class="feature-card">
                <h4>{emoji} {title}</h4>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Language toggle
    st.markdown("### 🌐 Language Support")
    st.markdown("**Ask in Bengali or English!**")

    # Quick stats
    st.markdown("### 📊 Chat Stats")
    message_count = len(st.session_state.messages)
    st.metric("Messages", message_count)

    if message_count > 0:
        user_messages = len(
            [m for m in st.session_state.messages if m["role"] == "user"]
        )
        st.metric("Your Questions", user_messages)

    st.markdown("---")

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.welcome_shown = False
            st.rerun()

    with col2:
        if st.button("🔄 New Chat", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.welcome_shown = False
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8rem;">
            <p>Made with ❤️ for Bangladesh</p>
            <p>Powered by AI & Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
