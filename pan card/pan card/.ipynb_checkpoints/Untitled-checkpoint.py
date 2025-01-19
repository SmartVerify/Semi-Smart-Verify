#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import pytesseract
from PIL import Image
import pandas as pd
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\SAIMANOJ\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def display_and_crop_region(image_path, coordinates):
    # Load the image
    img = mpimg.imread(image_path)

    # Check if the image is in portrait orientation, and rotate it to landscape
    if img.shape[0] > img.shape[1]:
        img = np.rot90(img)

    # Display the original image
    plt.imshow(img)
    plt.title("Original Image")
    plt.show()

    # Extract coordinates
    x, y, w, h = coordinates

    # Crop the region from the original image using specified coordinates
    cropped_region = img[y:y + h, x:x + w]

    # Display the cropped region
    plt.imshow(cropped_region)
    plt.title("Cropped Region")
    plt.show()

    return cropped_region

def extract_info(image_path):
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(Image.open(image_path))
    print(f"OCR Output for {image_path}:\n{text}\n")

    # Define patterns based on the observed OCR output
    name_pattern = r'(?<=Ta / Name\s)([A-Z\s]+)'
    dob_pattern = r'(?i)(\d{2}/\d{2}/\d{4})'
    pan_pattern = r'([A-Z]{5}[0-9]{4}[A-Z]{1})'
    father_name_pattern = r'(?<=frat I 41a / Father\'s Name igs iia\s)([A-Z\s]+)'

    # Extract information using patterns
    name_match = re.search(name_pattern, text)
    dob_match = re.search(dob_pattern, text)
    pan_match = re.search(pan_pattern, text)
    father_name_match = re.search(father_name_pattern, text)

    # Extracted values or 'Not found' if not found
    name = name_match.group(1).strip() if name_match else 'Not found'
    dob = dob_match.group(1) if dob_match else 'Not found'
    pan = pan_match.group(1) if pan_match else 'Not found'

    # Remove common text from father's name
    father_name = father_name_match.group(1).strip() if father_name_match else 'Not found'
    if name.lower() in father_name.lower():
        father_name = father_name.replace(name, '').strip()

    # Check for the presence of the word "Signature" in the extracted text
    signature_presence = 'present' if 'Signature' in text else 'absent'

    return [name, father_name, dob, pan, signature_presence]

def process_and_save_data(image_path, coordinates, csv_file_path):
    # Display and crop the specified region
    cropped_region = display_and_crop_region(image_path, coordinates)

    # Extract information from the single image
    extracted_data = [extract_info(image_path)]

    # Convert the list of data to a pandas DataFrame
    df = pd.DataFrame(extracted_data, columns=['Name', 'Father\'s Name', 'DOB', 'PAN', 'Signature Presence'])

    # Save the cropped image to the CSV file
    img_path = os.path.splitext(csv_file_path)[0] + "_cropped.jpg"
    cv2.imwrite(img_path, cv2.cvtColor(cropped_region, cv2.COLOR_RGB2BGR))
    df['Cropped Image'] = [img_path]

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    print(f"Data extracted and saved to {csv_file_path}")
    print(f"Cropped image saved to {img_path}")

def main():
    # Replace 'path/to/your/image.jpg' with the actual path to your image
    image_path = r"C:\Users\SAIMANOJ\Desktop\pan card\data\2.jpg"

    # Specify the coordinates (x, y, width, height) for the region to be cropped
    box_coordinates = (400, 650, 600, 700)  # Adjust these coordinates based on your image

    # Provide the path to save the CSV file
    csv_file_path = r"C:\Users\SAIMANOJ\Desktop\pan card\im\final.csv"

    # Process and save data
    process_and_save_data(image_path, box_coordinates, csv_file_path)

if __name__ == "__main__":
    main()


# In[ ]:




