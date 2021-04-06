import os
from flask import Flask, render_template, request, flash, send_from_directory, redirect, url_for

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads\\images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config["SECRET_KEY"] = "iuhto743yto34iuho287gh78"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'filename' not in request.files:
            print("No file part")
            return redirect(url_for("home"))
        file = request.files['filename']
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(url_for("home"))
        print(file)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        
        return redirect(url_for("home"))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/predict')
def predict():
    if request.method == 'GET':
        default_name = 'John Doe'
        name = request.args.get("filename", default_name)
        return f'Hello from predict {name}'
    else:
        return 'Just hello no GET'

if __name__ == '__main__':
    app.run(debug=True)