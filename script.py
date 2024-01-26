from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import json



def scrape_tweets(user, username):
    url = f'https://twitter.com/{user}'

    # Setup the WebDriver (in this case, Chrome)
    # Retain cookies for login info
    options = webdriver.ChromeOptions()
    # options.add_argument('--user-data-dir=C:/Users/gabri/AppData/Local/Google/Chrome/User Data/Default')
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=options)

    # Navigate to the user's Twitter page
    driver.get(url)
        
    # Wait 5 secodns for the twitter popup
    # time.sleep(10)
    
    # Click the 'Not now' button
    # driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]').click()
    
    # Wait 12 seconds
    # time.sleep(15)
    # Wait for login to happen
    input()
    
    # # Click the 'Log in' button
    # driver.find_element(By.XPATH, '/html/body/div/div').click()
    # # Write "username" in the username field
    # driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/label/div/div[2]/div/input').send_keys('username')
    
    # Scroll down the page to load tweets (you may need to adjust the range and sleep time)
    for _ in range(0):  # Adjust the range as necessary
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)  # Adjust sleep time as necessary
    
    # Store ids of tweets to avoid duplicates
    ids = []
    
    num = 0
    
    while True:
        # Used to check if all the tweets have been seen
        all_seen = True
        
        # Find the tweets
        tweets = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section/div/div/div')
        
        # Iterate over all tweets
        for i, tweet in enumerate(tweets):
            try:
                # Skip tweets that have already been seen
                if tweet.id in ids:
                    all_seen = False
                    continue
                
                # Store the id of the tweet
                ids.append(tweet.id)
                
                # Only get tweets from the username, no retweets
                if tweet.text.startswith(username) and not tweet.text.startswith(username + ' reposted'):
                    # Skip ads
                    if "Ad" not in tweet.text:
                        # Get the text
                        try:
                            text = tweet.find_element(By.XPATH, './/div/div/article/div/div/div[2]/div[2]/div[2]/div').text
                        except:
                            text = ""
                        
                        # Get the number of likes
                        try:
                            likes = tweet.find_element(By.XPATH, './/div/div/article/div/div/div[2]/div[2]/div[4]/div/div/div[3]/div/div/div[2]/span/span/span').text
                        except:
                            likes = ""
                        
                        # Possible reply
                        try:
                            reply = tweet.find_element(By.XPATH, './/div/div/article/div/div/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div/span').text
                        except:
                            reply = ""
                            
                        # Skip tweets with no text
                        if not text == "":
                            # print(text, likes, reply)
                            
                            # Create a dictionary containing the tweet data
                            tweet_data = {
                                'text': text,
                                'likes': likes,
                                'reply': reply
                            }
                            
                            # Write the tweet data to a file
                            with open('tweets.txt', 'a', encoding='utf-8') as file:
                                file.write(json.dumps(tweet_data, ensure_ascii=False) + '\n')
                            num += 1
                    
                    
            except Exception as e:
                print(e)
            
            # Wait for a random time between 1 and 2 seconds
            time.sleep(1 + random.random())
            
            if num % 100 == 0:
                print("Number of tweets:", num)
            
            # Scroll to the next tweet
            if i < len(tweets) - 1:
                try:
                    driver.execute_script('arguments[0].scrollIntoView( { behavior: "smooth", block: "end" } );', tweets[i + 1])
                except:
                    pass
                
                
        # If all the tweets have been seen, scroll down a little
        if all_seen:
            time.sleep(5)
            driver.execute_script('window.scrollTo(0, window.scrollY + 100);')
            time.sleep(5)
        
            
        # # Move to the bottom most tweet with a smooth scroll
        # for i in range(len(tweets), -1, -1):
        #     try:
        #         driver.execute_script('arguments[0].scrollIntoView( { behavior: "smooth", block: "end" } );', tweets[-1])
        #         break
        #     except:
        #         pass

# Yan LeCun
scrape_tweets('ylecun', 'Yann LeCun')
# Elon Musk
# scrape_tweets('elonmusk', 'Elon Musk')