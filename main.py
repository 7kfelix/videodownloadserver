import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title('Servidor de Downloads de Vídeos')

        self.url_label = tk.Label(root, text='URL do Vídeo:')
        self.url_label.grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        self.format_label = tk.Label(root, text='Formato:')
        self.format_label.grid(row=1, column=0, padx=10, pady=10)
        self.format_var = tk.StringVar(value='mp4')
        self.format_menu = ttk.Combobox(root, textvariable=self.format_var, values=['mp4', 'mp3'])
        self.format_menu.grid(row=1, column=1, padx=10, pady=10)

        self.quality_label = tk.Label(root, text='Qualidade:')
        self.quality_label.grid(row=2, column=0, padx=10, pady=10)
        self.quality_var = tk.StringVar(value='High')
        self.quality_menu = ttk.Combobox(root, textvariable=self.quality_var, values=['High', 'Medium', 'Low'])
        self. quality_menu.grid(row=2, column=1, padx=10, pady=10)

        self.progress = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

        self.download_button = tk.Button(root, text='Download', command=self.start_download)
        self.download_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


    def start_download(self):
        url = self.url_entry.get()
        format = self.format_var.get()
        quality = self.quality_var.get()
        threading.Thread(target=self.download_video, args=(url, format, quality)).start()


    def download_video(self, url, format, quality):
        output_path = filedialog.askdirectory()
        ydl_opts = {
            'format': f'bestvideo[ext={format}]+bestaudio/best' if format == 'mp4' else 'bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'progress_hooks': [self.ydl_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio' if format == 'mp3' else 'FFmpegVideoConvertor',
                'preferredcodec': 'mp3' if format == 'mp3' else None,
                'preferredquality': '192' if format == 'mp3' else None,
            }] if format == 'mp3' else [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': format
            }]
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo('Sucesso', 'Download Concluído!')
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def ydl_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes')
            if total_bytes and downloaded_bytes:
                progress_percent = downloaded_bytes / total_bytes * 100
                self.progress['value'] = progress_percent
                self.root.update_idletasks()

if __name__ == '__main__':
    root = tk.Tk()
    app = VideoDownloader(root)
    root.mainloop()