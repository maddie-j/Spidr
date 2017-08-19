from flask import Flask, request, redirect, render_template
import requests
import base64
import api_auth

app = Flask(__name__)

@app.route('/')
def root():
    print("HELLO")
    return render_template('upload.html')

@app.route('/identify', methods=['POST'])
def spider():

    if 'image' not in request.files:
        return redirect(request.url)

    img = request.files['image'].read()


    auth = (api_auth.USER, api_auth.PASS)
    uploaded_task = requests.post(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
        data = {
            'service': 'tagging1',
            'image': base64.b64encode(img)
        },
        auth = auth
    )

    resp = uploaded_task.json()

    print("IMAGE ID:{}".format(resp['id']))

    scan_task = requests.put(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/run/{}'.format(resp['id']),
        data = {
            "scanned": True
        },
        auth = auth
    )

    resp = scan_task.json()

    desc = resp['description'].split(',')
    print(resp)
    confidence = [int(a) for a in resp['confidence'].split(',')]

    return 'description: {}, confidence: {}'.format(desc, confidence)


app.run(debug=True)
