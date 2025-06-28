import streamlit as st
import requests
import datetime

# CONFIG - Replace with your bot + channel info
BOT_TOKEN = "8058471433:AAE68N4V0tqTryeu3yjKohRPchoYYen-AU0"
CHANNEL_ID = "-1002835921912"  # like -1001234567890

# Streamlit UI
st.set_page_config(page_title="Telegram Drive", layout="centered")
st.title("🚀 Telegram Drive - Upload Files to Your Channel")

with st.form("upload_form"):
    file = st.file_uploader("📁 Choose a file", type=None)
    folder = st.text_input("📂 Folder Name (optional)", "")
    caption = st.text_area("📝 Caption (optional)", "")
    submitted = st.form_submit_button("Upload to Telegram")

if submitted and file is not None:
    file_bytes = file.read()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_caption = f"{caption}\n\n📁 Folder: {folder}\n🕒 Uploaded: {now}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    response = requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "caption": final_caption
    }, files={"document": (file.name, file_bytes)})

    if response.status_code == 200:
        st.success("✅ File uploaded successfully!")
        msg_id = response.json()["result"]["message_id"]
        public_link = f"https://t.me/c/{CHANNEL_ID[4:]}/{msg_id}" if CHANNEL_ID.startswith("-100") else "Link unavailable"
        st.markdown(f"🔗 [View on Telegram]({public_link})")
    else:
        st.error("❌ Upload failed. Please check bot token or channel ID.")
