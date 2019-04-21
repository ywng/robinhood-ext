from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

# Test api call
@app.route('/test', methods=['get'])
def get_test():
    return 'The server is up and running.'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
