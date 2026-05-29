import streamlit as st
import streamlit.components.v1 as components
import yt_dlp
import os

# --- 1. CONFIG & ADS ---
st.set_page_config(page_title="Downloadey", page_icon="📥")

def inject_ads():
    ad_code = """
    <div style="text-align:center; margin: 10px 0;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR-AD-CLIENT-ID" crossorigin="anonymous"></script>
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-YOUR-AD-CLIENT-ID" data-ad-slot="YOUR-AD-SLOT" data-ad-format="auto"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    </div>
    """
    components.html(ad_code, height=100)

# --- 2. UI DESIGN ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url('https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?q=80&w=1974&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main-box {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    .stButton > button {
        width: 100%;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 55px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #808080 !important;
        color: #000000 !important;
    }
    h1, p, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. APP LOGIC ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.title("DOWNLOADEY")
st.write("Professional Media Downloader")

inject_ads()

url = st.text_input("", placeholder="Paste Link (IG, FB, YT)...")
choice = st.radio("FORMAT", ["MP4 (VIDEO)", "MP3 (AUDIO)"], horizontal=True)

if st.button("DOWNLOAD NOW"):
    if url:
        try:
            # STEALTH OPTIONS TO PREVENT BLOCKS
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'referer': 'https://www.google.com/',
                'nocheckcertificate': True,
                'add_header': ['Accept-Language: en-US,en;q=0.9'],
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

            with st.spinner('⚡ Connecting to server...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    if "MP3" in choice:
                        filename = os.path.splitext(filename)[0] + ".mp3"

                with open(filename, "rb") as f:
                    st.success("DOWNLOAD READY!")
                    st.download_button(
                        label="⬇️ SAVE FILE",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="video/mp4" if "MP4" in choice else "audio/mpeg"
                    )
                
                # Auto-delete from server after user gets it to save space
                os.remove(filename)

        except Exception as e:
            # THIS WILL TELL US THE REAL PROBLEM
            st.error(f"DOWLOAD FAILED: {str(e)[:200]}")
    else:
        st.warning("Please paste a URL")

st.markdown('</div>', unsafe_allow_html=True)
