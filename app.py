import sys

from LanguageModels import models
from input import input

import json
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def default():
    return render_template('default.html')


@app.route('/', methods=['POST'])
def analyze():
    dump = json.dumps(dict(request.form))
    raw_data = json.loads(dump)
    data = raw_data['file_content'][0]

    model_input = input(data)

    model_id = ""
    model_result = 0

    for model in models:

        eval = model.evaluateInput(model_input)
        if (model_result < eval):
            model_id = model.id
            model_result = eval

    return model_id

@app.route('/about')
def about():
    return render_template('about.html')

def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)