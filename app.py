from flask import Flask, render_template, request, abort, make_response, jsonify, flash, redirect
from werkzeug.utils import secure_filename
import os
import tempfile
import prediction

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
# app.config['UPLOAD_FOLDER'] = "F:/Imagenes/"
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.errorhandler(413)
def too_large(e):
    return make_response(jsonify(message="File is too large"), 413)

@app.route('/')
def home():
    return render_template('ejemplo.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Here you should save the file
            # file.save("F:/Imagenes")
            file_path = file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
            # return 'File uploaded successfully'
        try:
            predict = prediction.getPrediction(file_path)
            flash(predict)
            return redirect('/')
        except Exception as error:
            print("Error:", error)
            return {'error': str(error)}, 500

    return 'No file uploaded'

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 80)