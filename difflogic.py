from PIL import Image, ImageChops # imagechops -> "image channel operations"
import sys, os

from testseed import load_users, load_input_imgs, load_diff_imgs

# useful Image attributes:  .format, .size, .mode, .bits, .pallette
# useful Image methods:     .getbbox(), .histogram(), .putalpha(), .resize(), 
#                           .rotate(), .crop(), .save(), .copy(), .open()

class InputImage:

    def __init__(self, filepath):
        """Instantiate an Image class object"""

        self.filepath = filepath
        self.base = os.path.basename(filepath)
        self.filename = os.path.splitext(self.base)[0]

    def get_info(self):
        """Retrieve basic information about an image"""

        im = Image.open(self.filepath) # open file

        im_size = im.size # retrieve data via PIL Image attributes
        im_mode = im.mode
        im_format = im.format

        im.close() # responsibly close file

        print(f"""\t\tFilepath: {self.filepath},
                  Size: {im_size},
                  Mode: {im_mode},
                  Format: {im_format}""")


##########################################################

try:
    img_1_path, img_2_path = [sys.argv[1], sys.argv[2]]
    
except:

    print("Please provide image inputs.\n")
    img_1_path = input("Image 1: ") # 'test-fixtures/imgs/inputs/img1.jpg'
    img_2_path = input("Image 2: ") # 'test-fixtures/imgs/inputs/img2.jpg'

# Establish image classes and open files for differencing
img_1, img_2 = InputImage(img_1_path), InputImage(img_2_path)
diff_input_1, diff_input_2 = Image.open(img_1.filepath), Image.open(img_2.filepath)

# Perform image differencing, save the diff
diff = ImageChops.difference(diff_input_1, diff_input_2)
diff.save('test-fixtures/imgs/diffs/diff_{}_{}.jpg'.format(img_1.filename, img_2.filename))

# Close all image files
diff_input_1.close(), diff_input_2.close(), diff.close()

