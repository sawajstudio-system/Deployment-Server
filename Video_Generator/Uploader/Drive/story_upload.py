# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Uploader/Drive/story_upload.py
# 🎯 PURPOSE: तैयार वीडियो को Google Drive में अपलोड करना और लिंक निकालना
# ══════════════════════════════════════════════════════════════════════════════

import os
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(file_path, custom_name=None):
    """
    यह फंक्शन वीडियो को Google Drive में अपलोड करता है।
    - OAuth2 (Refresh Token) का इस्तेमाल करके लॉगिन करता है।
    - वीडियो को खास फोल्डर (GDRIVE_F_STORY_ID) में डालता है।
    - वीडियो को Public बनाता है ताकि लिंक से कोई भी देख सके।
    """
    print(f"☁️ [Uploader] Starting upload for: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ [Uploader] File not found: {file_path}")
        return None

    # 1. Environment Variables (GitHub Secrets) से क्रेडेंशियल्स लोड करना
    client_id = os.getenv("GDRIVE_CLIENT_ID")
    client_secret = os.getenv("GDRIVE_CLIENT_SECRET")
    refresh_token = os.getenv("GDRIVE_REFRESH_TOKEN")
    folder_id = os.getenv("GDRIVE_F_STORY_ID") # जहाँ वीडियो सेव होगी

    if not all([client_id, client_secret, refresh_token]):
        print("❌ [Uploader] Missing Google Drive Credentials in environment variables.")
        return None

    # 2. Google Drive API के लिए Authenticate करना
    try:
        creds = Credentials(
            None, # Token अभी नहीं है, हम refresh_token का इस्तेमाल करेंगे
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            token_uri="https://oauth2.googleapis.com/token"
        )
        service = build('drive', 'v3', credentials=creds, cache_discovery=False)
        print("✅ [Uploader] Successfully authenticated with Google Drive.")
    except Exception as e:
        print(f"❌ [Uploader] Authentication Failed: {e}")
        return None

    # 3. फाइल का नाम तय करना
    if custom_name:
        file_name = custom_name
    else:
        # अगर नाम नहीं दिया है, तो टाइमस्टैम्प के साथ सेव करो
        file_name = f"Story_Video_{int(time.time())}.mp4"

    # 4. अपलोड का रिक्वेस्ट तैयार करना
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
        print(f"📁 [Uploader] Target Folder ID: {folder_id}")
    else:
        print("⚠️ [Uploader] GDRIVE_F_STORY_ID not set. Uploading to Drive Root.")

    media = MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)

    # 5. अपलोड शुरू करना
    try:
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"⏳ [Uploader] Uploading {file_name} (Size: {file_size_mb:.2f} MB)...")
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        file_id = file.get('id')
        print(f"✅ [Uploader] Upload Complete! File ID: {file_id}")

        # 6. फाइल को Public बनाना (ताकि हर किसी के पास लिंक खुले)
        try:
            service.permissions().create(
                fileId=file_id,
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()
            print("🔓 [Uploader] File permissions set to public.")
        except Exception as e:
            print(f"⚠️ [Uploader] Could not set public permissions: {e}")

        # 7. फाइनल लिंक रिटर्न करना
        return file.get('webViewLink')

    except Exception as e:
        print(f"❌ [Uploader] Upload Failed: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("☁️ Google Drive Uploader Test")
    print("═" * 50)
    
    # (इसे टेस्ट करने के लिए आपके पास temp/Final_Story.mp4 फाइल होनी चाहिए)
    test_file = "temp/Final_Story.mp4"
    
    if os.path.exists(test_file):
        link = upload_to_drive(test_file)
        if link:
            print(f"🎉 Success! Drive Link: {link}")
        else:
            print("❌ Upload failed.")
    else:
        print(f"⚠️ Test file missing at {test_file}")
    print("═" * 50)
