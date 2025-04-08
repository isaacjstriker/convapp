from flask import Flask, request, render_template, send_file
import os
from converters.google_to_csv import convert_google_sheet_to_csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and file.filename.endswith('.xlsx'):
        output_file = convert_google_sheet_to_csv(file)
        return send_file(output_file, as_attachment=True)
    return "Invalid file format", 400

if __name__ == '__main__':
    app.run(debug=True)