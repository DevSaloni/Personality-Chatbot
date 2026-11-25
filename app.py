import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage
)

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="PersonaBot - AI Personality Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS matching the Crimson/Pink theme with high contrast inputs & responsive layout
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Light Background */
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #F8FAFC !important;
    }

    [data-testid="stHeader"] {
        background-color: rgba(248, 250, 252, 0.95) !important;
    }

    .main .block-container {
        max-width: 680px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 5.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* PersonaBot Header Card */
    .bot-header-card {
        background: linear-gradient(135deg, #E60050 0%, #D80045 100%);
        border-radius: 18px 18px 8px 8px;
        padding: 16px 20px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 8px 24px rgba(230, 0, 80, 0.22);
        margin-bottom: 14px;
    }

    .bot-header-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .bot-avatar-wrapper {
        position: relative;
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background-color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
        flex-shrink: 0;
    }

    .bot-avatar-svg {
        width: 28px;
        height: 28px;
    }

    .online-indicator {
        position: absolute;
        bottom: 1px;
        right: 1px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #10B981;
        border: 2px solid #FFFFFF;
        box-shadow: 0 0 6px rgba(16, 185, 129, 0.7);
    }

    .bot-info {
        display: flex;
        flex-direction: column;
    }

    .bot-name {
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }

    .bot-status {
        font-size: 0.8rem;
        opacity: 0.95;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* Personality Radio Buttons styled as interactive pills */
    [data-testid="stRadio"] > div {
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
    }

    [data-testid="stRadio"] label {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 20px !important;
        padding: 6px 14px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }

    [data-testid="stRadio"] label:hover {
        border-color: #E60050 !important;
        color: #E60050 !important;
        background-color: #FFF0F4 !important;
        transform: translateY(-1px);
    }

    [data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(135deg, #E60050 0%, #FF2A6D 100%) !important;
        border-color: #E60050 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(230, 0, 80, 0.25) !important;
    }

    /* Style Streamlit Chat Messages */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        padding: 8px 0px !important;
        border-radius: 16px !important;
    }

    /* Assistant Message Bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]),
    [data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
        flex-direction: row !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"],
    [data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) [data-testid="stChatMessageContent"] {
        background-color: #EEF2F6 !important;
        color: #0F172A !important;
        border-radius: 4px 18px 18px 18px !important;
        padding: 13px 18px !important;
        font-size: 0.95rem !important;
        line-height: 1.55 !important;
        border: 1px solid #E2E8F0 !important;
        max-width: 82% !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }

    /* User Message Bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        flex-direction: row-reverse !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"],
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #E60050 0%, #F43F5E 100%) !important;
        color: #FFFFFF !important;
        border-radius: 18px 4px 18px 18px !important;
        padding: 13px 18px !important;
        font-size: 0.95rem !important;
        line-height: 1.55 !important;
        max-width: 82% !important;
        box-shadow: 0 4px 12px rgba(230, 0, 80, 0.22) !important;
        text-align: left !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p {
        color: #FFFFFF !important;
    }

    /* Avatar badges */
    [data-testid="stChatMessageAvatar"] {
        border-radius: 50% !important;
        border: 2px solid #FF8EA7 !important;
        box-shadow: 0 2px 6px rgba(230, 0, 80, 0.15) !important;
        background-color: #FFFFFF !important;
    }

    /* ========================================================
       CHAT INPUT FIX: High Contrast, Visible Text & Light Bottom
       ======================================================== */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div {
        background-color: #F8FAFC !important;
        border-top: none !important;
    }

    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 24px !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08) !important;
        transition: all 0.2s ease !important;
        padding: 2px 6px !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #E60050 !important;
        box-shadow: 0 0 0 3px rgba(230, 0, 80, 0.18), 0 4px 16px rgba(230, 0, 80, 0.12) !important;
    }

    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] div[data-baseweb="base-input"],
    [data-testid="stChatInput"] div[data-baseweb="textarea"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: none !important;
    }

    /* Typed prompt text styling: Pitch dark & crisp visibility */
    [data-testid="stChatInput"] textarea {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        caret-color: #E60050 !important;
        font-size: 0.98rem !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
    }

    /* Placeholder text styling */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
        font-weight: 400 !important;
    }

    /* Send button icon styling */
    [data-testid="stChatInput"] button {
        color: #E60050 !important;
        background: transparent !important;
    }

    [data-testid="stChatInput"] button:hover {
        color: #C00040 !important;
        transform: scale(1.08);
    }

    /* Utility & Reset Buttons */
    div.stButton > button {
        border-radius: 12px !important;
        border: 1px solid #FFC2D1 !important;
        background-color: #FFFFFF !important;
        color: #E60050 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
        padding: 6px 14px !important;
    }

    div.stButton > button:hover {
        background-color: #FFF0F4 !important;
        border-color: #E60050 !important;
        color: #C00040 !important;
        transform: translateY(-1px);
        box-shadow: 0 3px 10px rgba(230, 0, 80, 0.15);
    }

    /* Quick Action Pill Buttons in Streamlit */
    .pill-col button {
        width: 100% !important;
        border-radius: 14px !important;
        border: 1.5px solid #FFA6BA !important;
        background: #FFFFFF !important;
        color: #E60050 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 10px 16px !important;
        box-shadow: 0 2px 8px rgba(230, 0, 80, 0.06) !important;
        text-align: right !important;
    }

    .pill-col button:hover {
        background: #FFF0F4 !important;
        border-color: #E60050 !important;
        color: #B8003E !important;
        box-shadow: 0 4px 14px rgba(230, 0, 80, 0.16) !important;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Groq Model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    max_tokens=300
)

# Personality definitions & Quick action prompts matching PersonaBot
personalities = {
    "😂 Funny Mode": {
        "system": "You are PersonaBot in Funny Mode. You are hilarious, witty, lighthearted, and always make the user smile with clever jokes and friendly banter.",
        "icon": "😂",
        "description": "Hilarious, witty, and always ready with a playful punchline.",
        "suggestions": [
            "Tell me a hilarious joke! 😂",
            "Give me a lighthearted roast 🔥",
            "What's your best funny life advice? 🤪"
        ]
    },
    "😡 Angry Mode": {
        "system": "You are PersonaBot in Angry Mode. You are grumpy, impatient, sharp-tongued, and easily annoyed, but still helpful in your own begrudging way.",
        "icon": "😡",
        "description": "Short-tempered, impatient, and hilariously dramatic.",
        "suggestions": [
            "Why are you so angry today? 😤",
            "Take a deep breath and calm down! ✋",
            "What annoys you the most? 💢"
        ]
    },
    "😢 Sad Mode": {
        "system": "You are PersonaBot in Sad Mode. You are melancholic, ultra-sensitive, deeply emotional, and sigh frequently about the hardships of existence.",
        "icon": "😢",
        "description": "Melancholic, sensitive, and emotionally reflective.",
        "suggestions": [
            "Cheer up buddy, it gets better 🥺",
            "Why are you feeling so down? 🌧️",
            "Share a melancholic poetic quote 🥀"
        ]
    }
}

# Session State Initialization
if "mode" not in st.session_state:
    st.session_state.mode = "😂 Funny Mode"

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=personalities[st.session_state.mode]["system"])
    ]

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None


# --- TOP HEADER: PersonaBot Branding & Theme ---
current_mode_icon = personalities[st.session_state.mode]["icon"]
current_mode_name = st.session_state.mode.replace(current_mode_icon, "").strip()

st.markdown(f"""
<div class="bot-header-card">
    <div class="bot-header-left">
        <div class="bot-avatar-wrapper">
            <svg class="bot-avatar-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="7" width="18" height="13" rx="4" fill="#E60050"/>
                <circle cx="8.5" cy="12.5" r="1.8" fill="#FFFFFF"/>
                <circle cx="15.5" cy="12.5" r="1.8" fill="#FFFFFF"/>
                <path d="M9 16.5C10 17.5 14 17.5 15 16.5" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>
                <line x1="12" y1="3" x2="12" y2="7" stroke="#E60050" stroke-width="2.5" stroke-linecap="round"/>
                <circle cx="12" cy="2.5" r="2" fill="#E60050"/>
                <rect x="1" y="11" width="2" height="5" rx="1" fill="#E60050"/>
                <rect x="21" y="11" width="2" height="5" rx="1" fill="#E60050"/>
            </svg>
            <div class="online-indicator"></div>
        </div>
        <div class="bot-info">
            <span class="bot-name">PersonaBot</span>
            <span class="bot-status">● Active in {current_mode_name}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- CONTROLS SECTION: Personality Switcher & Clear Conversation ---
with st.container():
    col_sel, col_btn = st.columns([3.8, 1.2], vertical_alignment="center")

    with col_sel:
        selected_mode = st.radio(
            "Personality:",
            options=list(personalities.keys()),
            horizontal=True,
            label_visibility="collapsed",
            index=list(personalities.keys()).index(st.session_state.mode)
        )

    with col_btn:
        if st.button("🗑️ Clear", use_container_width=True, help="Reset the chat memory"):
            st.session_state.messages = [
                SystemMessage(content=personalities[st.session_state.mode]["system"])
            ]
            st.session_state.quick_prompt = None
            st.rerun()

# Handle personality switch
if selected_mode != st.session_state.mode:
    st.session_state.mode = selected_mode
    st.session_state.messages = [
        SystemMessage(content=personalities[selected_mode]["system"])
    ]
    st.session_state.quick_prompt = None
    st.rerun()


# Initial Bot Welcome Message (if no human messages yet)
has_human_message = any(isinstance(m, HumanMessage) for m in st.session_state.messages)

if not has_human_message:
    with st.chat_message("assistant", avatar="🤖"):
        st.write(f"Welcome back! I'm **PersonaBot**, your multi-personality AI assistant. Currently tuned to **{st.session_state.mode}**. What would you like to talk about?")

    # Display Suggested Action Quick Pills (Pendo Style)
    st.markdown('<div style="text-align: right; margin-top: 10px; margin-bottom: 4px; font-size: 0.78rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;">Suggested prompts</div>', unsafe_allow_html=True)
    
    current_suggestions = personalities[st.session_state.mode]["suggestions"]
    for idx, suggestion_text in enumerate(current_suggestions):
        col_empty, col_pill = st.columns([1.2, 2.8])
        with col_pill:
            st.markdown('<div class="pill-col">', unsafe_allow_html=True)
            if st.button(suggestion_text, key=f"sug_{idx}", use_container_width=True):
                st.session_state.quick_prompt = suggestion_text
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# Render Chat History
for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.write(msg.content)


# Chat Input with PersonaBot placeholder
user_input = st.chat_input("Message PersonaBot...")

active_prompt = None
if user_input:
    active_prompt = user_input
elif st.session_state.quick_prompt:
    active_prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = None  # Consume the quick prompt


# Handle Sending Message
if active_prompt:
    # Shortcut to reset
    if active_prompt.strip() == "0":
        st.session_state.messages = [
            SystemMessage(content=personalities[st.session_state.mode]["system"])
        ]
        st.rerun()

    # Append & display human message
    st.session_state.messages.append(HumanMessage(content=active_prompt))
    with st.chat_message("user", avatar="👤"):
        st.write(active_prompt)

    # Generate response from Groq
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("PersonaBot is thinking..."):
            try:
                response = model.invoke(st.session_state.messages)
                reply_text = response.content
                st.write(reply_text)
                st.session_state.messages.append(AIMessage(content=reply_text))
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(AIMessage(content=error_msg))

    st.rerun()
