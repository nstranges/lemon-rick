import streamlit as st
import os
# Import the audio processing function from your lemon backend file
from lemon import talk

# 1. Page Configuration
st.set_page_config(
    page_title="Lemon Rick",
    page_icon="🍋",
    layout="centered" # Brought back to centered for a cozy, tight cottage feel
)

# 2. Lavender Lemonade Aesthetic via Custom CSS
st.markdown("""
    <style>
    /* Main App Background - Warm Cottage Sun & Lavender Haze */
    .stApp {
        background: linear-gradient(180deg, #FFFDF6 0%, #F3E5F5 100%);
    }
    
    .block-container {
        padding-top: 3rem;
        max-width: 700px;
    }
    
    /* Title Typography Styling */
    h1 {
        color: #6A1B9A !important; /* Deep Lavender Purple */
        font-family: 'Georgia', serif;
        font-weight: 500;
        margin-bottom: 0px;
    }
    
    /* Customizing the chat input box to look soft and welcoming */
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 2px solid #FFF59D !important; /* Soft Pastel Lemon */
        box-shadow: 0 4px 15px rgba(106, 27, 154, 0.05) !important;
        background-color: white !important;
    }
    
    /* --- CUSTOM CHAT BUBBLE CARDS --- */
    div[data-testid="stChatMessage"] {
        border-radius: 20px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.02);
        border: none;
    }
    
    /* User bubbles (The Visitor / Gentle Cream Sun) */
    div[data-testid="stChatMessageUser"] {
        background-color: #FFFDE7 !important; 
        border-right: 4px solid #FFF59D;
    }
    
    /* Assistant bubbles (Lemon Rick / Lavender Breeze) */
    div[data-testid="stChatMessageAssistant"] {
        background-color: #F3E5F5 !important; 
        border-left: 4px solid #BA68C8;
    }
    
    /* Styled container for the thinking widget */
    div[data-testid="stStatusWidget"] {
        border-radius: 12px;
        border: none;
        background-color: #F3E5F5 !important;
        font-family: 'Georgia', serif;
        font-style: italic;
    }
    
    /* Smooth, relaxed formatting for the transcription text */
    .transcription-text {
        font-family: 'Georgia', serif;
        font-size: 1.15rem;
        color: #4A148C;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Main Cottage Header Area
st.title("🍋 Lemon Rick")
st.markdown("<p style='color: #7B1FA2; font-family: Georgia, serif; font-style: italic; font-size: 1.1rem; margin-top:-5px;'>Homemade lavender lemonade. Freshly squeezed, completely unhurried.</p>", unsafe_allow_html=True)
st.divider()

# 4. Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Existing Chat History
for message in st.session_state.messages:
    avatar = "✨" if message["role"] == "user" else "🍋"
    with st.chat_message(message["role"], avatar=avatar):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            # Display text transcription and audio player together
            st.markdown(f"<div class='transcription-text'>{message['transcription']}</div>", unsafe_allow_html=True)
            st.audio(message["audio_bytes"], format="audio/mp3", autoplay=False)

# 6. Text Input Widget
if user_prompt := st.chat_input("Pull up a chair and pour your thoughts here..."):
    
    # 1. Append and render User Text prompt instantly
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="✨"):
        st.markdown(user_prompt)
        
    # 2. Call Custom Backend Model inside Assistant UI card
    with st.chat_message("assistant", avatar="🍋"):
        with st.status("Stirring up an answer...", expanded=True) as status:
            
            # Execute backend logic
            raw_backend_response = talk(user_prompt)
            
            # Transcription guard check
            if raw_backend_response:
                transcription = str(raw_backend_response)
            else:
                transcription = "*(The glass clinks softly, but the transcription came back empty...)*"
            
            status.update(label="Pouring a glass...", state="complete", expanded=False)
        
        # Display the crisp transcription text right above the audio player
        st.markdown(f"<div class='transcription-text'>{transcription}</div>", unsafe_allow_html=True)
            
        # Read the newly generated file bytes
        if os.path.exists("out.mp3"):
            with open("out.mp3", "rb") as f:
                ai_audio_bytes = f.read()
            
            # Render player and trigger autoplay seamlessly
            st.audio(ai_audio_bytes, format="audio/mp3", autoplay=True)
            
            # 3. Append Assistant response to history log
            st.session_state.messages.append({
                "role": "assistant", 
                "transcription": transcription, 
                "audio_bytes": ai_audio_bytes
            })
        else:
            st.error("Looks like the pitcher spilled. out.mp3 wasn't found.")