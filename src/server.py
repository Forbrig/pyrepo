from flask import Flask, render_template, abort, jsonify, request, redirect, url_for
import json, requests

from model import db, save_db

app = Flask(__name__)

github_name = "Forbrig"
repos = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/repository')
def repositories():
    # repo = db
    repos = json.loads(requests.get('https://api.github.com/users/'+github_name+'/repos').content.decode('utf-8'))
    return render_template('repositories.html', author = github_name, repos = repos)

@app.route('/repository/<string:index>')
def repository(index):
    try:
        # repo = db[index]
        # return render_template('repository.html', repo = repo, index = index, max_index = len(db) - 1)

        repo = json.loads(requests.get('https://api.github.com/repos/'+github_name+'/'+index).content.decode('utf-8'))
        print(repo)
        return render_template('repository.html', repo = repo, index = 0, max_index = 123456)
    except IndexError:
        abort(404)

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

# @app.route('/github')
# def get_github():
#     return requests.get('https://api.github.com/users/'+github_name+'/repos').content

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