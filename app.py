from flask import Flask, render_template, abort
import os
import markdown

app = Flask(__name__)

ARTICLES_FOLDER = 'articles'

def get_articles():
    articles = []
    for filename in os.listdir(ARTICLES_FOLDER):
        if filename.endswith('.md'):
            path = os.path.join(ARTICLES_FOLDER, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                title = lines[0].replace('#', '').strip()
                preview = lines[1][:100] + '...'
                slug = filename.replace('.md', '')
                articles.append({'title': title, 'preview': preview, 'slug': slug})
    return articles

def get_article(slug):
    filepath = os.path.join(ARTICLES_FOLDER, slug + '.md')
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        html = markdown.markdown(content)
        return html

@app.route("/")
def homepage():
    articles = get_articles()
    return render_template("index.html", articles=articles)

@app.route("/article/<slug>")
def article(slug):
    content = get_article(slug)
    return render_template("article.html", content=content)

if __name__ == '__main__':
    app.run(debug=True)