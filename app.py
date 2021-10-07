from flask import Flask, render_template, jsonify, Response, request
import json

app = Flask(__name__)

def getUsers():
    with open('./users.json', 'r') as f:
        users = f.read()
    return users

def getPosts():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return posts

@app.route('/')
def index_view():
    username = request.args.get('username')
    users = json.loads(getUsers())
    if username in users:
        tweets = {}
        #listoftweets = []
        connected_users = users[username]
        posts = json.loads(getPosts())
        tweets[username] = posts[username]
        for user in connected_users:
            tweets[user] = posts[user]

        sorted_tweets = []
        for user in tweets:
            for t in tweets[user]:
                sorted_tweets.append(Tweets(user, t["status"], t["time"]))

        sorted_tweets.sort(key=lambda t: t.time, reverse=True)

        return render_template('index.html', username = username, tweets = sorted_tweets)
    return render_template('index.html', username = username)

@app.route('/users')
def users_view():
    return Response(getUsers(), mimetype="application/json")

@app.route('/posts')
def posts_view():
    return Response(getPosts(), mimetype="application/json")

class Tweets:
    def __init__(self, user, status, time) :
        self.user = user
        self.status = status
        self.time = time
        

if __name__ == '__main__':
    app.run(host='127.0.0.1')