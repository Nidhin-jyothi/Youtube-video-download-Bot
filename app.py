from flask import Flask, request, send_file
from twilio.twiml.messaging_response import MessagingResponse
import yt_dlp
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()
    msg = response.message()

    if "youtube.com" in incoming_msg or "youtu.be" in incoming_msg:
        try:
            # Define download options
            ydl_opts = {
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(incoming_msg, download=True)
                file_path = ydl.prepare_filename(info)

            # Send video back to user
            msg.body("Here is your video!")
            msg.media(f"https://your-server-url/download?file={os.path.basename(file_path)}")

        except Exception as e:
            msg.body("Failed to download the video. Please check the link and try again.")
    else:
        msg.body("Please send a valid YouTube link.")

    return str(response)

@app.route("/download", methods=["GET"])
def download_file():
    file_name = request.args.get('file')
    file_path = os.path.join('downloads', file_name)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
