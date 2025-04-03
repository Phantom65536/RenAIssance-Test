from hezar.models import Model
from hezar.utils import *
# from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import os
import cv2
import numpy as np
# from pytesseract import Output
# import pytesseract
# import matplotlib.pyplot as plt


data_name = "PORCONES.228.35 – 1636"
file_name = "page_1"
model = Model.load("hezarai/CRAFT", device="cpu")
image = load_image(f"./extracted_imgs/{data_name}/{file_name}.png")

image_np = np.array(image)

# Parameters for the bounding boxes
start_x = 0  # p1, p3: 15
start_y = 0  # p1: 55, p3: 61 # 14
fixed_width = 475  # p1: 520, p3: 545
heights = [23] * 3 + [22] * 4 + [24] * 3 + [22]  # [18] * 2 + [17] * 1 + [16] * 16  # + [17] * 6 + [16] * 4

# Draw bounding boxes
current_y = start_y
save_dir = 'cropped_imgs'
img_copy = image_np.copy()
for i in range(len(heights)):
    # Draw the rectangle (bounding box)
    top_left = (start_x, current_y)
    bottom_right = (start_x + fixed_width, current_y + heights[i])
    cv2.rectangle(img_copy, top_left, bottom_right, (0, 255, 0), 2)
    cropped_image = image_np[current_y:current_y + heights[i], start_x:start_x + fixed_width]
    current_y += heights[i]
    file_path = os.path.join(f"./{save_dir}/{data_name}/{file_name}/", f'cropped_{i}.png')
    print(file_path)
    cv2.imwrite(file_path, cropped_image)

# gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
# rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
# results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
#
# for i in range(0, len(results["text"])):
#     # extract the bounding box coordinates of the text region from
#     # the current result
#     if int(results["conf"][i]) > 0.7:
#         x = results["left"][i]
#         y = results["top"][i]
#         w = results["width"][i]
#         h = results["height"][i]
#         cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

# # Step 1: Binarize and invert
# _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# binary = 255 - binary
#
# # Step 2: Horizontal dilation
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 1))  # wide and short
# dilated = cv2.dilate(binary, kernel, iterations=1)
#
# # Step 3: Find contours
# contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# line_boxes = [cv2.boundingRect(c) for c in contours]
#
# # Optional: Sort lines top to bottom
# line_boxes = sorted(line_boxes, key=lambda x: x[1])
#
# # Draw results
# output = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
# for x, y, w, h in line_boxes:
#     cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

# output = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
pil_image = Image.fromarray(img_copy)
show_image(pil_image, "thick_text")

# _, bin_img = cv2.threshold(gray, 120, 255, cv2.THRESH_OTSU)
#
# # Compute the distance transform (larger values in thicker regions)
# dist = cv2.distanceTransform(bin_img, cv2.DIST_L2, 3)
#
# # Label connected components
# num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(bin_img, connectivity=8)
#
# # Output image for thick text only
# thick_text = np.zeros_like(bin_img)
#
# # Set a threshold for the maximum distance within a component (tune as needed)
# thickness_threshold = 1.6  # adjust based on your image resolution
#
# for i in range(1, num_labels):
#     component_mask = (labels == i)
#     max_dist = dist[component_mask].max()
#     if max_dist >= thickness_threshold:
#         thick_text[component_mask] = 255
#
# processed_for_craft = cv2.cvtColor(thick_text, cv2.COLOR_GRAY2BGR)
# pil_image = Image.fromarray(processed_for_craft)
# show_image(pil_image, "thick_text")



# _, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# dist = cv2.distanceTransform(bin_img, cv2.DIST_L2, 3)
#
# num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(bin_img)
# for i in range(1, num_labels):
#     mask = (labels == i)
#     # Max distance of this component
#     max_dist = dist[mask].max()
#     if max_dist < some_threshold:
#         bin_img[mask] = 0  # remove thin component

# # 3. Enhance contrast (CLAHE example)
# clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
# enhanced = clahe.apply(gray)
#
# # 4. Adaptive threshold
# # thresh = cv2.adaptiveThreshold(
# #     enhanced,
# #     maxValue=255,
# #     adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
# #     thresholdType=cv2.THRESH_BINARY,
# #     blockSize=15,
# #     C=25
# # )
# _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
#
# processed_for_craft = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
# pil_image = Image.fromarray(processed_for_craft)
#
# ori_image = pil_image.copy()
# outputs = model.predict(pil_image)
# result_image = draw_boxes(pil_image, outputs[0]["boxes"])
# show_image(result_image, "text_detected")
#
# save_dir = 'cropped_imgs'
# os.makedirs(f"./{save_dir}/{data_name}", exist_ok=True)
# print(processed_for_craft.size)
#
# for i, box in enumerate(outputs[0]["boxes"]):
#     if box is None:
#         continue
#
#     # Ensure coordinates are integers (in case they're float)
#     x_min, y_min, x_h, y_h = map(int, box)
#
#     # Crop the image using numpy slicing
#     cropped_image = ori_image.crop((x_min, y_min, x_min + x_h, y_min + y_h))
#
#     # Define the file path for the cropped image
#     file_path = os.path.join(f"./{save_dir}/{data_name}", f'cropped_{i}.png')
#
#     # Save the cropped image; if the file exists, it will be overwritten
#     save_image(cropped_image, file_path)
#
# processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
# model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
#
# # load image from the IAM dataset
# url = "./extracted_imgs/Constituciones sinodales Calahorra 1602/page_1 copyy.png"
# image = Image.open(url).convert("RGB")
#
# pixel_values = processor(image, return_tensors="pt").pixel_values
# generated_ids = model.generate(pixel_values)
#
# generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)
# print(generated_text)
