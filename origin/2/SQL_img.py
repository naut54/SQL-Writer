import pymysql
import tkinter as tk
from tkinter import filedialog

def upload_image():
    # Database connection details
    db_config = {
        'host': 'PMYSQL178.dns-servicio.com',
        'user': 'admin',
        'password': 'edu7709M%',
        'database': '10467318_users',
    }

    # Create a simple GUI to select the image file
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])

    if file_path:
        # Read the image file
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        # Connect to the database
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Insert the image into the database
                sql = "INSERT INTO images (name, image_data) VALUES (%s, %s)"
                values = (file_path.split("/")[-1], binary_data)
                cursor.execute(sql, values)
            connection.commit()
            print("Image uploaded successfully")
        except pymysql.Error as error:
            print(f"Failed to upload image: {error}")
        finally:
            if connection:
                connection.close()
    else:
        print("No file selected")

# Run the upload function
upload_image()