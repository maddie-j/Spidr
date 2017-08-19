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

    json_header = {'Content-Type': 'application/json'}

    auth = (api_auth.USER, api_auth.PASS)
    b64img = base64.b64encode(img).decode()

    data = '{"service":"%s","image":"%s"}'%('tagging2',b64img)

    uploaded_task = requests.post(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
        data = data,
        auth = auth,
        headers = json_header
    )

    print("UPLOADED")

    resp = uploaded_task.json()


    id = resp['task']['uri'].split('/')[-1]

    #print("IMAGE ID:{}".format(resp['id']))
    scan_task = requests.put(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/run/{}'.format(id),
        data = '{"scanned": true}',
        auth = auth,
        headers = json_header
    )

    print("SCANNED")

    resp = scan_task.json()['task']

    desc = resp['description']
    print(resp)
    confidence = resp['confidence']

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


app.run(debug=True, threaded=True)
