from PIL import Image, ImageChops, ImageStat # imagechops -> "image channel operations"
import sys, os

from config import S3_KEY, S3_SECRET, S3_BUCKET, TMP_BOOL_FOLDER, save_bool_img_to_tmp

### Class establishments ###

class DiffInputImage:

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

### Functions ###

def check_inputs_and_open():
    """Manage incoming images"""

    try:
        img_1_path, img_2_path = [sys.argv[1], sys.argv[2]]
        
    except:

        print("Please provide image inputs.\n")
        img_1_path = input("Image 1: ").rstrip() # 'test-fixtures/imgs/inputs/img1.jpg'
        img_2_path = input("Image 2: ").rstrip() # 'test-fixtures/imgs/inputs/img2.jpg'

    # Establish image classes and open files for differencing
    img_1, img_2 = DiffInputImage(img_1_path), DiffInputImage(img_2_path)
    diff_input_1, diff_input_2 = Image.open(img_1.filepath), Image.open(img_2.filepath)

    return [img_1, img_2, diff_input_1, diff_input_2]



def create_cheap_diff(img_1, img_2, diff_input_1, diff_input_2):
    """Create a direct pixel value subtraction diff and save it"""

    diff_img = ImageChops.difference(diff_input_1, diff_input_2)
    diff_img.save('test-fixtures/imgs/diffs/diff_{}_{}.jpg'.format(img_1.filename, img_2.filename))

    return diff_img


def create_boolean_diff(diff_input_1_path, diff_input_2_path):
    """Convert input images to single channel images, output new bool diff"""

    # Convert input images to single channel, 8-bit, black and white images
    im1, im2 = Image.open(diff_input_1_path), Image.open(diff_input_2_path)
    im1l, im2l = im1.convert("L"), im2.convert("L") 
    im1.close(), im2.close() 

    # Compute diff at each pixel, find median value of diff 
    bw_diff = ImageChops.difference(im1l, im2l)
    bw_stat = ImageStat.Stat(bw_diff)
    bw_median = bw_stat.median

    # Est new image to populate later, est empty list for boolean vals
    bool_img = Image.new("L", bw_diff.size)
    bool_vals = []

    # Change all values to either 0 or 255, split based on median val of diff
    for pixel in bw_diff.getdata():

        if pixel > bw_median[0]:
            bool_vals.append(255)
    
        else:
            bool_vals.append(0)

    # Populate bool_img object with new vals and save 
    bool_img.putdata(bool_vals) 
    bool_img_path = save_bool_img_to_tmp(diff_input_1_path, diff_input_2_path, bool_img) #config util
    
    return bool_img_path

if __name__ == "__main__":

    img_1, img_2, diff_in_1, diff_in_2 = check_inputs_and_open()
    diff_img = create_cheap_diff(img_1, img_2, diff_in_1, diff_in_2)
    bool_img = create_boolean_diff(diff_in_1, diff_in_2)

    diff_img.show(), bool_img.show()
    diff_img.close(), bool_img.close()
