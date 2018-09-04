from flask import Flask, render_template, request
from ranker.main import main, file_to_link
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('search.html')


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    initial_time = time.time()
    search_results = main("../indexer/index", search_term.lower())
    res = [(file_to_link(os.path.join(b"../indexer/raw", path)), sim) for (path, sim) in search_results]
    elapsed_time = time.time() - initial_time
    num_results = len(search_results)
    return render_template("results.html", res=res, elapsed_time=elapsed_time, num_results=num_results)
