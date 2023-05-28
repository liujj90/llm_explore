from flask import Flask, render_template, request, jsonify
import os
from scripts.pdfquery import QApipeline

app = Flask(__name__)

# Set the path for file uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the results list
results = []

# Function to process the uploaded file
def process_file(model):
    # Add your code here to process the uploaded file
    # You can call the function from main.py or write the processing code directly here
    query = "give me a concise summary of this document. suggest 2 points phrased as potential questions a reader may have for this document."
    result = model.run(query)
    return result



# Function to process user input
def process_user_input(model, user_input):
    # Add your code here to process the user input
    result = model.run(user_input)
    return result


# Route to the home page
@app.route('/')
def home():
    return render_template('index.html', results=[])

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file is selected in the request
    if 'file' not in request.files:
        return "No file selected."

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return "No file selected."

    # Save the uploaded file to the upload folder
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Process the uploaded file
    global qa_model 
    qa_model = QApipeline(filepath)
    result = process_file(qa_model)
    
    results.append(result)
    # Render the response in a new page
    # return jsonify({'results': results})
    return render_template('result_basic.html', result=result)

# Route to handle user input
@app.route('/user_input', methods=['POST'])
def user_input():
    user_input = request.form['input_text']

    # Process the user input and get the response
    result = process_user_input(qa_model, user_input)
    
    # Append the result to the results list
    results.append(result)
    return render_template('result_basic.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)