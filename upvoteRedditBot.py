import praw
import upvoteConfig
import os
import time

user = "yoyashing"

def bot_login():
    print("Logging in...")
    r = praw.Reddit(username = upvoteConfig.username, password = upvoteConfig.password, client_id = upvoteConfig.client_id, client_secret = upvoteConfig.client_secret, user_agent = "dog comment responder v1.0")
    print("Login successful!\n")
    return r

def run_bot(r, comments_replied_to):
    print("Obtaining all comments by " + user)
    upvoted = 0;
    for comment in r.redditor(user).comments.new(limit=None):
        if comment not in comments_upvoted:
            comment.upvote()
            upvoted += 1
            comments_upvoted.append(comment.id)
            with open("comments_upvoted.txt", "a") as f:
                f.write(comment.id + "\n")
            print("* * * Upvoted comment " + comment.id)
            print("......Sleeping for 2 seconds......")
            time.sleep(2)
    print("Upvoted " + str(upvoted) + " new comments by " + user + "\n")

def get_saved_comments():
    if not os.path.isfile("comments_upvoted.txt"):
        comments_upvoted = []
    else:
        with open("comments_upvoted.txt", "r") as f:
            comments_upvoted = f.read()
            comments_upvoted = comments_upvoted.split("\n")
            comments_upvoted = list(filter(None, comments_upvoted))
    return comments_upvoted

r = bot_login()
comments_upvoted = get_saved_comments()

while True:
    run_bot(r, comments_upvoted)
    print("......Sleeping for 5 seconds......\n")
    time.sleep(5)
