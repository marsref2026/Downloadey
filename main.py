import streamlit as st
import streamlit.components.v1 as components
import yt_dlp
import os

# --- UI & ADS ---
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
            # SAVE FILENAME TEMPLATE
            out_tmpl = '%(title)s.%(ext)s'
            
            # UPDATED OPTIONS FOR MAXIMUM COMPATIBILITY
            ydl_opts = {
                'outtmpl': out_tmpl,
                'cookiefile': 'cookies.txt',
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
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
                # This string is the magic fix:
                # 1. Try to get best video + best audio merged into MP4
                # 2. If that fails, get the best single file that is ALREADY an MP4
                # 3. If that fails, just get the 'best' of anything available.
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

            with st.spinner('🚀 Analyzing and grabbing media...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    # We use get() because merged files might have different names than expected
                    filename = ydl.prepare_filename(info)
                    
                    # Fix for potential extension changes during merging
                    base, ext = os.path.splitext(filename)
                    if "MP4" in choice and not os.path.exists(filename):
                        if os.path.exists(base + ".mp4"):
                            filename = base + ".mp4"
                        elif os.path.exists(base + ".mkv"): # Sometimes yt-dlp merges to mkv
                            filename = base + ".mkv"
                    
                    if "MP3" in choice:
                        filename = base + ".mp3"

                with open(filename, "rb") as f:
                    st.success("✅ SUCCESS!")
                    st.download_button(
                        label="⬇️ CLICK TO SAVE TO DEVICE",
                        data=f,
                        file_name=os.path.basename(filename)
                    )
                
                # Cleanup to keep server fast
                os.remove(filename)

        except Exception as e:
            st.error(f"DOWNLOAD ERROR: {str(e)[:250]}")
    else:
        st.warning("Please paste a URL")

st.markdown('</div>', unsafe_allow_html=True)
