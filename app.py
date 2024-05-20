from flask import Flask, request, send_file, render_template
from flask import jsonify
import reportbro
import os
import datetime
from io import BytesIO
from uuid import uuid4


app = Flask(__name__,template_folder='templates')
REPORTS_DIR = './reports/'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/designer")
def designer():
    return render_template("designer.html")

@app.route('/report/run', methods=['POST', 'PUT'])
def get_create_report():
    # The data for the report is obtained from the POST request's JSON
    report_definition = request.get_json()["report"]
    data = request.get_json()["data"]

    # Generate report
    report = reportbro.Report(report_definition, data)
    report_pdf = report.generate_pdf()

    # Convert the PDF bytes to a BytesIO object
    report_file = BytesIO(report_pdf)

    # Write the report file to disk
    # Generate a unique filename
    filename = f"{uuid4().hex}"
    with open(os.path.join('./reports/', filename), 'wb') as f:
        report_file.seek(0)  # Move the file pointer to the beginning of the stream
        f.write(report_file.read())

    return "key:" +filename


@app.route('/report/run', methods=['GET'])
def get_report():
    #delete all files in the reports catalog that is older than one day
    # Get the current date and time
    current_time = datetime.datetime.now()

    # Calculate the time 5 min ago
    one_day_ago = current_time - datetime.timedelta(minutes=5)

    # Get a list of all files in the reports directory
    files = os.listdir('reports')

    # Iterate over the files and delete those that are older than one day
    for file in files:
        file_path = os.path.join('reports', file)
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        if file_time < one_day_ago:
            os.remove(file_path)

    key = request.args.get('key')
    filename = f"{key}"

    # Load the previously saved PDF file
    with open(os.path.join('reports', filename), 'rb') as f:
        pdf_file = f.read()

    return send_file(BytesIO(pdf_file), mimetype='application/pdf')


if __name__ == "__main__":
    os.makedirs(REPORTS_DIR, exist_ok=True)
    app.run(host='0.0.0.0', debug=True, port=5012) #, ssl_context=('cert.pem', 'key.pem'))
   # app.run(debug=True,port=5012)
