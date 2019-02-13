from PIL import Image, ImageChops, ImageStat # imagechops -> "image channel operations"
import sys, os

from testseed import load_users, load_input_imgs, load_diff_imgs

#################### Class definitions: 

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


#################### Make cheap pixel image difference: 

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
diff_img = ImageChops.difference(diff_input_1, diff_input_2)
diff_img.save('test-fixtures/imgs/diffs/diff_{}_{}.jpg'.format(img_1.filename, img_2.filename))

#################### Make boolean difference:

# Convert input images to single channel, 8-bit, black and white images
im1l, im2l = diff_input_1.convert("L"), diff_input_2.convert("L")
bw_diff = ImageChops.difference(im1l, im2l) # compute their diff at every pixel
bw_stat = ImageStat.Stat(bw_diff) # create an image statistics object
bw_median = bw_stat.median # grab the diff's median value

# Create a new image that will be populated by boolean image
# Open a list for storing boolean values
bool_img = Image.new("L", bw_diff.size)
bool_vals = []

# Change all values to either 0 or 255, split based on median val of diff
for pixel in bw_diff.getdata():
    if pixel > bw_median[0]:
        bool_vals.append(255) # 255 instead of 1 cuz 8 bits
    else:
        bool_vals.append(0)

# Add new vals to new image and save boolean image next to initial diff
bool_img.putdata(bool_vals)
bool_img.save('test-fixtures/imgs/diffs/diff_{}_{}_bool.jpg'.format(img_1.filename, img_2.filename))

# For debugging:
diff_img.show(), bool_img.show()

# Close up shop
diff_input_1.close(), diff_input_2.close(), diff_img.close(), bool_img.close()
