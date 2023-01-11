from flask import Flask, request, send_from_directory
from flask_cors import CORS

import json
import utils.utils as utils  

app = Flask(__name__)
CORS(app)

# Test
@app.route("/test", methods = ['GET'])
def Test():
    return json.dumps({"code": "200"})

@app.route('/api/upload', methods=["POST"])
def Upload():
    upload_file = request.files['file']
    filename = request.form.get('filename')
    coordinate = eval(request.form.get('coordinate'))
    utils.save_video(upload_file, filename, coordinate)
    return json.dumps({"code": "200"})

@app.route('/api/download', methods=["GET"])
def Download():
    return send_from_directory("output", "output.mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="9000", debug=True)