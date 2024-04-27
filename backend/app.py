from flask import Flask, request, make_response
from image_processing import process_image

app = Flask(__name__)


@app.post("/process-image")
def image_processing_endpoint():
    """Take the image and the operation.

    Returns:
        PNG Image: Processed image.
    """
    image = request.files["image"]
    operation = request.form["operation"]
    result = process_image(image, operation)
    response = make_response(result)
    response.headers["Content-Type"] = "image/png"
    return response


@app.post("/ocr")
def ocr_endpoint():
    """Take the image and apply ocr.

    Returns:
        PNG Image: Processed image.
    """
    image = request.files["image"]
    result = ocr(image)
    response = make_response(result)
    return response
