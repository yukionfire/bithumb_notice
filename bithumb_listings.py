import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import random

def parse_korean_date(date_string):
    date_parts = re.findall(r'\d+', date_string)
    return datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
    ]
    return random.choice(user_agents)

def get_headers():
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

def fetch_bithumb_listings():
    url = "https://feed.bithumb.com/notice"
    one_year_ago = datetime.now() - timedelta(days=365)
    
    listing_notices = []
    page = 1
    old_notice_count = 0
    max_old_notices = 5  # Stop after encountering 5 consecutive old notices
    max_pages = 10  # Scrape a maximum of 10 pages

    while page <= max_pages:
        headers = get_headers()
        response = requests.get(f"{url}?page={page}", headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        notices = soup.select('li[class^="ContentList_notice-list"]')
        
        print(f"--- Page {page} ---")
        print(f"Found {len(notices)} notices")
        
        for i, notice in enumerate(notices, 1):
            print(f"\nNotice {i}:")
            print(notice.prettify())
            
            time.sleep(random.uniform(1, 3))
            
            title = notice.select_one('strong[class^="ContentList_title"]').text.strip()
            date_string = notice.select_one('span[class^="ContentList_date"]').text.strip()
            notice_date = parse_korean_date(date_string)
            
            if notice_date < one_year_ago:
                old_notice_count += 1
                if old_notice_count >= max_old_notices:
                    return listing_notices
                continue
            else:
                old_notice_count = 0  # Reset counter

            if re.search(r'(상장|추가|신규)', title):
                link = "https://feed.bithumb.com" + notice.find('a')['href']
                
                detail_response = requests.get(link, headers=get_headers())
                detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                
                content = detail_soup.find('div', class_='notice_content').text
                coin_match = re.search(r'$$(.*?)$$', title)
                coin = coin_match.group(1) if coin_match else "Unknown"
                
                deposit_time = re.search(r'입금\s*:\s*([\d]{4}년\s*[\d]{1,2}월\s*[\d]{1,2}일\s*[\d]{2}:[\d]{2})', content)
                withdrawal_time = re.search(r'출금\s*:\s*([\d]{4}년\s*[\d]{1,2}월\s*[\d]{1,2}일\s*[\d]{2}:[\d]{2})', content)
                trading_time = re.search(r'거래\s*:\s*([\d]{4}년\s*[\d]{1,2}월\s*[\d]{1,2}일\s*[\d]{2}:[\d]{2})', content)
                
                listing_notices.append({
                    'title': title,
                    'link': link,
                    'date': date_string,
                    'coin': coin,
                    'deposit_time': deposit_time.group(1) if deposit_time else "Not specified",
                    'withdrawal_time': withdrawal_time.group(1) if withdrawal_time else "Not specified",
                    'trading_time': trading_time.group(1) if trading_time else "Not specified"
                })
            
            print(f"Processed notice: {title}")
        
        if not notices:
            print("No more notices found, stopping scraping")
            break
        
        page += 1
    
    return listing_notices

def save_to_markdown(listings):
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"bithumb_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Bithumb Listing Announcements (Generated: {today})\n\n")
        
        for listing in listings:
            f.write(f"## {listing['title']}\n\n")
            f.write(f"- Publication Date: {listing['date']}\n")
            f.write(f"- Coin: {listing['coin']}\n")
            f.write(f"- Deposit Opening Time: {listing['deposit_time']}\n")
            f.write(f"- Withdrawal Opening Time: {listing['withdrawal_time']}\n")
            f.write(f"- Trading Start Time: {listing['trading_time']}\n")
            f.write(f"- Link: [{listing['link']}]({listing['link']})\n\n")
        
        f.write(f"\n\n*This document was automatically generated on {today}*")
    
    print(f"Results saved to {filename}")

print("Starting to scrape Bithumb announcements...")
listings = fetch_bithumb_listings()
print(f"Scraped {len(listings)} relevant announcements")
save_to_markdown(listings)
print("Scraping completed")