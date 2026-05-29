import streamlit as st
import streamlit.components.v1 as components
import yt_dlp
import os

# --- UI CONFIG ---
st.set_page_config(page_title="Downloadey", page_icon="📥")

def inject_ads():
    ad_code = """<div style="text-align:center; margin: 10px 0;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR-ID" crossorigin="anonymous"></script>
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-YOUR-ID" data-ad-slot="YOUR-SLOT" data-ad-format="auto"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script></div>"""
    components.html(ad_code, height=100)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url('https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?q=80&w=1974&auto=format&fit=crop');
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .main-box { background-color: rgba(0, 0, 0, 0.6); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); text-align: center; }
    .stButton > button {
        width: 100%; background-color: #FFFFFF !important; color: #000000 !important;
        font-weight: 900 !important; border-radius: 12px !important; height: 55px; transition: 0.3s;
    }
    .stButton > button:hover { background-color: #808080 !important; color: #000000 !important; }
    h1, p, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.title("DOWNLOADEY")
inject_ads()

url = st.text_input("", placeholder="Paste Link (IG, FB, YT)...")
choice = st.radio("FORMAT", ["MP4 (VIDEO)", "MP3 (AUDIO)"], horizontal=True)

if st.button("DOWNLOAD NOW"):
    if url:
        try:
            # 1. THE STEALTH CONFIGURATION
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'cookiefile': 'cookies.txt',
                'quiet': True,
                'no_warnings': True,
                # Impersonate Android client to bypass 403 Forbidden
                'extractor_args': {'youtube': {'player_client': ['android']}},
                'http_headers': {
                    'User-Agent': 'com.google.android.youtube/19.29.37 (Linux; U; Android 11; en_US) gzip',
                },
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
                # Force standard mp4 if possible to reduce bandwidth and errors
                ydl_opts['format'] = 'best[ext=mp4]/best'

            with st.spinner('🚀 Bypassing security...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # Fix extension if it was converted
                    base = os.path.splitext(filename)[0]
                    if "MP3" in choice:
                        filename = base + ".mp3"
                    elif not filename.endswith(".mp4") and os.path.exists(base + ".mp4"):
                        filename = base + ".mp4"

                with open(filename, "rb") as f:
                    st.success("✅ BYPASSED! DOWNLOAD READY.")
                    st.download_button(
                        label="⬇️ SAVE TO DEVICE",
                        data=f,
                        file_name=os.path.basename(filename)
                    )
                os.remove(filename)

        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg:
                st.error("SYSTEM ERROR: YouTube is blocking this server's IP. Try refreshing your cookies.txt or try an Instagram/Facebook link instead.")
            else:
                st.error(f"DOWNLOAD ERROR: {error_msg[:250]}")
    else:
        st.warning("Please paste a URL")

st.markdown('</div>', unsafe_allow_html=True)
