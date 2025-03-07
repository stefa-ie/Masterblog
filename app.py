from flask import Flask, request, render_template, redirect, url_for
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


@app.route('/', methods=['GET'])
def index():
    blog_posts = load_blog_posts()
    print(blog_posts)
    return render_template('index.html', posts=blog_posts)

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

def fetch_post_by_id(post_id):
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post_id == post['id']:
            return post
        None

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    # Update the post in the JSON file
    if request.method == 'POST':
        post['author'] = request.form.get('author', post['author'])
        post['title'] = request.form.get('title', post['title'])
        post['content'] = request.form.get('content', post['content'])
        save_blog_posts(load_blog_posts())
        # Redirect back to index
        return redirect('/')

    return render_template('update.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_blog_posts()
    post_to_delete = fetch_post_by_id(post_id)
    if post_to_delete:
        blog_posts.remove(post_to_delete)
        save_blog_posts(blog_posts)
    return redirect('/')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)