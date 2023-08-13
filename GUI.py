import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from pyzbar.pyzbar import decode
import webbrowser

class QRReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Reader")

        self.root.geometry("600x400")

        self.qr_code_data = ""

        self.create_widgets()

    def create_widgets(self):
        try:
            self.qr_label = tk.Label(self.root, text="QR Code Data:")
            self.qr_label.pack(pady=10)

            self.qr_data_label = tk.Label(self.root, text="", wraplength=500)
            self.qr_data_label.pack(pady=5)

            self.browse_button = tk.Button(self.root, text="Browse Image", command=self.browse_image)
            self.browse_button.pack(pady=10)

            self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
            self.quit_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during GUI creation: {e}")

    def browse_image(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
            if file_path:
                self.read_qr_codes(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while browsing image: {e}")

    def read_qr_codes(self, image_path):
        try:
            frame = cv2.imread(image_path)
            if frame is None:
                messagebox.showerror("Error", "Failed to open the selected image.")
                return

            decoded_objects = decode(frame)
            if decoded_objects:
                self.qr_code_data = decoded_objects[0].data.decode('utf-8')
                self.qr_data_label.config(text=self.qr_code_data, foreground="blue", cursor="hand2")
                self.qr_data_label.bind("<Button-1>", self.open_link)
            else:
                self.qr_code_data = ""
                self.qr_data_label.config(text="No QR code found in the image.", foreground="red")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading QR codes: {e}")

    def open_link(self, event):
        try:
            if self.qr_code_data.startswith("http://") or self.qr_code_data.startswith("https://"):
                webbrowser.open_new(self.qr_code_data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the link: {e}")

