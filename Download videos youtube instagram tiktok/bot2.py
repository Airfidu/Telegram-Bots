import telebot
import os
import re
import yt_dlp
import time

BOT_TOKEN = "8430218433:AAFRWx28rirgOPgifBG-DBfcwZWq-hsstmM"
OUTPUT = os.path.join(os.path.dirname(__file__), "videos")
MAX_SIZE = 200 * 1024 * 1024  # 200MB

bot = telebot.TeleBot(BOT_TOKEN)

os.makedirs(OUTPUT, exist_ok=True)
user_states = {}

def format_bytes(bytes_val):
    """Convert bytes to human readable format"""
    if bytes_val is None or bytes_val == 0:
        return "0B"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f}{unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f}TB"

def format_time(seconds):
    """Convert seconds to human readable format"""
    if seconds is None or seconds <= 0:
        return "calculating..."
    
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"

class DownloadProgressTracker:
    """Track download progress and update Telegram message"""
    def __init__(self, chat_id, message_id, bot):
        self.chat_id = chat_id
        self.message_id = message_id
        self.bot = bot
        self.last_update = 0
        self.start_time = time.time()
        
    def __call__(self, d):
        if d['status'] == 'downloading':
            current_time = time.time()
            
            # Update every 1.5 seconds
            if current_time - self.last_update >= 1.5:
                try:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    speed = d.get('speed', 0)
                    eta = d.get('eta', 0)
                    
                    if total > 0:
                        percentage = (downloaded / total) * 100
                        
                        # Progress bar
                        bar_length = 10
                        filled = int(bar_length * downloaded / total)
                        bar = '█' * filled + '░' * (bar_length - filled)
                        
                        progress_text = (
                            f"⏳ *Downloading...*\n\n"
                            f"`{bar}` {percentage:.1f}%\n\n"
                            f"📦 *Downloaded:* {format_bytes(downloaded)} / {format_bytes(total)}\n"
                            f"⚡ *Speed:* {format_bytes(speed)}/s\n"
                            f"⏱️ *Time left:* {format_time(eta)}"
                        )
                    else:
                        progress_text = (
                            f"⏳ *Downloading...*\n\n"
                            f"📦 *Downloaded:* {format_bytes(downloaded)}\n"
                            f"⚡ *Speed:* {format_bytes(speed)}/s"
                        )
                    
                    self.bot.edit_message_text(
                        progress_text,
                        chat_id=self.chat_id,
                        message_id=self.message_id,
                        parse_mode='Markdown'
                    )
                    
                    self.last_update = current_time
                    
                except Exception as e:
                    pass
        
        elif d['status'] == 'finished':
            try:
                self.bot.edit_message_text(
                    "✅ *Download complete!*\n📤 *Uploading to Telegram...*",
                    chat_id=self.chat_id,
                    message_id=self.message_id,
                    parse_mode='Markdown'
                )
            except:
                pass

def download_video(url, chat_id, message_id, audio_only=False):
    """Download video or audio using yt-dlp with enhanced options"""
    try:
        progress_tracker = DownloadProgressTracker(chat_id, message_id, bot)
        
        # Common options for all downloads
        common_opts = {
            'outtmpl': os.path.join(OUTPUT, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_tracker],
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': False,
            # YouTube-specific fixes
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
        }
        
        if audio_only:
            # Audio download options
            ydl_opts = {
                **common_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            # Video download options with fallback formats
            ydl_opts = {
                **common_opts,
                'format': (
                    'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/'
                    'bestvideo[height<=720]+bestaudio/best[height<=720]/'
                    'best'
                ),
                'merge_output_format': 'mp4',
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get info
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            
            # Download
            ydl.download([url])
            
            # Find the downloaded file
            if audio_only:
                base_filename = ydl.prepare_filename(info)
                filename = os.path.splitext(base_filename)[0] + '.mp3'
            else:
                filename = ydl.prepare_filename(info)
            
            # If file not found, search in OUTPUT directory
            if not os.path.exists(filename):
                base_name = os.path.splitext(os.path.basename(filename))[0]
                for file in os.listdir(OUTPUT):
                    if base_name in file:
                        filename = os.path.join(OUTPUT, file)
                        break
        
        return filename, title
    
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")

def detect_platform(url):
    """Detect platform from URL"""
    url_lower = url.lower()
    
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"  
    elif "instagram.com" in url_lower:
        return "instagram"  
    elif "tiktok.com" in url_lower:
        return "tiktok" 
    else:
        return None

@bot.message_handler(commands=['start', 'help'])
def start(msg):
    welcome_text = (
        "👋 *Welcome to Video Downloader Bot!*\n\n"
        "📹 YouTube\n"
        "📸 Instagram\n"
        "🎵 TikTok\n\n"
        "Choose an option below:"
    )
    
    bot.reply_to(msg, welcome_text, parse_mode='Markdown')

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = telebot.types.KeyboardButton('📹 Download Video')
    itembtn2 = telebot.types.KeyboardButton('🎵 Download Audio (YouTube)')
    markup.add(itembtn1, itembtn2)

    bot.send_message(msg.chat.id, "👇 *Select an option:*", reply_markup=markup, parse_mode='Markdown')
    user_states[msg.chat.id] = "menu"

@bot.message_handler(func=lambda m: m.text in ['📹 Download Video', '🎵 Download Audio (YouTube)'])
def handle_options(msg):
    if msg.text == '📹 Download Video':
        user_states[msg.chat.id] = "waiting_for_video_url"
        bot.reply_to(msg, "📤 *Send the link*\n\nSupported: YouTube, Instagram, TikTok", parse_mode='Markdown')
    
    elif msg.text == '🎵 Download Audio (YouTube)':
        user_states[msg.chat.id] = "waiting_for_audio_url"
        bot.reply_to(msg, "📤 *Send YouTube link*\n\nI'll extract the audio as MP3", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_url(msg):
    url = msg.text.strip()
    chat_id = msg.chat.id
    
    platform = detect_platform(url)
    
    if not platform:
        bot.reply_to(msg, "❌ Invalid link! Send a link from YouTube")
        return
    
    if chat_id not in user_states:
        user_states[chat_id] = "waiting_for_video_url"
    
    state = user_states[chat_id]
    
    # Audio download
    if state == "waiting_for_audio_url":
        if not platform or "youtube" not in platform.lower():
            bot.reply_to(msg, "❌ Audio download only works with YouTube!")
            user_states[chat_id] = "menu"
            return
        
        progress_msg = bot.reply_to(msg, "🎵 *Preparing...*", parse_mode='Markdown')
        
        try:
            file_path, title = download_video(url, chat_id, progress_msg.message_id, audio_only=True)
            
            if file_path and os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                
                if file_size > MAX_SIZE:
                    bot.edit_message_text(
                        f"❌ File too large: {format_bytes(file_size)}\nMax: {format_bytes(MAX_SIZE)}",
                        chat_id=chat_id,
                        message_id=progress_msg.message_id
                    )
                    os.remove(file_path)
                    user_states[chat_id] = "menu"
                    return
                
                with open(file_path, "rb") as f:
                    bot.send_audio(chat_id, f, title=title, caption=f"✅ *{title}*", timeout=180, parse_mode='Markdown')
                
                bot.delete_message(chat_id, progress_msg.message_id)
                os.remove(file_path)
            
            user_states[chat_id] = "menu"
        
        except Exception as e:
            bot.edit_message_text(f"❌ Error: {str(e)}", chat_id=chat_id, message_id=progress_msg.message_id)
            user_states[chat_id] = "menu"
    
    # Video download
    elif state == "waiting_for_video_url":
        progress_msg = bot.reply_to(msg, f"📹 *Preparing download from {platform}...*", parse_mode='Markdown')
        
        try:
            file_path, title = download_video(url, chat_id, progress_msg.message_id, audio_only=False)
            
            if file_path and os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                
                if file_size > MAX_SIZE:
                    bot.edit_message_text(
                        f"❌ File too large: {format_bytes(file_size)}\nMax: {format_bytes(MAX_SIZE)}",
                        chat_id=chat_id,
                        message_id=progress_msg.message_id
                    )
                    os.remove(file_path)
                    user_states[chat_id] = "menu"
                    return
                
                with open(file_path, "rb") as f:
                    bot.send_video(
                        chat_id, f,
                        caption=f"✅ *{title}*\n📦 {format_bytes(file_size)}",
                        timeout=180,
                        supports_streaming=True,
                        parse_mode='Markdown'
                    )
                
                bot.delete_message(chat_id, progress_msg.message_id)
                os.remove(file_path)
            
            user_states[chat_id] = "menu"
        
        except Exception as e:
            bot.edit_message_text(f"❌ Error: {str(e)}", chat_id=chat_id, message_id=progress_msg.message_id)
            user_states[chat_id] = "menu"

print("🤖 Bot is running...")
print("Press Ctrl+C to stop")
bot.infinity_polling(timeout=60, long_polling_timeout=60)