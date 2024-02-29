
import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import os


def convert_pdf_to_images(pdf_path):
    images = []
    pdf_document = fitz.open(pdf_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]

        # using page.to_pixmap() to obtain a pixel rep on the current page
        pixmap = page.get_pixmap()
        img_pil = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)

        # Convert PIL image to BGR
        img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        images.append(img_bgr)

    pdf_document.close()
    return images


def highlight_extra_shapes(image1, image2):
    # Convert images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # compute absolute difference between the two grayscale images
    diff = cv2.absdiff(gray_image1, gray_image2)

    # threshold the difference to get binary image
    _, thresholded_diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    contours1, _ = cv2.findContours(thresholded_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # convert the binary difference image to color
    color_diff_image = cv2.cvtColor(thresholded_diff, cv2.COLOR_GRAY2BGR)

    # contours of differences only in image2
    contours2, _ = cv2.findContours(gray_image2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    for i, contour2 in enumerate(contours2):
        found_in_image1 = False
        for contour1 in contours1:
            if cv2.matchShapes(contour1, contour2, cv2.CONTOURS_MATCH_I2, 0.0) < 0.1:
                found_in_image1 = True
                break

        color = (0, 0, 255)

        if found_in_image1:
            color = (0, 0, 255)  # Use red color for lines on contours present in both images

        cv2.drawContours(color_diff_image, [contour2], 0, color, 2)

    return color_diff_image


def blend_images(original, highlighted, alpha=0.1):
    return cv2.addWeighted(original, 1 - alpha, highlighted, alpha, 0)


def save_highlighted_image(image, page_number, output_folder):
    output_path = os.path.join(output_folder, f'highlighted_page_{page_number}.png')

    # ensuring the image is in BGR format before saving
    if len(image.shape) == 2:
        # convert grayscale image to BGR
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    cv2.imwrite(output_path, image)
    print(f'Saved: {output_path}')


pdf1_path = '/Users/manvithanandyala/Desktop/comp_vision/intern_assignment/file_1.pdf'
pdf2_path = '/Users/manvithanandyala/Desktop/comp_vision/intern_assignment/file_2.pdf'

# output folder
output_folder = '/Users/manvithanandyala/Desktop/comp_vision/intern_assignment/output_highlighted_images'
os.makedirs(output_folder, exist_ok=True)

# convert PDFs to images
images1 = convert_pdf_to_images(pdf1_path)
images2 = convert_pdf_to_images(pdf2_path)

# save modified images
for i, (img1, img2) in enumerate(zip(images1, images2)):
    highlighted_img = highlight_extra_shapes(img1, img2)
    blended_img = blend_images(img1, highlighted_img)
    save_highlighted_image(blended_img, i + 1, output_folder)


























