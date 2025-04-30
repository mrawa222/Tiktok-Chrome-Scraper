import asyncio
from datetime import datetime
import re
import pandas as pd
from pytz import timezone, utc
from playwright.async_api import async_playwright
import time

USERNAME = "insertthename" # Here insert the TikTok name that is after @
SCROLL_TIMES = 100 # the amount of scrolls that the scraper will do, test first with a smaller ammount
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Update to your Chrome .exe path
CHROME_PROFILE = "Profile X"  # Update to your chrome profile
USER_DATA_DIR = "C:/Users/Admin/AppData/Local/Google/Chrome/User Data"  # Update to your actual user data path

def decode_timestamp_from_id(video_id: str) -> dict:
    video_id_int = int(video_id)
    timestamp = (video_id_int >> 32) & 0x7FFFFFFF  # Mask to get the first 31 bits
    dt_utc = datetime.utcfromtimestamp(timestamp).replace(tzinfo=utc)
    cet = timezone('Europe/Warsaw')
    dt_cet = dt_utc.astimezone(cet)
    return {
        "utc": dt_utc.strftime('%Y-%m-%d %H:%M:%S'),
        "local": dt_cet.strftime('%Y-%m-%d %H:%M:%S')
    }

async def scrape_video_links():
    video_links = []
    profile_url = f"https://www.tiktok.com/@{USERNAME}"

    async with async_playwright() as p:
        print("Launching Chrome an a user profile")
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False,
            args=[f"--profile-directory={CHROME_PROFILE}"]
        )

        page = await browser.new_page()
        print(f"\U0001F50E Navigating to profile: {profile_url}")
        await page.goto(profile_url)

        print("Solve the CAPTCHA or log in if required. You have 60 seconds")
        time.sleep(60)  

        for i in range(SCROLL_TIMES):
            print(f"\U0001F4DC Scrolling... {i + 1}/{SCROLL_TIMES}")
            await page.mouse.wheel(0, 5000)
            await asyncio.sleep(3)

        anchors = await page.query_selector_all("a")
        for a in anchors:
            href = await a.get_attribute("href")
            if href and "/video/" in href and href not in video_links:
                video_links.append(href)

        await browser.close()

    return video_links

async def get_engagement_metrics(page, url): # Code for engagement metrics
    try:
        await page.goto(url)
        await page.wait_for_selector('strong[data-e2e="like-count"]', timeout=10000)

        like_button = page.locator('[data-e2e="like-count"]').first
        comment_button = page.locator('[data-e2e="comment-count"]').first
        share_button = page.locator('[data-e2e="share-count"]').first

        likes = await like_button.inner_text()
        comments = await comment_button.inner_text()
        shares = await share_button.inner_text()

        return likes, comments, shares
    except Exception as e:
        print(f"Error fetching metrics for {url}: {e}") # When the program fails to fetch metrics
        return None, None, None

async def main():
    print("Starting scrape and date extraction")
    video_links = await scrape_video_links()

    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False,
            args=[f"--profile-directory={CHROME_PROFILE}"]
        )
        page = await browser.new_page()

        for link in video_links:
            video_id_match = re.search(r"/video/(\d+)", link)
            if video_id_match:
                video_id = video_id_match.group(1)
                post_dates = decode_timestamp_from_id(video_id)
                likes, comments, shares = await get_engagement_metrics(page, link)
                results.append({
                    "Video URL": link,
                    "Post Date (UTC)": post_dates["utc"],
                    "Post Date (Local - CET/CEST)": post_dates["local"],
                    "Likes": likes,
                    "Comments": comments,
                    "Shares": shares
                })
            else:
                print(f"Invalid video URL: {link}") # Displayed if the programe fails to access scrapet video link

        await browser.close()

    df = pd.DataFrame(results)
    df.to_excel("tiktok_video_dates_with_metrics.xlsx", index=False) # change here the name of a final file
    print("Saved to tiktok_video_dates_with_metrics.xlsx")

if __name__ == "__main__":
    asyncio.run(main())
