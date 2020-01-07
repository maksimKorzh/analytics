from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import Response
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://analytics:342124@analytics-knicw.mongodb.net/stats?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/')
def root():
    return render_template('stats.html')

@app.route('/api/post', methods=['POST'])
def post():
    response = Response('')
    response.headers['Access-Control-Allow-Origin'] = '*'

    stats = {
        'Date': request.form.get('date'),
        'Url': request.form.get('url'),
        'Agent':request.headers.get('User-Agent')
    }

    if request.headers.getlist("X-Forwarded-For"):
       stats['Ip'] = request.headers.getlist("X-Forwarded-For")[0]
    else:
       stats['Ip'] = request.remote_addr
    
    if request.headers.get('Origin'):
        stats['Origin'] = request.headers.get('Origin')
    else:
        stats['Origin'] = 'N/A'
    
    if request.headers.get('Referer'):
        stats['Referer'] = request.headers.get('Referer')
    else:
        stats['Referer'] = 'N/A'
    
    mongo.db.stats.insert_one(stats)
    return response


@app.route('/api/get')
def get():
    stats = []
    
    for stat in mongo.db.stats.find():
        stat['_id'] = str(stat['_id'])
        stats.append(stat)

    return jsonify({'data': stats})


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
