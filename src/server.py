from flask import Flask, render_template, abort, jsonify, request, redirect, url_for
import json, requests, datetime
# import base64

from model import db, save_db

app = Flask(__name__)

github_name = ""
repos = []

@app.route('/', methods=["GET", "POST"])
def home():
    global github_name
    message = ""
    if request.method == "POST":
        github_name = request.form['username']
        user_data = json.loads(requests.get('https://api.github.com/users/'+github_name).content.decode('utf-8'))
        if "message" in user_data:
            message = user_data["message"]
            user_data = None
    else:
        user_data = json.loads(requests.get('https://api.github.com/users/'+github_name).content.decode('utf-8'))
        if "message" in user_data:
            message = user_data["message"]
            user_data = None

    return render_template('home.html', user = user_data, message = message)

@app.route('/repository')
def repositories():
    # repo = db
    global repos
    global github_name

    if github_name != "":
        repos = json.loads(requests.get('https://api.github.com/users/'+github_name+'/repos').content.decode('utf-8'))
        if "message" in repos:
            return redirect(url_for("home", user = None))
        else:
            return render_template('repositories.html', author = github_name, repos = repos, total = str(len(repos)))
    else:
        return redirect(url_for("home", user = None))


@app.route('/repository/<int:index>')
def repository(index):
    try:
        global repos
        repo = repos[index]
        # return render_template('repository.html', repo = repo, index = index, max_index = len(repos) - 1)

        # repo = json.loads(requests.get('https://api.github.com/repos/'+github_name+'/'+index).content.decode('utf-8'))
        
        # repo["created_at"] = datetime.datetime.strptime(repo["created_at"].replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
        # readme = json.loads(requests.get('https://api.github.com/repos/'+github_name+'/'+index+'/readme').content.decode('utf-8'))
        # print(readme)
 
        return render_template(
            'repository.html', repo = repo, index = index, max_index = len(repos) - 1)
    except IndexError:
        abort(404)

@app.route('/remove_user')
def remove_user():
    global github_name
    global repos
    github_name = ""
    repos = []
    return redirect(url_for("home", user = None))

@app.route('/add_repository', methods=["GET", "POST"])
def add_repository():
    if request.method == "POST":
        repo = {
            "title": request.form['title'],
            "author": request.form['author']
        }
        db.append(repo)
        save_db()
        return redirect(url_for("repository", index = len(db) - 1))
    else:
        return render_template('add_repository.html')

################## SERVING AS API ####################

@app.route('/api/repository')
def api_repositories():
    return jsonify(db)

@app.route('/api/repository/<int:index>')
def api_repository(index):
    try:
        repo = db[index]
        return repo
    except IndexError:
        abort(404)

if __name__ == '__main__':
    app.run()