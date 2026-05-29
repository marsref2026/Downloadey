import streamlit as st
import streamlit.components.v1 as components
import yt_dlp
import os

# --- UI CONFIG ---
st.set_page_config(page_title="Downloadey", page_icon="📥")

def inject_ads():
    ad_code = """<div style="text-align:center; margin: 10px 0;">
        <p style="color: grey; font-size: 10px;">ADVERTISEMENT</p>
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR-ID" crossorigin="anonymous"></script>
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-YOUR-ID" data-ad-slot="YOUR-SLOT" data-ad-format="auto"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script></div>"""
    components.html(ad_code, height=120)

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
            # FLEXIBLE OPTIONS
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'cookiefile': 'cookies.txt',
                'quiet': True,
                'no_warnings': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
                # This says: "Get the best video and best audio and combine them, 
                # OR get the best single file if that fails."
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'

            with st.spinner('🚀 Processing media streams...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # Ensure filename is correct if it was merged into mp4
                    if "MP4" in choice and not filename.endswith(".mp4"):
                        base = os.path.splitext(filename)[0]
                        if os.path.exists(base + ".mp4"):
                            filename = base + ".mp4"
                    
                    if "MP3" in choice:
                        filename = os.path.splitext(filename)[0] + ".mp3"

                with open(filename, "rb") as f:
                    st.success("✅ DOWNLOAD READY!")
                    st.download_button(
                        label="⬇️ SAVE TO DEVICE",
                        data=f,
                        file_name=os.path.basename(filename)
                    )
                os.remove(filename)

        except Exception as e:
            st.error(f"SYSTEM ERROR: {str(e)[:250]}")
    else:
        st.warning("Please paste a URL")

st.markdown('</div>', unsafe_allow_html=True)
