from flask import Flask, jsonify, render_template, request, redirect, url_for,send_file
import os
import random
from DirectTest import predict_image
from SaveRecords import save_to_csv
from CSV_To_Excel import csv_to_excel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

@app.route('/')
def index():
    return render_template('index.html')
def generate_random_filename():
    return ''.join(str(random.randint(0, 9)) for _ in range(8)) + ".jpg"

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return "Error"

        file = request.files['file']
        if file.filename == '':
            return "Error"

        random_filename = generate_random_filename()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], random_filename)

        # Stream and save the file in chunks
        chunk_size = 4096  # You can adjust the chunk size based on your needs
        with open(file_path, 'wb') as f:
            while True:
                chunk = file.stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)

        return random_filename
    except Exception as e:
        print("Error:", e)
        return f"Error Happened: {str(e)}"


@app.route('/file/<filename>')
def get_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404

@app.route('/predict',methods= ["post"])
def predictImage():
    imgName = request.json.get('imageName')
    classCode = request.json.get('classCode')
    print(imgName)
    print(request.json)
    imgName = imgName.split("/")[-1]
    output = predict_image(imgName)
    saveCSV = save_to_csv(classCode,output['labels'])
    return jsonify(output['data'])


@app.route('/downloadSheet', methods=['POST'])
def download_sheet():
    try:
        # Get the sheet name from the request
        csv_name  = request.form.get('classCode')

        csv_to_sheet = csv_to_excel(csv_name+".csv")

        sheet_name = csv_name 

        # Assume the sheets are stored in the '/sheets' directory
        sheets_dir = os.path.join(os.getcwd(), 'Sheets')

        # Construct the file path for the requested sheet
        file_path = os.path.join(sheets_dir, f"{sheet_name}.xlsx")
        print(file_path)
        # Check if the file exists
        if os.path.exists(file_path):
            # Send the file as a response
            return send_file(file_path, as_attachment=True)
        else:
            return "Sheet not found", 404

    except Exception as e:
        print(f"Error: {e}")
        return "Internal Server Error", 500


@app.route('/downloadCSV', methods=['POST'])
def download_csv():
    try:
        # Get the CSV file name from the request
        csv_filename = request.form.get('classCode')

        # Assume the CSV files are stored in the '/Records' directory
        records_dir = os.path.join(os.getcwd(), 'Records')

        # Construct the file path for the requested CSV file
        csv_path = os.path.join(records_dir, f"{csv_filename}.csv")

        # Check if the file exists
        if os.path.exists(csv_path):
            # Send the file as a response
            return send_file(csv_path, as_attachment=True)
        else:
            return "CSV file not found", 404

    except Exception as e:
        print(f"Error: {e}")
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
