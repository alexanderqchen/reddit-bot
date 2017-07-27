import praw
import config
import time

def bot_login():
    print("Logging in...")
    r = praw.Reddit(username = config.username, password = config.password, client_id = config.client_id, client_secret = config.client_secret, user_agent = "dog comment responder v1.0")
    print("Login successful!")
    return r

def run_bot(r):
    print("Obtaining 25 comments...")
    for comment in r.subreddit('test').comments(limit=25):
        if "dog" in comment.body:
            print('String with "dog" found in comment ' + comment.id)
            comment.reply("I also love dogs! [Here](https://www.cesarsway.com/sites/newcesarsway/files/styles/large_article_preview/public/Common-dog-behaviors-explained.jpg?itok=FSzwbBoi) is an image of one!")
            print("Replied to comment " + comment.id)
    print("Sleeping for 10 seconds")
    time.sleep(10)

while True:
    r = bot_login()
    run_bot(r)
