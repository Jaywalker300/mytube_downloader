## Mytube Downloader
MyTube Downloader is a desktop application designed to easily download YouTube videos and audio directly to your local machine. It provides a clean and intuitive user interface built with customtkinter and utilizes yt_dlp for efficient downloading.

Features
1. Video Downloading: Download YouTube videos in the best available quality.

2. Audio Downloading: Extract audio from YouTube videos and save it as high-quality MP3.

3. Progress Tracking: Real-time progress bar with speed, estimated time (ETA), and percentage.

4. Pause and Resume: Ability to pause and resume downloads seamlessly.

5. Custom Download Folder: Choose where to save the downloaded files.

6. Cross-platform Compatibility: Built with Python and PyInstaller for potential cross-platform support.
7. Dark Theme Interface: Modern dark mode with green accents.

## Technologies Used
GUI Framework: customtkinter
YouTube Downloading: yt_dlp
Media Processing: FFmpeg (required for audio conversion)
Python Version: 3.8+

## Installation
Clone the repository or download the source files.

Install the required dependencies using:
pip install -r requirements.txt

Ensure FFmpeg is available in the ffmpeg directory or update the ffmpeg_path accordingly.
Run the application with:

python main.py

## Usage
1. Paste the YouTube link in the provided input field.
Choose your desired download folder (optional).

2. Click Download Video to save the video or Download Audio for audio extraction.

3. Use the Pause and Resume buttons to control the download process.

4. Monitor the download progress via the progress bar and status messages.

## Requirements
Python 3.8+

FFmpeg: Ensure it is correctly installed or included in the application folder.
Internet connection for downloading content.

Troubleshooting
FFmpeg Missing Error: Ensure FFmpeg is correctly placed in the ffmpeg folder or update ffmpeg_path.

Network Issues: Check your internet connection if you encounter network errors.

Timeouts: Ensure a stable internet connection or adjust the socket_timeout value.
Acknowledgments
Powered by yt_dlp, customtkinter, and FFmpeg.
Developed by SkySurf Digital © 2024.
Enjoy fast and easy YouTube downloads with MyTube Downloader!![mytube GUI](https://github.com/user-attachments/assets/91f1729f-c3b3-412a-89eb-119a8a35f8c6)
