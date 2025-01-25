from flask import Flask, render_template, request, send_file
from funcs import encode_image, decode_image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
    if 'image' not in request.files:
        return "No file uploaded!", 400
    image = request.files['image']
    data = request.form['data']
    output_path = os.path.join(UPLOAD_FOLDER, 'encoded.png')
    input_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(input_path)
    encode_image(input_path, data, output_path)
    return send_file(output_path, as_attachment=True)

@app.route('/extract', methods=['POST'])
def extract():
    if 'image' not in request.files:
        return "No file uploaded!", 400
    image = request.files['image']
    input_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(input_path)
    try:
        hidden_data = decode_image(input_path)
        return f"Hidden Data: {hidden_data}"
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)