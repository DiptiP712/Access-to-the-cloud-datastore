import datetime
from google.cloud import datastore
from flask import Flask, render_template

app = Flask(__name__)
datastore_client = datastore.Client()


def store_time():
    dt = datetime.datetime.now()
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({'timestamp': dt})
    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']
    times = query.fetch(limit=limit)
    return times


@app.route('/')
def root():
    store_time()
    times = fetch_times(10)
    return render_template('index.html', times=times)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
