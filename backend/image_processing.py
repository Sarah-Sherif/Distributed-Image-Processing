import cv2
import numpy as np
import cv2
import matplotlib.pyplot as plt
from rembg import remove
from PIL import *
import pytesseract
import easyocr
import pandas as pd


def edge_detection(image):
    """Return the edge map of the image."""
    result = cv2.Canny(image=image, threshold1=threshold1, threshold2=threshold2, apertureSize=3, L2gradient=False)
    return result
    


def corner_detection(image):
    """Return the image with the corners/interest points highlighted."""
    return image


def gaussian_blur(image):
    """Return the blurred image."""
    result = cv2.GaussianBlur(image, (kernel,kernel), 0)
    return result


def median_blur(image):
    """Return the blurred image"""
    result = cv2.medianBlur(image,ksize=kernel)
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
    padded = cv2.copyMakeBorder(gray_image, 0, m - rows, 0, n - cols, cv2.BORDER_CONSTANT, value=0)

    # Perform the Discrete Fourier Transform (DFT)
    dft = cv2.dft(np.float32(padded), flags=cv2.DFT_COMPLEX_OUTPUT)
    
    # Shift the zero frequency component to the center
    dft_shift = np.fft.fftshift(dft)

    # Compute the magnitude and take the logarithm for better visualization
    magnitude_spectrum = cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
    magnitude_spectrum = np.log(magnitude_spectrum + 1)  # Add 1 to avoid log(0)
    
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
   


def image_compression(image):
    """Return the compressed image."""
    image = cv2.imread("images.jpg")
    # Save the image with JPEG compression, setting the quality (1-100, where 100 is the best quality and least compression)
    compression_params = [int(cv2.IMWRITE_JPEG_QUALITY), 30]  # 30% quality for high compression
    # Save to a new JPEG file
    cv2.imwrite("images.jpg", image, compression_params)
    return image


def text_detection(image):
    """Return a string with the text in the image."""
    gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    noise=median_blur(gray,5)
    thresh = cv2.threshold(noise, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image2,paragraph="False")
    df=pd.DataFrame(result)
    print(str(df[1]))
    return image


def process_image(image, operation):
    """return the result of the operation."""
    return image
