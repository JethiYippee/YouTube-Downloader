import customtkinter as ctk
import threading
import yt_dlp
import tkinter.messagebox as msgbox
import os

def get_downloads_folder():
    if os.name == 'nt':
        import ctypes.wintypes
        CSIDL_PERSONAL = 0x0005
        SHGFP_TYPE_CURRENT = 0
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        return os.path.join(os.path.dirname(buf.value), "Downloads")
    else:
        return os.path.join(os.path.expanduser("~"), "Downloads")

def download_video():
    url = video_url_entry.get()
    video_status_label.configure(text="Downloading...")
    video_log_textbox.configure(state="normal")
    video_log_textbox.delete("1.0", "end")
    video_log_textbox.configure(state="disabled")

    def _download():
        try:
            def log_hook(d):
                msg = ""
                if d['status'] == 'downloading':
                    msg = f"Downloading: {d.get('filename', '')}"
                elif d['status'] == 'finished':
                    msg = f"Download finished: {d.get('filename', '')}"
                elif d['status'] == 'error':
                    msg = f"Error: {d.get('filename', '')}"
                else:
                    msg = str(d)
                video_log_textbox.configure(state="normal")
                video_log_textbox.insert("end", msg + "\n")
                video_log_textbox.see("end")
                video_log_textbox.configure(state="disabled")

            class MyLogger:
                def debug(self, msg):
                    if '[download]' in msg or '[ffmpeg]' in msg or '[EmbedThumbnail]' in msg or '[Metadata]' in msg:
                        video_log_textbox.configure(state="normal")
                        video_log_textbox.insert("end", msg.strip() + "\n")
                        video_log_textbox.see("end")
                        video_log_textbox.configure(state="disabled")
                def warning(self, msg):
                    video_log_textbox.configure(state="normal")
                    video_log_textbox.insert("end", "Warning: " + msg.strip() + "\n")
                    video_log_textbox.see("end")
                    video_log_textbox.configure(state="disabled")
                def error(self, msg):
                    video_log_textbox.configure(state="normal")
                    video_log_textbox.insert("end", "Error: " + msg.strip() + "\n")
                    video_log_textbox.see("end")
                    video_log_textbox.configure(state="disabled")

            downloads_folder = get_downloads_folder()
            outtmpl = os.path.join(downloads_folder, "%(title)s.%(ext)s")

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'outtmpl': outtmpl,
                'noplaylist': True,
                'quiet': True,
                'logger': MyLogger(),
                'progress_hooks': [log_hook],
                'embedthumbnail': True,
                'writethumbnail': True,
                'postprocessors': [
                    {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
                    {'key': 'EmbedThumbnail'},
                    {'key': 'FFmpegMetadata'},
                ],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            video_status_label.configure(text="Download Completed!")
            video_log_textbox.configure(state="normal")
            video_log_textbox.insert("end", "✅ Video saved to Downloads\n")
            video_log_textbox.see("end")
            video_log_textbox.configure(state="disabled")
        except Exception as e:
            video_status_label.configure(text=f"Error: {e}")
            msgbox.showerror("YouTube Downloader", f"Error: {e}")

    threading.Thread(target=_download).start()

def download_audio():
    url = audio_url_entry.get()
    audio_quality_label = audio_quality_var.get()
    file_format = audio_format_var.get()
    audio_quality = audio_quality_label.replace("kbps", "")
    audio_status_label.configure(text="Downloading...")
    audio_log_textbox.configure(state="normal")
    audio_log_textbox.delete("1.0", "end")
    audio_log_textbox.configure(state="disabled")

    def _download():
        try:
            def log_hook(d):
                msg = ""
                if d['status'] == 'downloading':
                    msg = f"Downloading: {d.get('filename', '')}"
                elif d['status'] == 'finished':
                    msg = f"Download finished: {d.get('filename', '')}"
                elif d['status'] == 'error':
                    msg = f"Error: {d.get('filename', '')}"
                else:
                    msg = str(d)
                audio_log_textbox.configure(state="normal")
                audio_log_textbox.insert("end", msg + "\n")
                audio_log_textbox.see("end")
                audio_log_textbox.configure(state="disabled")

            class MyLogger:
                def debug(self, msg):
                    if '[download]' in msg or '[ffmpeg]' in msg or '[EmbedThumbnail]' in msg or '[Metadata]' in msg:
                        audio_log_textbox.configure(state="normal")
                        audio_log_textbox.insert("end", msg.strip() + "\n")
                        audio_log_textbox.see("end")
                        audio_log_textbox.configure(state="disabled")
                def warning(self, msg):
                    audio_log_textbox.configure(state="normal")
                    audio_log_textbox.insert("end", "Warning: " + msg.strip() + "\n")
                    audio_log_textbox.see("end")
                    audio_log_textbox.configure(state="disabled")
                def error(self, msg):
                    audio_log_textbox.configure(state="normal")
                    audio_log_textbox.insert("end", "Error: " + msg.strip() + "\n")
                    audio_log_textbox.see("end")
                    audio_log_textbox.configure(state="disabled")

            downloads_folder = get_downloads_folder()
            outtmpl = os.path.join(downloads_folder, "%(title)s.%(ext)s")

            ydl_opts = {
                'format': f"bestaudio[ext={file_format}]/bestaudio/best",
                'outtmpl': outtmpl,
                'noplaylist': True,
                'quiet': True,
                'logger': MyLogger(),
                'progress_hooks': [log_hook],
                'embedthumbnail': True,
                'writethumbnail': True,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': file_format,
                        'preferredquality': audio_quality
                    },
                    {'key': 'EmbedThumbnail'},
                    {'key': 'FFmpegMetadata'},
                ],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            audio_status_label.configure(text="Download Completed!")
            audio_log_textbox.configure(state="normal")
            audio_log_textbox.insert("end", "✅ Download Completed!\n")
            audio_log_textbox.see("end")
            audio_log_textbox.configure(state="disabled")
        except Exception as e:
            audio_status_label.configure(text=f"Error: {e}")
            msgbox.showerror("YouTube Downloader", f"Error: {e}")

    threading.Thread(target=_download).start()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("660x430")
app.title("YouTube Downloader")

tabview = ctk.CTkTabview(app, width=640, height=400)
tabview.pack(padx=10, pady=10)
tabview.add("Video")
tabview.add("Audio")

video_tab = tabview.tab("Video")

video_url_label = ctk.CTkLabel(video_tab, text="YouTube Video Link:")
video_url_label.pack(pady=(20, 5))
video_url_entry = ctk.CTkEntry(video_tab, width=500)
video_url_entry.pack()

video_opts_frame = ctk.CTkFrame(video_tab)
video_opts_frame.pack(pady=10)

video_quality_label = ctk.CTkLabel(video_opts_frame, text="Quality:")
video_quality_label.grid(row=0, column=0, padx=10, pady=5)
video_quality_options = ["2160p", "1440p", "1080p", "720p", "480p", "360p"]
video_quality_var = ctk.StringVar(value=video_quality_options[2])
video_quality_menu = ctk.CTkOptionMenu(video_opts_frame, variable=video_quality_var, values=video_quality_options)
video_quality_menu.grid(row=1, column=0, padx=10)

video_framerate_label = ctk.CTkLabel(video_opts_frame, text="Framerate:")
video_framerate_label.grid(row=0, column=1, padx=10, pady=5)
video_framerate_options = ["60fps", "30fps", "24fps"]
video_framerate_var = ctk.StringVar(value=video_framerate_options[1])
video_framerate_menu = ctk.CTkOptionMenu(video_opts_frame, variable=video_framerate_var, values=video_framerate_options)
video_framerate_menu.grid(row=1, column=1, padx=10)

video_format_label = ctk.CTkLabel(video_opts_frame, text="Format:")
video_format_label.grid(row=0, column=2, padx=10, pady=5)
video_format_options = ["mp4"]
video_format_var = ctk.StringVar(value="mp4")
video_format_menu = ctk.CTkOptionMenu(video_opts_frame, variable=video_format_var, values=video_format_options)
video_format_menu.grid(row=1, column=2, padx=10)

video_download_btn = ctk.CTkButton(video_tab, text="Download", command=download_video)
video_download_btn.pack(pady=10)
video_status_label = ctk.CTkLabel(video_tab, text="")
video_status_label.pack(pady=5)

video_log_textbox = ctk.CTkTextbox(video_tab, width=600, height=120)
video_log_textbox.pack(pady=4)
video_log_textbox.configure(state="disabled")

audio_tab = tabview.tab("Audio")

audio_url_label = ctk.CTkLabel(audio_tab, text="YouTube Audio Link:")
audio_url_label.pack(pady=(20, 5))
audio_url_entry = ctk.CTkEntry(audio_tab, width=500)
audio_url_entry.pack()

audio_opts_frame = ctk.CTkFrame(audio_tab)
audio_opts_frame.pack(pady=10)

audio_quality_label = ctk.CTkLabel(audio_opts_frame, text="Audio Quality:")
audio_quality_label.grid(row=0, column=0, padx=10, pady=5)
audio_quality_options = ["320kbps", "256kbps", "192kbps", "128kbps", "96kbps"]
audio_quality_var = ctk.StringVar(value=audio_quality_options[0])
audio_quality_menu = ctk.CTkOptionMenu(audio_opts_frame, variable=audio_quality_var, values=audio_quality_options)
audio_quality_menu.grid(row=1, column=0, padx=10)

audio_format_label = ctk.CTkLabel(audio_opts_frame, text="Audio Format:")
audio_format_label.grid(row=0, column=1, padx=10, pady=5)
audio_format_options = ["mp3", "wav", "aac", "m4a", "opus", "flac"]
audio_format_var = ctk.StringVar(value="mp3")
audio_format_menu = ctk.CTkOptionMenu(audio_opts_frame, variable=audio_format_var, values=audio_format_options)
audio_format_menu.grid(row=1, column=1, padx=10)

audio_download_btn = ctk.CTkButton(audio_tab, text="Download", command=download_audio)
audio_download_btn.pack(pady=10)
audio_status_label = ctk.CTkLabel(audio_tab, text="")
audio_status_label.pack(pady=5)

audio_log_textbox = ctk.CTkTextbox(audio_tab, width=600, height=120)
audio_log_textbox.pack(pady=4)
audio_log_textbox.configure(state="disabled")

app.mainloop()