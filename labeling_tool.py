import csv
import os
from PIL import Image
import psutil

# Path to the directory containing images
image_directory = './resized_images'
# Path to the CSV file
csv_file_path = f'./{image_directory}/metadata.csv'

# Function to display an image
def display_image(image_path):
    with Image.open(image_path) as img:
        img.show()

# Read the CSV file
with open(csv_file_path, mode='r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    # Convert to list for reusability
    rows = list(csv_reader)

# Loop through each row and display the image and current text
# Function to close the image preview
def close_image(image):
    for proc in psutil.process_iter():
        if proc.name() == "display":
            proc.kill()

# Loop through each row and display the image and current text
for row in rows:
    image_path = os.path.join(image_directory, row['file_name'])
    if os.path.exists(image_path):
        text_parts = row['text'].split(', ')
        
        # Check if there are at least three parts to edit the text after the second comma
        if len(text_parts) > 2:
            print(f"Current text for {row['file_name']}: {row['text']}")
            img = Image.open(image_path)
            img.show()
            
            # Ask the user for new text to replace the part after the second comma
#             print("Enter new text to replace the part after the second comma:")
            new_text_part = input(f"Current part: {text_parts[1]}\nNew text (or press Enter to keep the current text): ")
            
#             # If the user entered new text, update the part after the second comma
#             if new_text_part:
#                 text_parts[1] = new_text_part
#                 row['text'] = ', '.join(text_parts)
#                 print(f"Updated text: {row['text']}")
#             else:
#                 print("No changes made.")

#             # Close the image, if possible
#             close_image(img)
#         else:
#             print(f"Not enough parts in the text to update for {row['file_name']}")

# # Write the updated data back to the CSV file
# with open(csv_file_path, mode='w', newline='') as csvfile:
#     fieldnames = rows[0].keys()
#     csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     csv_writer.writeheader()
#     for row in rows:
#         csv_writer.writerow(row)

# print("CSV file has been updated.")
