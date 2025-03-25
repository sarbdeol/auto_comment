import csv
import requests
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from flask import Flask, request, redirect, url_for, render_template_string, flash

# ------------------------------
# Global Stop Event for the Process
# ------------------------------
stop_event = threading.Event()

# ------------------------------
# Website Configurations (from your comment.py)
# ------------------------------
websites = [
    {
        'name': 'Site 1',
        'url': 'https://icam-colloquium.ucdavis.edu/wp-comments-post.php',
        'referer': 'https://icam-colloquium.ucdavis.edu/2021/05/13/introduction-to-emergence/',
        'origin': 'https://icam-colloquium.ucdavis.edu',
        'comment_post_ID': 125,
        'csv_file': 'comments.csv'
    },
    {
        'name': 'Site 2',
        'url': 'https://hukum.upnvj.ac.id/wp-comments-post.php',
        'referer': 'https://hukum.upnvj.ac.id/dosen-fakultas-hukum-upn-veteran-jakarta-juga-turut-ikut-menerbitkan-buku/',
        'origin': 'https://hukum.upnvj.ac.id',
        'comment_post_ID': 26930,
        'csv_file': 'comments.csv'
    },
    {
        'name': 'Site 3',
        'url': 'https://nanojournal.ifmo.ru/en/wp-comments-post.php',
        'referer': 'https://nanojournal.ifmo.ru/en/articles-2/volume3/3-2/chemistry/',
        'origin': 'https://nanojournal.ifmo.ru',
        'comment_post_ID': 492,
        'csv_file': 'comments.csv',
    },
    {
        'name': 'Site 4',
        'url': 'https://cssh.uog.edu.et/wp-comments-post.php',
        'referer': 'https://cssh.uog.edu.et/lms-wordpress-plugin/',
        'origin': 'https://cssh.uog.edu.et',
        'comment_post_ID': 60,
        'csv_file': 'comments.csv'
    },
    {
        'name': 'Site 5',
        'url': 'https://shindig-magazine.com/wp-comments-post.php',
        'referer': 'https://shindig-magazine.com/?p=6749',
        'origin': 'https://shindig-magazine.com',
        'comment_post_ID': 6749,
        'csv_file': 'comments.csv'
    },
    {
        'name': 'Site 6',
        'url': 'https://vitamagazine.com/wp-comments-post.php',
        'referer': 'https://vitamagazine.com/2024/02/01/the-most-flattering-haircut-for-thin-hair-what-to-avoid-heres-what-one-expert-says/',
        'origin': 'https://vitamagazine.com',
        'comment_post_ID': 57605,
        'csv_file': 'comments.csv',
    },
    {
        'name': 'Site 7',
        'url': 'https://vitamagazine.com/wp-comments-post.php',
        'referer': 'https://vitamagazine.com/2024/02/12/a-brief-history-of-the-crop-top/',
        'origin': 'https://vitamagazine.com',
        'comment_post_ID': 58100,
        'csv_file': 'comments.csv',
    },
    {
        'name': 'Site 8',
        'url': 'https://www.mae.gov.bi/wp-comments-post.php',
        'referer': 'https://www.mae.gov.bi/2021/10/05/celebration-du-72eme-anniversaire-de-la-fondation-de-la-republique-populaire-de-chine/',
        'origin': 'https://www.mae.gov.bi',
        'comment_post_ID': 5286,
        'csv_file': 'comments.csv'
    },
    {
        'name': 'Site 9',
        'url': 'https://blog.bhhscalifornia.com/wp-comments-post.php',
        'referer': 'https://blog.bhhscalifornia.com/how-much-does-land-cost-in-california/',
        'origin': 'https://blog.bhhscalifornia.com',
        'comment_post_ID': 21898,
        'csv_file': 'comments.csv'
    },
    {
        'name': 'Site 10',
        'url': 'https://pgpaud.unimed.ac.id/wp-comments-post.php',
        'referer': 'https://pgpaud.unimed.ac.id/2023/05/27/program-studi-pg-paud-unimed-gelar-webinar-nasional-tentang-peran-ict-dalam-manajemen-lembaga-pendidikan/',
        'origin': 'https://pgpaud.unimed.ac.id',
        'comment_post_ID': 3026,
        'csv_file': 'comments.csv'
    },
    {
        'name': 'Site 12',
        'url': 'https://www.pharmachoice.com/wp-comments-post.php',
        'referer': 'https://www.pharmachoice.com/flyer/',
        'origin': 'https://www.pharmachoice.com',
        'comment_post_ID': 5829,
        'csv_file': 'comments.csv'
    },
    {
        'name': 'Site 13',
        'url': 'https://hukum.upnvj.ac.id/wp-comments-post.php',
        'referer': 'https://hukum.upnvj.ac.id/dosen-fakultas-hukum-upn-veteran-jakarta-juga-turut-ikut-menerbitkan-buku/',
        'origin': 'https://hukum.upnvj.ac.id',
        'comment_post_ID': 26930,
        'csv_file': 'comments.csv'
    }
]

# ------------------------------
# Common Helper Functions
# ------------------------------
def build_headers(referer, origin):
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Origin': origin,
        'Pragma': 'no-cache',
        'Referer': referer,
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        ])
    }

def post_comment_to_site(website, comment, author, email, idx):
    payload = {
        'comment': comment,
        'author': author,
        'email': email,
        'url': '',
        'submit': 'Post Comment',
        'comment_post_ID': website['comment_post_ID'],
        'comment_parent': 0
    }
    headers = build_headers(website['referer'], website['origin'])
    cookies = website.get('cookies', None)
    try:
        response = requests.post(
            website['url'],
            headers=headers,
            data=payload,
            cookies=cookies,
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ [{website['name']}] Comment #{idx} posted by {author}")
        else:
            print(f"❌ [{website['name']}] Failed ({response.status_code}) for {author}")
            print(f"Response snippet: {response.text[:200]}...")
    except Exception as e:
        print(f"⚠️ [{website['name']}] Error for {author}: {str(e)}")

def post_comments_parallel(csv_file):
    """
    Reads the CSV and posts comments to all sites. Checks for a stop signal
    at each comment and during delays.
    """
    global stop_event
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader, start=1):
                if stop_event.is_set():
                    print("Process stopped before comment", idx)
                    break

                comment = row['comment']
                author = row['author']
                email = row['email']

                print(f"\n🚀 Sending comment #{idx} to all sites at the same time...")

                with ThreadPoolExecutor(max_workers=len(websites)) as executor:
                    futures = []
                    for website in websites:
                        futures.append(executor.submit(post_comment_to_site, website, comment, author, email, idx))
                    for future in as_completed(futures):
                        # Raise exception if any occurred in the thread
                        future.result()

                delay = random.randint(5, 10)
                print(f"\n⏳ Waiting {delay} seconds before next comment...\n")
                # Check the stop_event during the delay loop
                for _ in range(delay):
                    if stop_event.is_set():
                        print("Process stopped during delay before comment", idx + 1)
                        return
                    time.sleep(1)
    except Exception as e:
        print("Error reading CSV:", e)

# ------------------------------
# Flask Application Setup
# ------------------------------
app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = os.path.abspath('.')  # Folder where CSV will be saved/replaced
CSV_FILENAME = 'comments.csv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

process_thread = None

@app.route('/')
def index():
    html = """
    <!doctype html>
    <html>
    <head>
      <title>CSV Upload and Process Control</title>
    </head>
    <body>
    <h1>Upload CSV File</h1>
    <form method="post" enctype="multipart/form-data" action="/upload">
      <input type="file" name="csv_file">
      <input type="submit" value="Upload">
    </form>
    <h1>Process Controls</h1>
    <form method="post" action="/start">
      <input type="submit" value="Start Process">
    </form>
    <form method="post" action="/stop">
      <input type="submit" value="Stop Process">
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csv_file' not in request.files:
        flash("No file part")
        return redirect(url_for('index'))
    file = request.files['csv_file']
    if file.filename == '':
        flash("No file selected")
        return redirect(url_for('index'))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], CSV_FILENAME)
    file.save(filepath)
    flash("CSV file uploaded and replaced successfully")
    return redirect(url_for('index'))

@app.route('/start', methods=['POST'])
def start_process():
    global process_thread, stop_event
    if process_thread is None or not process_thread.is_alive():
        # Clear any previous stop signal before starting
        stop_event.clear()
        process_thread = threading.Thread(target=post_comments_parallel, args=(CSV_FILENAME,))
        process_thread.start()
        flash("Process started")
    else:
        flash("Process is already running")
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_process():
    global stop_event
    stop_event.set()
    flash("Process stopped")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
