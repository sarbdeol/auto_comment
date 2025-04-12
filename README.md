# 📝 Mass Comment Poster with Web UI

This Python project allows you to upload a CSV of comments and **automatically post them** across multiple WordPress websites’ comment forms using `requests`. The app includes a **web-based UI (Flask)** to upload CSVs and start/stop the posting process.

---

## 🚀 Features

- 📤 Auto-posts comments to multiple WordPress-based websites
- 🧠 Parallel processing using `ThreadPoolExecutor`
- 🔃 Smart delay and stop/resume control
- 🌐 Web UI (Flask) for uploading CSV and controlling the process
- 📁 All media and requests are locally handled

---

## 📦 Requirements

- Python 3.7+
- Flask

Install dependencies:
```bash
pip install flask requests





🧾 CSV Format
Upload a comments.csv file in the following format:

csv

comment,author,email
"This is a test comment","John Doe","john@example.com"
"Great article!","Alice Smith","alice@domain.com"


##  💻 Web Interface
After running the script, go to:



http://localhost:5000
You’ll see:

📂 Upload CSV button to update the comments file

▶️ Start Process button to begin automated posting

⛔ Stop Process button to halt the current loop

