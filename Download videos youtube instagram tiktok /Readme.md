# 🎥 Video Downloader Telegram Bot

A powerful and user-friendly Telegram bot that downloads videos and audio from **YouTube**, **Instagram**, and **TikTok** with real-time progress tracking.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg?logo=telegram)](https://telegram.org/)

## ✨ Features

- 📹 **Multi-Platform Support**: Download from YouTube, Instagram, and TikTok
- 🎵 **Audio Extraction**: Convert YouTube videos to MP3 format
- 📊 **Real-Time Progress**: Live download progress with speed and ETA
- ⚡ **Fast & Reliable**: Optimized download settings for best performance
- 🔒 **Safe**: Automatic file cleanup after sending

## 🚀 Demo

Try it out: [@YourBotUsername](https://t.me/YourBotUsername)

## 📸 Screenshots

### Video Download
```
⏳ Downloading...

████████░░ 85.3%

📦 Downloaded: 76.2MB / 89.0MB
⚡ Speed: 3.5MB/s
⏱️ Time left: 3s
```

### Audio Download
```
✅ Download complete!
📤 Uploading to Telegram...
```

## 🛠️ Tech Stack

- **Python 3.8+**
- **pyTelegramBotAPI** - Telegram Bot API wrapper
- **yt-dlp** - Video downloader for multiple platforms
- **FFmpeg** - Audio/video processing

## 📋 Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio conversion)
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

## 🔧 Installation

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Airfidu/Telegram-Bots.gits
cd Download-videos-youtube-instagram-tiktok
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install FFmpeg**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

5. **Set up environment variables**
```bash
export BOT_TOKEN="your_bot_token_here"
```

6. **Run the bot**
```bash
python bot.py
```

## 📝 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Your Telegram bot token from @BotFather | Yes |

### Customization

**Change maximum file size:**
```python
MAX_SIZE = 200 * 1024 * 1024  # 200MB (in bot.py)
```

**Change video quality:**
```python
'format': 'best[ext=mp4][height<=480]'  # 480p instead of 720p
```

## 📖 Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to see the menu
3. Choose an option:
   - **📹 Download Video** - For videos from YouTube/Instagram/TikTok
   - **🎵 Download Audio** - For YouTube audio (MP3)
4. Send the video link
5. Wait for download and upload to complete

### Supported URL Formats

- **YouTube**: `https://www.youtube.com/watch?v=...` or `https://youtu.be/...`
- **Instagram**: `https://www.instagram.com/p/...` or `https://www.instagram.com/reel/...`
- **TikTok**: `https://www.tiktok.com/@.../video/...`

## 🐛 Troubleshooting

### Bot not responding
- Check if bot token is correct
- Verify environment variables are set
- Check Render logs for errors

### Audio conversion failing
- Ensure FFmpeg is installed
- Check Render buildpack includes FFmpeg

### Download errors
- Some videos may be region-restricted
- Private videos cannot be downloaded
- Very large files (>200MB) will be rejected

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This bot is for educational purposes only. Please respect copyright laws and terms of service of the platforms you download from. The developers are not responsible for any misuse of this bot.

## 🙏 Acknowledgments

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) - Telegram Bot API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video downloader
- [FFmpeg](https://ffmpeg.org/) - Multimedia framework

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ by [Abderrahmane]
