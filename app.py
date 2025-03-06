from flask import Flask, request, render_template, redirect
import json
import os

app = Flask(__name__)

def load_blog_posts():
    file_path = 'blog_posts.json'
    if not os.path.exists(file_path):
        print(f"No such file: {file_path}")
        return []
    with open(file_path, 'r') as fobj:
        return json.load(fobj)


def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as fobj:
        json.dump(posts, fobj, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        blog_posts = load_blog_posts()
        return render_template('index.html', posts=blog_posts)
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_post = {
            "id": len(load_blog_posts()) + 1,
            "author": request.form.get('username', 'Anonymous'),
            "title": request.form.get('title', 'Untitled'),
            "content": request.form.get('content', 'No content')
        }
        blog_posts = load_blog_posts()
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect('/')
    return render_template('add.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)