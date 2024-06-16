from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image

def png_to_ico(icon_sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]):
    """
    Convert a selected PNG file to an ICO file through a file dialog.

    :param icon_sizes: List of tuple sizes for the icon.
    """
    # Hide the main tkinter window
    root = Tk()
    root.withdraw()

    # Open file dialog to choose the PNG file
    png_file = askopenfilename(title="Select PNG file", filetypes=[("PNG files", "*.png")])
    if not png_file:
        print("No file selected.")
        return

    # Open save file dialog to choose where to save the ICO file
    ico_file = asksaveasfilename(title="Save ICO file as", filetypes=[("ICO files", "*.ico")], defaultextension=".ico")
    if not ico_file:
        print("No save file chosen.")
        return

    # Open the PNG file
    image = Image.open(png_file)
    
    # Convert the image to ICO and save it
    image.save(ico_file, format='ICO', sizes=icon_sizes)
    print(f"Successfully converted {png_file} to {ico_file}")

# Call the function
png_to_ico()
