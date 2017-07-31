import praw
import upvoteConfig
import os
import time
from random import randint

users = ["yoyashing", "NGNLBot", "notanupvotebot001", "notanupvotebot002", "notanupvotebot003", "notanupvotebot004", "notanupvotebot005"]

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
                    print("---Upvoted comment " + comment.id)
                    print("......Sleeping for 2 seconds......")
                    time.sleep(2)
        comments_upvoted.extend(newComments)
        with open("comments_upvoted.txt", "a") as f:
            for comment in newComments:
                f.write(comment + "\n")
        print("Upvoted " + str(int(upvoted/len(reddits))) + " new comments by " + user + "\n")

def get_saved_comments():
    if not os.path.isfile("comments_upvoted.txt"):
        comments_upvoted = []
    else:
        with open("comments_upvoted.txt", "r") as f:
            comments_upvoted = f.read()
            comments_upvoted = comments_upvoted.split("\n")
            comments_upvoted = list(filter(None, comments_upvoted))
    return comments_upvoted

def bot_comment(reddits, pos):
    commentOptions = ["OMG!! XD XD", "LMAOOO I'M DYING!! XD XD", "THIS IS GREAT!! XD", "This is my favorite!", "HAHAHAAHAHA", "LMAOOOO", "LOL", "That's crazy!", "totally agree", "That's amazing!", "OMG", "ummmmmmmm"]
    if pos >= len(reddits):
        pos = 0;
    comments = list(reddits[pos].subreddit('test').comments(limit=25))
    comment = comments[randint(0, len(comments)-1)]
    try:
        comment.reply(commentOptions[randint(0, len(commentOptions)-1)])
        print("---" + upvoteConfig.username[pos] + " replied to comment " + comment.id)
        return True;
    except praw.exceptions.APIException:
        print("* * * " + upvoteConfig.username[pos] + " failed to reply.")
        return False;

reddits = bot_login()
comments_upvoted = get_saved_comments()

count = 0;
upvoteTimeInterval = 60
commentTimeIntervals = []
for reddit in reddits:
    commentTimeIntervals.append(600)

while True:
    for i in range(len(commentTimeIntervals)):
        if count*upvoteTimeInterval % commentTimeIntervals[i] == 0:
            if bot_comment(reddits, i):
                commentTimeIntervals[i] -= 60
                print("---New comment time interval for " + upvoteConfig.username[i] + " is " + str(commentTimeIntervals[i]))
                print("......Sleeping for " + str(2) + " seconds......\n")
                time.sleep(2)
            else:
                commentTimeIntervals[i] *= 2
                print("---New comment time interval for " + upvoteConfig.username[i] + " is " + str(commentTimeIntervals[i]))
                print("......Sleeping for " + str(2) + " seconds......\n")
                time.sleep(2)
    run_bot(reddits, comments_upvoted)
    count += 1;
    print("......Sleeping for " + str(upvoteTimeInterval) + " seconds......\n")
    time.sleep(upvoteTimeInterval)
