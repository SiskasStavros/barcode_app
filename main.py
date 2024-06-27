from __future__ import print_function
import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk, ImageFont, ImageDraw
import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException
from pprint import pprint
import ast
import os

API_KEY = os.environ["API_KEY"]


def upload_file():
    f_types = [('png Files', '*.png'), ('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    phimg = ImageTk.PhotoImage(img)
    window.one = phimg
    canvas.create_image((20, 20), anchor='nw', image=phimg)
    configuration = cloudmersive_barcode_api_client.Configuration()
    configuration.api_key['Apikey'] = API_KEY
    api_instance = cloudmersive_barcode_api_client.BarcodeScanApi(cloudmersive_barcode_api_client.ApiClient(configuration))
    image_file = filename
    try:
        api_response = api_instance.barcode_scan_image(image_file)
        pprint(api_response)
    except ApiException as e:
        print(f"Exception when calling BarcodeScanApi->barcode_scan_image:{e}")
    

def generate_qrcode():
    configuration = cloudmersive_barcode_api_client.Configuration()
    configuration.api_key['Apikey'] = API_KEY
    api_instance = cloudmersive_barcode_api_client.GenerateBarcodeApi(cloudmersive_barcode_api_client.ApiClient(configuration))
    user_input = text_box.get("1.0", "end-1c")
    if user_input != "":
        try:
            api_response = api_instance.generate_barcode_qr_code(user_input)
        except ApiException as e:
            print(f"Exception when calling BarcodeScanApi->barcode_scan_image:{e}")
        data = ast.literal_eval(api_response)
        with open("new_qr_code.png", 'wb') as binary_file:
            binary_file.write(data)
        img = Image.open("new_qr_code.png")
        phimg = ImageTk.PhotoImage(img)
        window.one = phimg
        canvas.create_image((20, 20), anchor='nw', image=phimg)


window = tk.Tk()
window.geometry("1000x750")  # Size of the window
window.title('Barcode Generator')
my_font1 = ('arial', 18, 'bold')
l1 = tk.Label(window, text='Add an Image', width=30, font=my_font1)
l1.grid(row=1, column=1, columnspan=3)
b1 = tk.Button(window, text='Upload Barcode', width=20, command=lambda:upload_file())
text_box = tk.Text(window,bg="white", height=2, width=25)
b2 = tk.Button(window, text="Create Barcode", width=20, command=generate_qrcode)
canvas = tk.Canvas(window, width=500, height=500, background="white")
b1.grid(row=2, column=1, padx=20)
text_box.grid(row=2, column=2)
b2.grid(row=2, column=3)
canvas.grid(row=3, column=1, columnspan=4, padx=20, pady=20)


window.mainloop()  # Keep the window open
