import streamlit as st
import streamlit.components.v1 as components
import yt_dlp
import os

# --- 1. CONFIG & ADS LOGIC ---
st.set_page_config(page_title="Downloadey", page_icon="📥")

def inject_ads():
    # Replace 'YOUR-AD-CLIENT-ID' with your real Google AdSense ID later
    ad_code = """
    <div style="text-align:center; margin: 10px 0;">
        <p style="color: grey; font-size: 10px;">ADVERTISEMENT</p>
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR-AD-CLIENT-ID" crossorigin="anonymous"></script>
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-YOUR-AD-CLIENT-ID" data-ad-slot="YOUR-AD-SLOT" data-ad-format="auto"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    </div>
    """
    components.html(ad_code, height=120)

# --- 2. MODERN UI WITH OVERLAY & HOVER BUTTON ---
st.markdown("""
    <style>
    /* Background with 70% Black Overlay */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url('https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?q=80&w=1974&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Main Container */
    .main-box {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }

    /* Input Field */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 15px !important;
    }

    /* THE BUTTON: Normal State (White) */
    .stButton > button {
        width: 100%;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        border: none !important;
        height: 55px;
        transition: 0.3s all ease;
    }

    /* THE BUTTON: Hover State (Grey Background, Black Text) */
    .stButton > button:hover {
        background-color: #808080 !important; /* Grey */
        color: #000000 !important;           /* Black Text */
        transform: scale(1.01);
    }

    h1, p, label { color: white !important; }
    .stRadio label { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFACE ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("DOWNLOADEY")
st.write("Fast Downloader for IG, FB, and YouTube")

inject_ads() # Top Ad

url = st.text_input("", placeholder="PASTE LINK HERE...")
choice = st.radio("CHOOSE FORMAT", ["MP4 (VIDEO)", "MP3 (AUDIO)"], horizontal=True)

if st.button("DOWNLOAD NOW"):
    if url:
        st.info("💰 AD: Download starting... (Please wait)")
        try:
            # ydl_opts using current directory to avoid server permission errors
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
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

            with st.spinner('⚡ PROCESSING MEDIA...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extraction
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    if "MP3" in choice:
                        filename = os.path.splitext(filename)[0] + ".mp3"

                with open(filename, "rb") as f:
                    st.success("✅ READY!")
                    st.download_button(
                        label="🔥 CLICK TO SAVE TO DEVICE",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="video/mp4" if "MP4" in choice else "audio/mpeg"
                    )
            inject_ads() # Post-Download Ad

        except Exception as e:
            # Showing actual error to debug "Private/Invalid" issue
            st.error(f"SYSTEM ERROR: {e}")
    else:
        st.warning("PLEASE PASTE A URL FIRST")

st.markdown('</div>', unsafe_allow_html=True)
