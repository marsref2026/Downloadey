import streamlit as st
import streamlit.components.v1 as components
import yt_dlp
import os

# --- 1. PROFESSIONAL CONFIG & BRANDING REMOVAL ---
st.set_page_config(
    page_title="Downloadey", 
    page_icon="📥",
    layout="centered"
)

# This CSS hides the Streamlit Menu, Footer, and Header to make it look professional
st.markdown("""
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .st-emotion-cache-18ni7ap {padding-top: 0rem;}

    /* Full Page Background with 70% Black Overlay */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url('https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?q=80&w=1974&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Main Modern Container */
    .main-box {
        background-color: rgba(0, 0, 0, 0.65);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 15px !important;
    }

    /* THE BUTTON: Normal White State */
    .stButton > button {
        width: 100%;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        border: none !important;
        height: 55px;
        transition: 0.3s all ease;
        text-transform: uppercase;
    }

    /* THE BUTTON: Grey Hover State with Black Text */
    .stButton > button:hover {
        background-color: #808080 !important; /* Grey background */
        color: #000000 !important;           /* Black text */
        transform: scale(1.01);
    }

    h1, p, label { color: white !important; font-family: 'Helvetica Neue', sans-serif; }
    .stRadio label { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def inject_ads():
    # Replace 'YOUR-AD-CLIENT-ID' and 'YOUR-AD-SLOT' when you have your AdSense info
    ad_code = """
    <div style="text-align:center; margin: 15px 0;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR-ID" crossorigin="anonymous"></script>
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-YOUR-ID" data-ad-slot="YOUR-SLOT" data-ad-format="auto"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    </div>
    """
    components.html(ad_code, height=120)

# --- 2. INTERFACE ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("DOWNLOADEY")
st.write("Professional Downloader for IG, FB, and Twitter (X)")

inject_ads() # Top Ad Slot

url = st.text_input("", placeholder="Paste Video Link Here...")
choice = st.radio("SELECT FORMAT", ["MP4 (VIDEO)", "MP3 (AUDIO)"], horizontal=True)

if st.button("DOWNLOAD NOW"):
    if url:
        st.info("💰 AD: Processing media... please wait.")
        try:
            # Optimal settings for Facebook, Instagram, and Twitter
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
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
                ydl_opts['format'] = 'bestvideo+bestaudio/best'

            with st.spinner('⚡ Fetching high-quality media...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # Fix extension for merged files
                    base = os.path.splitext(filename)[0]
                    if "MP3" in choice:
                        filename = base + ".mp3"
                    elif not os.path.exists(filename):
                        if os.path.exists(base + ".mp4"):
                            filename = base + ".mp4"
                        elif os.path.exists(base + ".mkv"):
                            filename = base + ".mkv"

                with open(filename, "rb") as f:
                    st.success("✅ READY!")
                    st.download_button(
                        label="🔥 CLICK TO SAVE TO DEVICE",
                        data=f,
                        file_name=os.path.basename(filename)
                    )
                # Remove file from server to save space
                os.remove(filename)
                
            inject_ads() # Bottom Ad Slot

        except Exception as e:
            st.error(f"DOWNLOAD ERROR: {str(e)[:250]}")
    else:
        st.warning("PLEASE PASTE A URL FIRST")

st.markdown('</div>', unsafe_allow_html=True)
