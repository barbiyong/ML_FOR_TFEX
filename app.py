# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
from runtime import run
app = Flask(__name__, static_url_path='')


@app.route('/', methods=['GET'])
def main():
    function_name = request.args.get('function_name')
    if function_name == 'LP':
        message = run(function_name)
        print(message)
        message = {
            "messages": [
                {"text": message}
            ]
        }
        return jsonify(message)
    elif function_name == 'NOW':
        message = run(function_name)
        print(message)
        message = {
            "messages": [
                {"text": u" LAST PREDICT !! "}
            ]
        }
        return jsonify(message)
    else:
        message = {
            "messages": [
                {"text": u" NOT HAVE THIS FEATURE ! "}
            ]
        }
        return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)

