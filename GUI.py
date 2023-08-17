import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from pyzbar.pyzbar import decode
import webbrowser
import qrcode

class QRReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Reader and Generator")  # Updated title

        self.root.geometry("600x400")

        self.qr_code_data = ""

        self.create_widgets()

    def create_widgets(self):
        try:
            self.qr_label = tk.Label(self.root, text="QR App:")
            self.qr_label.pack(pady=10)

            self.qr_data_label = tk.Label(self.root, text="", wraplength=500)
            self.qr_data_label.pack(pady=5)

            self.browse_button = tk.Button(self.root, text="Browse Image", command=self.browse_image)
            self.browse_button.pack(pady=10)

            self.generate_button = tk.Button(self.root, text="Generate QR Code", command=self.generate_qr_code)
            self.generate_button.pack(pady=10)  # Added Generate QR Code button

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

    def generate_qr_code(self):
        try:
            self.qr_data_entry = tk.Entry(self.root)
            self.qr_data_entry.pack(pady=5)
            
            generate_button = tk.Button(self.root, text="Generate QR Code", command=self.generate_qr_code_impl)
            generate_button.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while setting up QR code generation: {e}")

    def generate_qr_code_impl(self):
        try:
            qr_data = self.qr_data_entry.get()
            if qr_data.strip():
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_data)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")

                qr_img.save("generated_qrcode.png")  # Save the QR code image
                messagebox.showinfo("QR Code Generated", "QR Code generated and saved as 'generated_qrcode.png'.")

                # Clean up entry and button after generating QR code
                self.qr_data_entry.destroy()
                self.generate_button.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating QR code: {e}")


    def open_link(self, event):
        try:
            if self.qr_code_data.startswith("http://") or self.qr_code_data.startswith("https://"):
                webbrowser.open_new(self.qr_code_data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the link: {e}")

