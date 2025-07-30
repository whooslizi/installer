import tkinter as tk
import requests, zipfile, io, os, subprocess
from tkinter import messagebox

apps = {
    "UniKey": {
        "url": "https://www.unikey.org/assets/release/unikey46RC2-230919-win64.zip",
        "type": "zip",
        "exe": "UniKeyNT.exe"
    },
    "Firefox": {
        "url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US",
        "type": "exe"
    },
    "Office": {
        "url": "https://c2rsetup.officeapps.live.com/c2r/download.aspx?ProductreleaseID=O365ProPlusRetail&platform=x64&language=en-us&version=O16GA",
        "type": "exe"
    },
    "Zalo PC": {
        "url": "https://download.zalo.me/pc/ZaloSetup-64bit.exe",
        "type": "exe"
    },
    "Visual C++": {
        "url": "https://aka.ms/vs/17/release/vc_redist.x64.exe",
        "type": "exe"
    },
    "Foxit Reader": {
        "url": "https://cdn01.foxitsoftware.com/product/reader/desktop/win/12.1.3/FoxitPDFReader1213_L10N_Setup_Prom.exe",
        "type": "exe"
    },
    "UltraViewer": {
        "url": "https://ultraviewer.net/UltraViewer_setup_6.6_vi.exe",
        "type": "exe"
    },
    "VLC Media Player": {
        "url": "https://get.videolan.org/vlc/3.0.20/win64/vlc-3.0.20-win64.exe",
        "type": "exe"
    },
    ".NET 3.5": {
        "url": "https://download.microsoft.com/download/1/7/D/17D8C7D8-F4DE-4A69-9C5F-9BC3DDC833CA/dotnetfx35.exe",
        "type": "exe"
    },
    ".NET 4.8": {
        "url": "https://go.microsoft.com/fwlink/?linkid=2088631",
        "type": "exe"
    },
    "Activate Office": {
        "url": "https://raw.githubusercontent.com/massgravel/Microsoft-Activation-Scripts/master/MAS/Separate-Files-Version/Activators/Ohook_Activation_AIO.cmd",
        "type": "cmd"
    }
}

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def install_app(name):
    app = apps[name]
    url = app["url"]
    ext_type = app["type"]

    if not url:
        lbl_status.config(text=f"{name}: No URL provided.")
        return

    try:
        lbl_status.config(text=f"Downloading {name}...")
        root.update_idletasks()

        r = requests.get(url, stream=True)

        if ext_type == "zip":
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(DOWNLOAD_DIR)
            filepath = os.path.join(DOWNLOAD_DIR, app["exe"])
            subprocess.Popen(filepath)

        else:
            filename = url.split("/")[-1].split("?")[0] or f"{name}.{ext_type}"
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(1024 * 1024):
                    f.write(chunk)

            if ext_type == "cmd":
                subprocess.Popen(["cmd.exe", "/k", filepath], shell=True)
            else:
                subprocess.Popen(filepath)

        lbl_status.config(text=f"Running {name}...")
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {name}\n{str(e)}")
        lbl_status.config(text="Error.")

root = tk.Tk()
root.title("Automatic App Downloader")
root.geometry("400x700")

tk.Label(root, text="App Installer", fg="red", font=("Arial", 13, "bold")).pack(pady=10)

for app_name in apps:
    tk.Button(root, text=app_name, width=35, command=lambda n=app_name: install_app(n)).pack(pady=4)

lbl_status = tk.Label(root, text="", fg="green")
lbl_status.pack(pady=20)

root.mainloop()
