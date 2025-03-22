import csv
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
# List of websites and their configurations
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
    }
    ,
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

# Common headers (modify if needed)
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

# Post comments for one website
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
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for idx, row in enumerate(reader, start=1):
            comment = row['comment']
            author = row['author']
            email = row['email']

            print(f"\n🚀 Sending comment #{idx} to all sites at the same time...")

            with ThreadPoolExecutor(max_workers=len(websites)) as executor:
                futures = []
                for website in websites:
                    futures.append(executor.submit(post_comment_to_site, website, comment, author, email, idx))

                # Wait for all sites to finish posting this comment
                for future in as_completed(futures):
                    future.result()  # This will raise any exception inside the thread if exists

            # Delay after each round of comments (optional)
            delay = random.randint(5, 10)
            print(f"\n⏳ Waiting {delay} seconds before next comment...\n")
            time.sleep(delay)

def main():
    csv_file = 'comments.csv'
    post_comments_parallel(csv_file)

if __name__ == '__main__':
    main()