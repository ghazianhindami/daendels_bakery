import os
import webbrowser
import subprocess

def main():
    script_path = os.path.abspath("app.py")
    url = "http://localhost:8502"

    # buka browser
    webbrowser.open(url)

    # jalankan Streamlit (non-blocking)
    streamlit_process = subprocess.Popen([
        "streamlit", "run", script_path,
        "--server.headless=true",
        "--server.port=8502",
        "--browser.serverAddress=localhost",
        "--server.fileWatcherType=none"
    ])

    # jalankan FastAPI (non-blocking)
    api_process = subprocess.Popen([
        "uvicorn", "api.serviceapi:app",
        "--port", "8000"
    ])

    # tunggu kedua proses selesai
    streamlit_process.wait()
    api_process.wait()

if __name__ == "__main__":
    main()