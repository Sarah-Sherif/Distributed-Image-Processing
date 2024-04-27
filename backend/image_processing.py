import cv2
import numpy as np
from rembg import remove
# import easyocr


def edge_detection(image, threshold1=100, threshold2=200):
    """Return the edge map of the image."""
    result = cv2.Canny(image=image, threshold1=threshold1,
                       threshold2=threshold2, apertureSize=3, L2gradient=False)
    return result


def corner_detection(image):
    """Return the image with the corners/interest points highlighted."""
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect corners using Harris Corner Detection
    dst = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)

    # Threshold to highlight corners
    dst = cv2.dilate(dst, None)
    image[dst > 0.01 * dst.max()] = [0, 0, 255]  # Highlight corners in red

    return image


def gaussian_blur(image, kernel=5):
    """Return the blurred image."""
    result = cv2.GaussianBlur(image, (kernel, kernel), 0)
    return result


def median_blur(image, kernel=5):
    """Return the blurred image"""
    result = cv2.medianBlur(image, ksize=kernel)
    return result


def fourier_transform(image):
    """Return the centered fourier transform of the image."""
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image

    # Get the optimal size for the Fourier transform
    rows, cols = gray_image.shape
    m = cv2.getOptimalDFTSize(rows)
    n = cv2.getOptimalDFTSize(cols)

    # Create a padded image for optimal Fourier transform
    padded = cv2.copyMakeBorder(
        gray_image, 0, m - rows, 0, n - cols, cv2.BORDER_CONSTANT, value=0)

    # Perform the Discrete Fourier Transform (DFT)
    dft = cv2.dft(np.float32(padded), flags=cv2.DFT_COMPLEX_OUTPUT)

    # Shift the zero frequency component to the center
    dft_shift = np.fft.fftshift(dft)

    # Compute the magnitude and take the logarithm for better visualization
    magnitude_spectrum = cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
    magnitude_spectrum = np.log(
        magnitude_spectrum + 1)  # Add 1 to avoid log(0)

    return magnitude_spectrum


def contrast_enhancement(image):
    """Return the image with enhanced contrast using histogram equalization."""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply histogram equalization
    equalized_image = cv2.equalizeHist(gray_image)
    # Original grayscale image
    return equalized_image


def background_removal(image):
    """Return the image without its background."""
    result = remove(image)
    return result


def invert_image(image):
    """Return the inverted image."""
    inverted_image = cv2.bitwise_not(image)

    return inverted_image


# def ocr(file):
#     """Return a string with the text in the image."""
#     image_bytes = file.read()
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     reader = easyocr.Reader(['en'])
#     result = reader.readtext(image, paragraph="False")
#     return result[-1][-1]


def process_image(file, operation):
    """Return the result of the operation."""
    # Read image data as bytes
    image_bytes = file.read()

    # Convert image data to NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if (operation == "edge_detection"):
        result = edge_detection(image)
    elif (operation == "corner_detection"):
        result = corner_detection(image)
    elif (operation == "gaussian_blur"):
        result = gaussian_blur(image)
    elif (operation == "median_blur"):
        result = median_blur(image)
    elif (operation == "fourier_transform"):
        result = fourier_transform(image)
    elif (operation == "contrast_enhancement"):
        result = contrast_enhancement(image)
    elif (operation == "background_removal"):
        result = background_removal(image)
    elif (operation == "color_inversion"):
        result = invert_image(image)
    else:
        result = image
    # Encode the image as JPEG
    _, encoded_image = cv2.imencode('.png', result)
    return encoded_image.tobytes()
