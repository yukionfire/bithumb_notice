# Bithumb Listing Announcement Scraper

This Python script is designed to scrape and collect listing announcements from the Bithumb cryptocurrency exchange.

## Features

- Scrapes listing announcements from Bithumb's notice page
- Filters announcements from the past year
- Extracts key information such as coin name, deposit time, withdrawal time, and trading start time
- Saves results in a formatted Markdown file

## Requirements

- Python 3.6+
- Required libraries: requests, beautifulsoup4

## Installation

1. Ensure Python 3.6+ is installed on your system.
2. Install required libraries:
```bash
pip install requests beautifulsoup4
```

## Usage

1. Run the script:
```bash
python bithumb_scraper.py
```
2. The script will start scraping Bithumb's announcement page.
3. Progress will be displayed in the console.
4. Once completed, results will be saved in a Markdown file named `bithumb_listings_YYYYMMDD_HHMMSS.md` in the same directory.

## Output

The script generates a Markdown file containing:
- Announcement title
- Publication date
- Coin name
- Deposit opening time
- Withdrawal opening time
- Trading start time
- Link to the original announcement

## Notes

- The script uses random delays and rotates user agents to mimic human behavior.
- It's designed to stop after encountering a certain number of old announcements or reaching a maximum page limit.
- Please use responsibly and in accordance with Bithumb's terms of service.

## Disclaimer

This script is for educational purposes only. Users are responsible for ensuring their use of this script complies with Bithumb's terms of service and local laws.