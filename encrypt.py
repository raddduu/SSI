from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import numpy as np
import cv2 as cv
import os

def generate_cipher(cipher_key):
    return Cipher(algorithms.AES(cipher_key), modes.ECB())

def pad_input(input_data):
    data_padder = padding.PKCS7(algorithms.AES.block_size).padder()
    return data_padder.update(input_data.encode('latin-1')) + data_padder.finalize()

def encrypt_input(input_data, cipher_key):
    cipher_instance = generate_cipher(cipher_key)
    padded_input = pad_input(input_data)
    return cipher_instance.encryptor().update(padded_input) + cipher_instance.encryptor().finalize()

def read_input_file(input_file_path):
    with open(input_file_path, 'rb') as input_file:
        return input_file.read()

def write_output_file(output_file_path, output_content):
    with open(output_file_path, 'wb') as output_file:
        output_file.write(output_content)

def transform_image(input_file_path, cipher_key):
    file_data = read_input_file(input_file_path)
    encrypted_output = file_data[:file_data.find(b'255\n') + 4] + encrypt_input(file_data[file_data.find(b'255\n') + 4:].decode('latin-1'), cipher_key)
    write_output_file(os.path.splitext(input_file_path)[0] + '_encr.ppm', encrypted_output)

    encrypted_image_data = np.frombuffer(encrypted_output, dtype=np.uint8)
    image_height = int(np.sqrt(len(encrypted_image_data)))
    image_width = len(encrypted_image_data) // image_height
    encrypted_image_data = encrypted_image_data[:image_height*image_width].reshape((image_height, image_width))

    cv.imshow('Encrypted Image', cv.resize(encrypted_image_data, (0, 0), fx=2, fy=2))
    cv.waitKey(0)
    cv.destroyAllWindows()

def delete_encrypted_files(target_directory):
    for file in [file for file in os.listdir(target_directory) if file.endswith('_encr.ppm')]:
        os.remove(f'{target_directory}/{file}')

def process_directory_files(target_directory, cipher_key):
    for file in os.listdir(target_directory):
        transform_image(f'{target_directory}/{file}', cipher_key)

delete_encrypted_files('to_be_encrypted_files')
process_directory_files('to_be_encrypted_files', b'ABCDEFGHIJKLMNOP')