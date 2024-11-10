from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup, Comment
import sqlalchemy
import requests
from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, inspect
import re
from pytube import YouTube


def scrape():
    # url ='https://www.youtube.com/playlist?list=PLj5dR1tyJldkvdq8T51fgCQjlPGbLRej0'
    # options = Options() 
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0")
    # driver = webdriver.Chrome(options = options)
    # # Getting the origin url
    # try:
    #     driver.get(url)
    # except:
    #      print("URL Not working")
    # time.sleep(5)

    # page_source = driver.page_source
    # with open ("page_source.txt", "w", encoding='utf-8') as f:
    #     f.write(page_source)


    # time.sleep(10)
    # driver.close()

    # Read the page source from the file
    with open("page_source.txt", "r", encoding='utf-8') as f:
        page_source = f.read()

    # Parse the HTML content
    soup = BeautifulSoup(page_source, features="lxml")

    nav_links = []
    for link in soup.find_all('a', href=True):
        if re.search("ytd-playlist-video-renderer", str(link)):
            href = link.get('href')
            nav_links.append(href)

    print(len(nav_links))

    # pytube
    base_url = 'https://www.youtube.com'
    save_path = './videos'
    link_dict = []
    for item in range(len(nav_links)):
        link_dict.append(base_url + str(nav_links[item]))
    # print(link_dict)

    for item in range(len(link_dict)):
        try:
            r = requests.get(link_dict[item])
        except:    
            print("Error")
        if r.status_code == 200:
            try: 
            # object creation using YouTube 
                print(link_dict[item])
                yt = YouTube(link_dict[item]) 
                print("success")
            except Exception as e: 
                #to handle exception 
                print("Connection Error: {e}") 


            caption = yt.captions
            print(caption.xml_captions)
            # print(caption.generate_srt_captions())

            counter = 1
            with open("captions_" + str(counter), 'w') as f:
                f.write(str(link_dict[item]))
                f.write(caption)
                counter += 1

            # Get all streams and filter for mp4 files
            # mp4_streams = None
            # try:
            #     mp4_streams = yt.streams.filter(file_extension='mp4').all()
            # except Exception as e:
            #     print("Failed: Get all streams and filter for mp4 files", (e))

            # get the video with the highest resolution
            # d_video = mp4_streams[-1]
            # print(mp4_streams)

            # try: 
                # downloading the video 
                # d_video.download(output_path=save_path)
            #     # print('Video downloaded successfully!')
            # except: 
                # print("Some Error!")

y = scrape()
