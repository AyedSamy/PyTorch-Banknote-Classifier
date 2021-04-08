import os
import numpy as np
from flask import Flask, render_template, request, flash, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from get_prediction import get_prediction
from transform_image import transform_image

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

@app.route('/predict/<filename>')
def predict(filename):
    #tensor = transform_image('5-euro-paper.jpg')
    tensor = transform_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # delete the uploaded image after transforming it into a tensor
    if type(tensor) == str: # send the error message if the transformation couldn't be done
        return "Error: " + tensor
    else:
        prediction, probabilities = get_prediction(tensor)
        probabilities = [round(d,4) for d in probabilities.tolist()]
        return render_template('prediction.html', prediction=str(prediction), probabilities=probabilities)
        #return str(prediction) + ' ' + str(probabilities.numpy())

@app.route('/upload', methods=['POST'])
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
            #return redirect(url_for('uploaded_file', filename=filename))
            return redirect(url_for('predict', filename=filename))
        
        return redirect(url_for("home"))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)