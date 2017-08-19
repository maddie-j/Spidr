from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route('/')
def root():
    print("HELLO")
    return render_template('upload.html')

@app.route('/identify', methods=['POST'])
def spider():

    if 'image' not in request.files:
        return redirect(request.url)

    img = request.files['image']

    # TODO send image to api

    return 'TODO result.html'


app.run()
