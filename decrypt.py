import hashlib
import numpy as np
import os
import cv2 as cv

hash_values = []

with open('hashes.txt', 'r') as f:
    for line in f:
        hash_values.append(line.strip())

encrypted_files_dir = 'encrypted_files'
results_dir = 'decrypt_results'
encrypted_files = os.listdir('encrypted_files')

if len(os.listdir(results_dir)) > 0:
    for file in os.listdir(results_dir):
        os.remove(os.path.join(results_dir, file))

for file in encrypted_files:
    with open(f'{encrypted_files_dir}/{file}', 'rb') as f:
        data = f.read()

        for i in range(300, 800):
            for j in range(300, 800):
                header = f'P6 {i} {j} {255}'.encode('utf-8')
                hash = hashlib.sha256(header).hexdigest()

                if hash in hash_values:
                    img = header + b'\n' + data
                    decrypted_file_name = f"{file}_{hash}_decrypted.ppm"

                    with open(os.path.join(results_dir, decrypted_file_name), 'wb') as destination_file:
                        destination_file.write(img)

for i in range(1, 9):
    image_files = [file for file in os.listdir(results_dir) if file.startswith(f'File{i}')]

    for image_file in image_files:
        img = cv.imread(os.path.join(results_dir, image_file), cv.IMREAD_GRAYSCALE)
        
        if img is not None:
            # img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)[1]
            # img = cv.medianBlur(img, 3)

            # kernel = np.ones((2,2),np.uint8)
            # img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
            # img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

            # img = cv.medianBlur(img, 3)

            # img = cv.Laplacian(img, cv.CV_8U, ksize=1)

            # kernel = np.ones((3,3),np.uint8)
            # img = cv.dilate(img, kernel, iterations=1)

            # img = cv.Laplacian(img, cv.CV_8U, ksize=3)

            # kernel = np.ones((5,5),np.uint8)
            # img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

            # img = cv.medianBlur(img, 3)

            cv.imshow(image_file, img)
            cv.waitKey(0)
            cv.destroyAllWindows()
        else:
            print(f"Error reading file {image_file}")