# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Routing
@app.route('/')
def index():
    title = "会話補助アプリ"
    message = "routing test"
    return render_template('index.html',
                           message=message, title=title)

@app.route('/post',methods=['POST', 'GET'])
def post():
  return render_template('conversation.html',message='in a conversation')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
