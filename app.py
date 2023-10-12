
from flask import Flask, request, jsonify
import PyPDF2
from io import BytesIO

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if file:
        try:
            pdf_reader = PyPDF2.PdfFileReader(BytesIO(file.read()))
            text = ""
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
            return jsonify({"text": text}), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == "__main__":
    app.run()
