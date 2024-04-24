from flask import Flask, request, make_response

app = Flask(__name__)


@app.post("/process-image")
def root():
    """Take the image and the operation.

    Returns:
        JSON: Processed image.
    """
