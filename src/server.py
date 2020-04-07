from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    posts = [
                {'title': 'Post 1', 'author': 'Vitor'},
                {'title': 'Post 2', 'author': 'Guilherme'},
                {'title': 'Post 2', 'author': 'Guilherme'},
                {'title': 'Post 2', 'author': 'Guilherme'},
                {'title': 'Post 2', 'author': 'Guilherme'},
            ]
    return render_template('blog.html', author = "Vitor Forbrig", posts = posts)

if __name__ == '__main__':
    app.run()