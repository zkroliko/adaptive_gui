from cameraSource import CameraSource
from flask import Flask

PORT_NUMBER = 8080


source = CameraSource()

app = Flask(__name__)

@app.route("/")
def hello():
    return str(source.get_ratio())

if __name__ == "__main__":
    app.run(port=PORT_NUMBER)