import cv2

image_path = "C:/Users/MSI/Documents/QR decode/QR_reader_python/frame.png"
image = cv2.imread(image_path)

from pyzbar.pyzbar import decode

decoded_objects = decode(image)
for obj in decoded_objects:
    print("Data:", obj.data.decode('utf-8'))
