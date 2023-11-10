from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import numpy as np
import os
import cv2

def normalize_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Normalize colors
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)

    # Denoising
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

    # Convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Skew correction
    coords = np.column_stack(np.where(image > 0))
    angle = 90 - cv2.minAreaRect(coords)[-1]
    M = cv2.getRotationMatrix2D((image.shape[1] / 2, image.shape[0] / 2), angle, 1)
    image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    normalized_image_path = "preprocessed/normalized_" + os.path.basename(image_path)
    cv2.imwrite(normalized_image_path, image)

    return normalized_image_path

def doctr_ocr(path, name):
    model = ocr_predictor(pretrained=True)

    # Normalize the image
    normalized_image_path = normalize_image(path)

    doc = DocumentFile.from_images(normalized_image_path)
    result = model(doc)
    # result.show(doc)
    json_response = result.export()
    file_path = "outputs/" + name + ".txt"
    with open(file_path, "w") as file:
        pass
    for block in json_response["pages"][0]["blocks"]:
        for line in block["lines"]:
            val = ""
            for word in line["words"]:
                val += word["value"]
                val += " "
            val += "\n"
            with open(file_path, "a") as file:
                file.write(val)

folder_path = "images"
file_list = os.listdir(folder_path)

for path in file_list:
    doctr_ocr(folder_path + "/" + path, path)
