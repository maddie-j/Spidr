from flask import *
import requests
import base64
import api_auth
import json

app = Flask(__name__)

descriptions = {
    "huntsman": "This is a huntsman. Deal with it...",
    "red back": "This is a red back. RUN!",
    "funnel web": "idk about funnel webs",
    "mouse spider": "wtf. Mouse is not a spider... I think"
}

@app.route('/')
def root():
    return render_template('upload.html')

@app.route('/identify', methods=['POST'])
def spiderMob():

    if 'upload' in request.files:
        b64img = base64.b64encode(request.files['upload'].read()).decode()
        print(b64img)
    elif 'imageData' in request.form:
        b64img = request.form['imageData']

    json_header = {'Content-Type': 'application/json'}

    auth = (api_auth.USER, api_auth.PASS)

    data = '{"service":"%s","image":"%s"}'%('spiders',b64img)

    uploaded_task = requests.post(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
        data = data,
        auth = auth,
        headers = json_header
    )

    resp = uploaded_task.json()
    print(resp)

    id = resp['task']['uri'].split('/')[-1]

    scan_task = requests.put(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/run/{}'.format(id),
        data = '{"scanned": true}',
        auth = auth,
        headers = json_header
    )

    print(scan_task.text)
    resp = scan_task.json()['task']

    name = resp['description']
    confidence = float(resp['confidence'])

    data = {
        "name": name,
        "description": descriptions[name],
        "spider_img": "TODO"
    } 

    if confidence < 0.60:
        data = {
            "error": True
        }

    return render_template("result.html", **data)

@app.route('/result')
def dummy() :
    info = {
        'name': 'Scary', 
        'danger': 'Will kill you within 24 hours. Call 000.  NOW!', 
        'image': url_for("images", filename='Scary'),
        'uploaded': request.files['image'].read()
    }

    return render_template("result.html", info=info)


app.run(host='0.0.0.0', debug=True, threaded=True)
