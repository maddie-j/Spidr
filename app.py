from flask import *
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

    if 'upload' not in request.files:
        return redirect(request.url)

    img = request.files['upload'].read()


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

@app.route('/result')
def dummy() :
    info = {
        'name': 'Scary', 
        'danger': 'Will kill you within 24 hours. Call 000.  NOW!', 
        'image': url_for("images", filename='Scary'),
        'uploaded': request.files['image'].read()
    }

    return render_template("result.html", info=info)


app.run(debug=True)
