from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import pandas as pd
import time

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  driver.get(YOUTUBE_TRENDING_URL)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')
  
  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

  duration_div = video.find_element(By.ID, 'overlays')
  duration = duration_div.find_element(By.TAG_NAME, 'span').text

  channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel_name = channel_div.text


  views_and_upload_div = video.find_element(By.ID, 'metadata-line')
  views_and_upload_list = views_and_upload_div.find_elements(By.TAG_NAME, 'span')
  views = views_and_upload_list[0].text
  uploaded = views_and_upload_list[1].text

  description = video.find_element(By.ID, 'description-text').text

  return {
    'title' : title,
    'url' : url,
    'thumbnail_url' : thumbnail_url,
    'duration' : duration,
    'channel_name' : channel_name,
    'views' : views,
    'uploaded' : uploaded,
    'description' : description
  }
  


if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()

  print('Fetching trending videos')
  videos = get_videos(driver)
  
  print('Found {} videos'.format(len(videos)))

  # title, url, thumbnail_url, channel, views, uploaded, description
  print('Parsing top 20 video')
  videos_data = [parse_video(video) for video in videos[:20]]
  
  print('Save the data to a CSV')
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv('trending.csv')