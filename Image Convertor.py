import os
import sys
import pyheif
from PIL import Image

def heic_to_png(heic_file_path, png_file_path):
    try:
        heif_file = pyheif.read(heic_file_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        image.save(png_file_path, format="PNG")
        print(f"Conversion successful. PNG file saved at {png_file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    heic_file_path = input("Enter the path of the .heic file: ").strip()
    
    if not os.path.isfile(heic_file_path):
        print(f"Error: {heic_file_path} does not exist.")
        sys.exit(1)

    default_output_path = os.path.splitext(heic_file_path)[0] + ".png"
    png_file_path = input(f"Enter the path for the output .png file (default: {default_output_path}): ").strip()
    if not png_file_path:
        png_file_path = default_output_path

    heic_to_png(heic_file_path, png_file_path)
