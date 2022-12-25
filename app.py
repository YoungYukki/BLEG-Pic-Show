from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    folds = os.listdir('.')
    return render_template('folds.html', folds = folds)

@app.route('/<fold>')
def image(fold):
    files = os.listdir(f'./{fold}')
    return render_template('files.html', files=files, fold=fold)

if __name__ == '__main__':
    app.run(debug=True)