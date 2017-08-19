from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def root():
    return 'this is the root page with the upload photo button'

@app.route('/identify', methods=['POST'])
def spider():

    if 'image' not in request.files:
        return redirect(request.url)

    img = request.files['image']

    # TODO send image to api

    return 'spider classification page'

app.run()
