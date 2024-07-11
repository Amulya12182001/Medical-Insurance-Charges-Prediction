# Import necessary modules (Python standard library only)
import http.server
import socketserver
import json

# Load the model from file
Pkl_Filename = "rf_tuned.pkl" 
with open(Pkl_Filename, 'rb') as file:  
    model = pickle.load(file)

# Define the prediction function
def predict(features):
    try:
        # Assuming features are passed as a list of integers
        final = [features]  # Reshape not needed for single sample prediction
        pred = model.predict(final)[0]
        if pred < 0:
            return 'Error calculating Amount!'
        else:
            return f'Expected amount is {pred:.3f}'
    except Exception as e:
        return str(e)

# Define the HTTP request handler
class PredictionHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        features = json.loads(post_data.decode('utf-8'))
        
        prediction = predict(features)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(prediction.encode('utf-8'))

# Set up the HTTP server
def run(server_class=http.server.HTTPServer, handler_class=PredictionHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

# Run the server
if __name__ == "__main__":
    run()






'''from flask import Flask, request, url_for, redirect, render_template
import pickle

import numpy as np

app = Flask(__name__, template_folder='./templates', static_folder='./static')

Pkl_Filename = "rf_tuned.pkl" 
with open(Pkl_Filename, 'rb') as file:  
    model = pickle.load(file)
@app.route('/')

def hello_world():
    return render_template('home.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    features = [int(x) for x in request.form.values()]

    print(features)
    final = np.array(features).reshape((1,6))
    print(final)
    pred = model.predict(final)[0]
    print(pred)

    
    if pred < 0:
        return render_template('op.html', pred='Error calculating Amount!')
    else:
        return render_template('op.html', pred='Expected amount is {0:.3f}'.format(pred))

if __name__ == '__main__':
    app.run(debug=True)'''
