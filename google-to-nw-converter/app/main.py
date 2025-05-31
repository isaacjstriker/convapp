from flask import Flask, request, render_template, send_file
from converters.google_to_csv import convert_map_to_nw_format
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    #google_sheet_url = request.form.get('google_sheet_url')
    uploaded_file = request.files.get('file')
    territory_number = request.form.get('territory_number')
    
    # Add google_sheet_url validation back in later:
    # if not google_sheet_url

    if not uploaded_file or not territory_number:
        return "Missing required fields", 400
    
    try:
        input_file_path = "uploaded_map.xlsx"
        uploaded_file.save(input_file_path)
        # Convert the Google Sheet to CSV
        output_file = "output.csv"
        convert_map_to_nw_format(input_file_path, output_file, territory_number)
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)