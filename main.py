from flask import Flask, render_template, request, jsonify
from dashboard import get_dashboard_data

app = Flask(__name__)

# Dashboard
@app.route('/api/data/dashboard', methods=["POST"])
def api_dashboard_data():
    username = request.form['username']
    password = request.form['password']  
    return jsonify(get_dashboard_data(username, password))

@app.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)