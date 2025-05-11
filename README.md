# Tiktok-Chrome-Scraper
A Python script that scrapes TikTok video URLs, extracts their post dates (and converts them into CET time), and gathers engagement metrics (likes, comments, shares) using a Chrome user profile and Playwright automation.

Requirements:
- Python 3.8+
- Google Chrome (desktop installation)
- A valid Chrome user profile with access to TikTok

Installed Python packages:
- playwright
- pandas
- pytz
- asyncio
- openpyxl
  
Due to TikTok limitations caused by the anti-botting measures, the only way to scrape the videos from TikTok is to mimic the manual scraping done on the normal version of Google Chrome. Therefore, before running the script, you need to set up a new profile in the Chrome browser and log in to the TikTok account on it. You can check your path for Chrome and the profile under chrome://version/ in the Chrome browser

Before running the program, install dependencies:

pip install pandas pytz openpyxl playwright
playwright install

Configuration (before running change those):

USERNAME = "insertthename" # Here insert the TikTok name that is after @

SCROLL_TIMES = 100 # the number of scrolls that the scraper will do, test first with a smaller amount

CHROME_PATH = "C:/example"  # Update to your Chrome .exe path

CHROME_PROFILE = "Profile X"  # Update to your chrome profile

USER_DATA_DIR = "C:/example"  # Update to your actual user data path


and


df.to_excel("tiktok_video_dates_with_metrics.xlsx", index=False) # change here the name of a final file

print("Saved to tiktok_video_dates_with_metrics.xlsx")



Usage/Run this script:

python tiktok_scraper_example.py

What it does:
- Opens a Chrome window with your profile.

- Waits 60 seconds for manual login or CAPTCHA resolution.

- Scrolls through the profile to load videos.

- Collects links, fetches engagement data, and saves to: tiktok_video_dates_with_metrics.xlsx


Notes:

- This script mimics human interaction using your actual Chrome profile. Use responsibly.
- TikTok may change its structure at any time, which could break the code.
- Avoid scraping accounts at a large scale without previous permission to not break the TikTok terms of service.

Acknowledgments:
- This project was developed with assistance from Chatgpt, an AI language model by OpenAI.
- Parts of the code regarding decoding the dates from the TikTok URL were based on the research and work of Trevor Fox. Please visit his webpage to understand the logic behind it: https://trevorfox.com/tools/tiktok-video-date-extractor/
