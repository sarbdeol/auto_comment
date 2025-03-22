import csv
import requests
import time
import random

# Configuration for skillsmalaysia.gov.my
site_config = {
    'name': 'Skills Malaysia',
    'url': 'https://www.skillsmalaysia.gov.my/index.php',
    'referer': 'https://www.skillsmalaysia.gov.my/index.php/en/k2-full-width/item/85-permintaan-dan-penawaran',
    'origin': 'https://www.skillsmalaysia.gov.my',
    'comment_post_ID': 85,  # itemID used in the payload
    'extra_payload': {
        'option': 'com_k2',
        'view': 'item',
        'task': 'comment'
    }
}

def build_headers(referer, origin):
    return {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': origin,
        'Referer': referer,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': random.choice([
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        ]),
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"'
    }

def post_comments(csv_file):
    print(f"\n🚀 Starting comments for: {site_config['name']}")
    
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for idx, row in enumerate(reader, start=1):
                comment = row['comment']
                author = row['author']
                email = row['email']

                payload = {
                    'userName': author,
                    'commentEmail': email,
                    'commentURL': '',
                    'commentText': comment,
                    'itemID': site_config['comment_post_ID'],
                    **site_config['extra_payload']
                }

                headers = build_headers(site_config['referer'], site_config['origin'])

                try:
                    response = requests.post(
                        site_config['url'],
                        headers=headers,
                        data=payload,
                        timeout=10
                    )

                    if response.status_code == 200:
                        print(f"✅ [{site_config['name']}] Comment #{idx} posted by {author}")
                        print(response.json() if response.headers.get('Content-Type') == 'application/json' else response.text[:200])
                    else:
                        print(f"❌ [{site_config['name']}] Failed ({response.status_code}) for {author}")
                        print(f"Response: {response.text[:200]}...")

                except Exception as e:
                    print(f"⚠️ [{site_config['name']}] Error for {author}: {str(e)}")

                delay = random.randint(5, 10)
                print(f"⏳ Waiting {delay} seconds before next comment...")
                time.sleep(delay)

    except FileNotFoundError:
        print(f"🚫 CSV file not found: {csv_file}")

def main():
    csv_file = 'comments.csv'  # Use the same CSV file
    post_comments(csv_file)

if __name__ == '__main__':
    main()
