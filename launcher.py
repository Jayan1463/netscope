import subprocess
import sys
import os

def main():
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    app_path = os.path.join(base_path, "app.py")

    subprocess.Popen([
        "/usr/bin/python3",
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.headless=true",
        "--server.fileWatcherType=none",
        "--browser.serverAddress=localhost",
        "--browser.gatherUsageStats=false"
    ])

if __name__ == "__main__":
    main()
