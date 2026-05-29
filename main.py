import streamlit as st
import yt_dlp
import os

# --- 1. MODERN DESIGN CONFIGURATION ---
st.set_page_config(page_title="Downloadey", page_icon="📥")

# Custom CSS for Background and 70% Opacity Overlay
st.markdown("""
    <style>
    /* Full Page Background with Image and 70% Black Overlay */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url('https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?q=80&w=1974&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Main Container Styling */
    .main-box {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 15px !important;
        font-size: 16px;
    }

    /* Button Styling */
    .stButton > button {
        width: 100%;
        background: white !important;
        color: black !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 12px !important;
        border: none !important;
        height: 50px;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background: #dddddd !important;
        transform: scale(1.02);
    }

    /* Radio Buttons / Choice Styling */
    .stRadio label {
        color: white !important;
        font-weight: bold;
    }

    /* Titles */
    h1 {
        color: white !important;
        font-weight: 800 !important;
        text-align: center;
        letter-spacing: -1px;
    }
    
    p {
        color: rgba(255, 255, 255, 0.7) !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE APP INTERFACE ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("DOWNLOADEY")
st.write("The ultimate downloader for IG Reels, FB Videos, and YT Shorts.")

# Spacer
st.write("")

url = st.text_input("", placeholder="PASTE LINK HERE (FB, IG, YT)...")

st.write("")
choice = st.radio("CHOOSE FORMAT", ["MP4 (VIDEO)", "MP3 (AUDIO)"], horizontal=True)

st.write("")

if st.button("DOWNLOAD NOW"):
    if url:
        # GOOGLE ADS PLACEHOLDER (Monetization Trigger)
        st.info("💰 ADVERTISEMENT: Checking content... (Ad Loading)")
        
        try:
            # Temporary folder for downloads
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            ydl_opts = {
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': True,
            }

            if "MP3" in choice:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts['format'] = 'best'

            with st.spinner('⚡ PROCESSING...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    if "MP3" in choice:
                        filename = filename.rsplit('.', 1)[0] + ".mp3"

                with open(filename, "rb") as f:
                    st.success("SUCCESS! DOWNLOAD READY")
                    st.download_button(
                        label="⬇️ SAVE TO YOUR DEVICE",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="video/mp4" if "MP4" in choice else "audio/mpeg"
                    )
        except Exception as e:
            st.error("ERROR: Link is private or invalid.")
    else:
        st.warning("PLEASE PASTE A URL FIRST")

st.markdown('</div>', unsafe_allow_html=True)