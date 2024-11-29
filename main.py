import tkinter
from tkinter import filedialog, messagebox

import customtkinter
from yt_dlp import YoutubeDL
import os
import time
import sys

sys.path = [
               'C:\\Users\\JA\\PycharmProjects\\mytubeDownloader',
               'C:\\Users\\JA\\PycharmProjects\\mytubeDownloader\\venv',
               'C:\\Users\\JA\\PycharmProjects\\mytubeDownloader\\venv\\Lib\\site-packages'
           ] + sys.path



# Add FFmpeg to the list of binaries


# Determine if the application is running in a PyInstaller bundle
# ffmpeg_path = r"c:\users\JA\Desktop\youtube downloader app\ffmpeg\ffmpeg.exe"
# try:
#     import customtkinter
# except ImportError as e:
#     raise RuntimeError("Failed to import customtkinter. Ensure it's installed and accessible.") from e

print(sys.path)


def resource_path(relative_path):
    """Get the path for bundled resources, used by PyInstaller."""
    try:
        base_path = sys._MEIPASS  # When bundled by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # When running normally

    return os.path.join(base_path, relative_path)

# FFmpeg path resolution
ffmpeg_path = resource_path('ffmpeg/ffmpeg.exe')
if not os.path.exists(ffmpeg_path):
    raise FileNotFoundError(f"FFmpeg not found at {ffmpeg_path}")

# Initialize the app window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("700x400")
app.title("MyTube Downloader")
app.iconbitmap(resource_path("icon.ico"))  # Set the icon using resource_path


# Global variables
download_paused = False
download_running = False
current_ydl = None
download_folder = os.path.join(os.path.expanduser("~"), "Downloads")



def pick_folder():
    """Let the user pick a folder to save downloads."""
    global download_folder
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        download_folder = selected_folder
        folder_label.configure(text=f"Download Folder: {download_folder}")


def update_progress_bar(status):
    """Update progress bar and status information."""
    global download_paused
    if status['status'] == 'downloading' and not download_paused:
        downloaded = status.get('downloaded_bytes', 0)
        total = status.get('total_bytes', 1)
        progress = downloaded / total
        progress_bar.set(progress)

        speed = status.get('speed', 0)
        eta = status.get('eta', 0)
        file_size = status.get('total_bytes', 0)
        percent = int(progress * 100)

        # Update the status label with detailed information
        status_label.configure(
            text=(
                f"Downloading... {percent}%\n"
                f"Speed: {speed / 1024:.2f} KB/s | "
                f"ETA: {eta}s | "
                f"Size: {file_size / (1024 ** 2):.2f} MB"
            )
        )
        app.update_idletasks()


def show_popup(message, title="Notification"):
    """Display a popup message."""
    messagebox.showinfo(title, message)


def pause_download():
    """Pause the download."""
    global download_paused
    download_paused = True
    status_label.configure(text="Download Paused")


def resume_download():
    """Resume the download."""
    global download_paused
    download_paused = False
    status_label.configure(text="Resuming Download...")
    app.update_idletasks()
    if current_ydl:
        current_ydl.download([link.get()])


def download_video():
    """Download a YouTube video."""
    global current_ydl, download_running, download_paused
    yt_dlp_link = link.get()
    if not yt_dlp_link.strip():
        show_popup("Error: The URL cannot be empty.", "Input Error")
        return

    try:
        status_label.configure(text="Fetching video information...")
        app.update_idletasks()

        ydl_opts = {
            'ffmpeg_location': ffmpeg_path,  # Use resource_path-resolved FFmpeg path
            'format': 'best',
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'force-ipv4': True,
            'socket_timeout': 30,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'progress_hooks': [update_progress_bar],
            'continuedl': True,
        }

        with YoutubeDL(ydl_opts) as yt_dlp_object:
            current_ydl = yt_dlp_object
            info_dict = yt_dlp_object.extract_info(yt_dlp_link, download=False)
            video_title = info_dict.get('title', 'Unknown Title')

            title_label.configure(text=f"Title: {video_title}")
            progress_bar.pack(pady=10)
            app.update_idletasks()

            download_running = True
            download_paused = False
            yt_dlp_object.download([yt_dlp_link])

        # Update file modification time
        file_path = os.path.join(download_folder, f"{info_dict.get('title', 'Unknown Title')}.mp4")
        if os.path.exists(file_path):
            current_time = time.time()
            os.utime(file_path, (current_time, current_time))

        show_popup(f"Download Complete: {video_title}")
        status_label.configure(text="Video Download Complete!")
        link.delete(0, tkinter.END)

    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            show_popup("Download interrupted by user.", "Download Interrupted")
        elif "ffmpeg" in str(e).lower():
            show_popup("Error: FFmpeg is missing or not working correctly.", "FFmpeg Error")
        elif "Network" in str(e) or "Timeout" in str(e):
            show_popup("Network error: Please check your connection.", "Network Error")
        else:
            show_popup(f"Unexpected Error: {e}", "Download Error")
        status_label.configure(text=f"Error: {e}")

    finally:
        progress_bar.pack_forget()
        current_ydl = None
        download_running = False


def download_audio():
    """Download YouTube audio as MP3."""
    global current_ydl, download_running, download_paused
    yt_dlp_link = link.get()
    if not yt_dlp_link.strip():
        show_popup("Error: The URL cannot be empty.", "Input Error")
        return

    try:
        status_label.configure(text="Fetching audio information...")
        app.update_idletasks()

        # Ensure the FFmpeg executable path is correctly set
        if not os.path.exists(ffmpeg_path):
            show_popup("Error: FFmpeg not found.", "Missing FFmpeg")
            return

        ydl_opts = {
            'ffmpeg_location': ffmpeg_path,
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'force-ipv4': True,
            'socket_timeout': 30,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'FFmpegMetadata',
                }
            ],
            'progress_hooks': [update_progress_bar],
            'continuedl': True,
        }

        with YoutubeDL(ydl_opts) as yt_dlp_object:
            current_ydl = yt_dlp_object
            info_dict = yt_dlp_object.extract_info(yt_dlp_link, download=False)
            audio_title = info_dict.get('title', 'Unknown Title')

            title_label.configure(text=f"Title: {audio_title}")
            progress_bar.pack(pady=10)
            app.update_idletasks()

            download_running = True
            download_paused = False
            yt_dlp_object.download([yt_dlp_link])

        # After audio download completes, update modification time
        file_path = os.path.join(download_folder, f"{info_dict.get('title', 'Unknown Title')}.mp3")
        if os.path.exists(file_path):
            current_time = time.time()
            os.utime(file_path, (current_time, current_time))

        show_popup(f"Audio Download Complete: {audio_title}")
        status_label.configure(text="Audio Download Complete!")
        link.delete(0, tkinter.END)

    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            show_popup("Download interrupted by user.", "Download Interrupted")
        elif "ffmpeg" in str(e).lower():
            show_popup("Error: FFmpeg is missing or not working correctly.", "FFmpeg Error")
        elif "Network" in str(e) or "Timeout" in str(e):
            show_popup("Network error: Please check your connection.", "Network Error")
        else:
            show_popup(f"Unexpected Error: {e}", "Download Error")
        status_label.configure(text=f"Error: {e}")

    finally:
        progress_bar.pack_forget()
        current_ydl = None
        download_running = False


# UI Elements
title = customtkinter.CTkLabel(app, text="MyTube Downloader", font=("Helvetica", 20), fg_color="black",
                               text_color="white")
title.pack(padx=10, pady=10)

# Input box directly on the main window
link = customtkinter.CTkEntry(app, width=600, height=40, placeholder_text="Paste YouTube link here")
link.pack(pady=10)

# Folder Picker
folder_button = customtkinter.CTkButton(app, text="Choose Download Folder", command=pick_folder)
folder_button.pack(pady=10)
folder_label = customtkinter.CTkLabel(app, text=f"Download Folder: {download_folder}", font=("Helvetica", 14),
                                      text_color="white")
folder_label.pack(pady=5)

# Buttons for Download, Pause, and Resume
button_frame = customtkinter.CTkFrame(app, fg_color="black")
button_frame.pack(pady=20)

download_video_button = customtkinter.CTkButton(button_frame, text="Download Video", fg_color="green",
                                                command=download_video)
download_video_button.pack(side="left", padx=5)

download_audio_button = customtkinter.CTkButton(button_frame, text="Download Audio", fg_color="green",
                                                command=download_audio)
download_audio_button.pack(side="left", padx=5)

pause_button = customtkinter.CTkButton(button_frame, text="Pause", fg_color="blue", command=pause_download)
pause_button.pack(side="left", padx=5)

resume_button = customtkinter.CTkButton(button_frame, text="Resume", fg_color="purple", command=resume_download)
resume_button.pack(side="left", padx=5)

# Progress Bar and Status Label
progress_bar = customtkinter.CTkProgressBar(app, width=600)
progress_bar.set(0)

status_label = customtkinter.CTkLabel(app, text="", font=("Helvetica", 14), text_color="white")
status_label.pack(pady=10)

title_label = customtkinter.CTkLabel(app, text="", font=("Helvetica", 18, "bold"), text_color="white")
title_label.pack()

badge_label = customtkinter.CTkLabel(app, text=" Powered by SkySurf Digital © 2024.", font=("Helvetica", 12),
                                     text_color="white")
badge_label.pack(pady=20)

if __name__ == "__main__":
    app.mainloop()



