# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
app = Flask(__name__, static_url_path='')


@app.route('/', methods=['GET'])
def main():
    return None


if __name__ == "__main__":
    app.run(debug=True)
