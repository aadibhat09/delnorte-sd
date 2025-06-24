from os import path

from flask import Flask, render_template
from flask_frozen import Freezer

template_folder = path.abspath('./wiki')

app = Flask(__name__, template_folder=template_folder)
# app.config['FREEZER_BASE_URL'] = environ.get('CI_PAGES_URL')
app.config['FREEZER_DESTINATION'] = 'public'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
freezer = Freezer(app)


@app.cli.command()
def freeze():
    freezer.freeze()


@app.cli.command()
def serve():
    freezer.run()


@app.route('/')
def home():
    with open('docs/home.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return render_template('base.html',
                           title='Home',
                           md_content=html_content)


@app.route('/<page>')
def pages(page):
    with open(f'docs/{page.lower()}.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return render_template('base.html',
                           title=page.title().replace('-', ' '),
                           md_content=html_content)


# Main Function, Runs at http://0.0.0.0:8080
if __name__ == "__main__":
    app.run(port=8080)
