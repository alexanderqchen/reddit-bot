import praw
import upvoteConfig
import os
import time

users = ["yoyashing", "NGNLBot"]

def bot_login():
    print("Logging in...")
    reddits = []
    for i in range(len(upvoteConfig.username)):
        print("Logging in " + upvoteConfig.username[i] + "...")
        reddits.append(praw.Reddit(client_id=upvoteConfig.client_id[i],
                     client_secret=upvoteConfig.client_secret[i],
                     password=upvoteConfig.password[i],
                     user_agent="upvotebot",
                     username=upvoteConfig.username[i]))
        try:
            reddits[i].user.me()
        except:
            print("Unsuccessful login for " + upvoteConfig.username[i])
            quit()
    print("All logins successful!\n")
    return reddits

def run_bot(reddits, comments_replied_to):
    for user in users:
        print("Obtaining all comments by " + user)
        upvoted = 0;
        newComments = []
        for reddit in reddits:
            for comment in reddit.redditor(user).comments.new(limit=None):
                if comment not in comments_upvoted:
                    comment.upvote()
                    upvoted += 1
                    if comment.id not in newComments:
                        newComments.append(comment.id)
                    print("* * * Upvoted comment " + comment.id)
                    print("......Sleeping for 2 seconds......")
                    time.sleep(2)
        comments_upvoted.extend(newComments)
        with open("comments_upvoted.txt", "a") as f:
            for comment in newComments:
                f.write(comment + "\n")
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

reddits = bot_login()
comments_upvoted = get_saved_comments()

while True:
    run_bot(reddits, comments_upvoted)
    print("......Sleeping for 5 seconds......\n")
    time.sleep(5)
