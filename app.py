import streamlit as st
import requests
import datetime
import gspread
from google.oauth2.service_account import Credentials

# ======================= CONFIG ============================
BOT_TOKEN = "8058471433:AAE68N4V0tqTryeu3yjKohRPchoYYen-AU0"
CHANNEL_ID = "-1002835921912"  # <-- paste your real channel ID here
SHEET_NAME = "TelegramDriveData"  # your Google Sheet name

# Google Sheets auth
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_info({
    "type": "service_account",
    "project_id": "flash-medley-464305-h2",
    "private_key_id": "60ac6771856fcf9c5ccd99f44234d06e4b0d093a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDi+U9R8UqRLpk5...\n-----END PRIVATE KEY-----\n",
    "client_email": "streamlit-telegram-bot@flash-medley-464305-h2.iam.gserviceaccount.com",
    "client_id": "108785338248258713915",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/streamlit-telegram-bot%40flash-medley-464305-h2.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}, scopes=SCOPE)

gc = gspread.authorize(CREDS)
sheet = gc.open(SHEET_NAME).sheet1

# ======================= UI ============================
st.set_page_config(page_title="Telegram Drive", layout="centered")
st.title("🚀 Telegram Drive - Upload to Telegram + Save to Sheet")

with st.form("upload_form"):
    file = st.file_uploader("📁 Choose a file")
    folder = st.text_input("📂 Folder Name (optional)")
    caption = st.text_area("📝 Caption (optional)")
    submit = st.form_submit_button("Upload")

if submit and file:
    file_bytes = file.read()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_caption = f"{caption}\n\n📁 Folder: {folder}\n🕒 {timestamp}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    r = requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "caption": final_caption
    }, files={"document": (file.name, file_bytes)})

    if r.status_code == 200:
        st.success("✅ Uploaded to Telegram!")
        msg_id = r.json()["result"]["message_id"]
        message_link = f"https://t.me/c/{CHANNEL_ID[4:]}/{msg_id}"

        # Save to Google Sheet
        sheet.append_row([file.name, folder, caption, timestamp, message_link])
        st.markdown(f"🔗 [View File in Telegram]({message_link})")
    else:
        st.error("❌ Upload failed. Check BOT_TOKEN or CHANNEL_ID.")

# ======================= SEARCH ============================
st.markdown("---")
st.subheader("🔍 Search Your Files")

search_query = st.text_input("Search by file name or folder:")
if search_query:
    data = sheet.get_all_records()
    results = [row for row in data if search_query.lower() in row['File Name'].lower() or search_query.lower() in row['Folder'].lower()]

    if results:
        for row in results:
            st.markdown(f"**📁 Folder:** {row['Folder']}  \n**📄 File:** {row['File Name']}  \n📝 {row['Caption']}  \n🕒 {row['Upload Time']}  \n🔗 [Open File]({row['Message Link']})")
            st.markdown("---")
    else:
        st.warning("No matching files found.")
