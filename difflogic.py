from PIL import Image, ImageChops # imagechops -> "image channel operations"
import sys, os

from testseed import load_users, load_input_imgs, load_diff_imgs

# useful Image attributes: .format, .size, .mode, .bits, .pallette
# useful Image methods: .getbbox(), .histogram(), .putalpha(), .resize(), .rotate(), .crop(), .save(), .copy(), .open()

############# SPAGHETTI CODE FOR INITAL IMAGE DIFF #######################

try:
    #input_images = [sys.argv[1], sys.argv[2]]
    
    img_1_path = sys.argv[1]
    img_2_path = sys.argv[2]

except:

    print("Please provide image inputs.\n")
    img_1_path = input("Image 1: ") # 'test-fixtures/imgs/inputs/img1.jpg'
    img_2_path = input("Image 2: ") # 'test-fixtures/imgs/inputs/img2.jpg'

# img_1_basename = os.path.basename(img_1_path)
# img_2_basename = os.path.basename(img_2_path)

# img_1_name = os.path.splitext(img_1_basename)[0]
# img_2_name = os.path.splitext(img_2_basename)[0]

# img_1 = Image.open(img_1_path)
# img_2 = Image.open(img_2_path)

# diff = ImageChops.difference(img_1, img_2)

# img_1.close()
# img_2.close()

# diff.show()
# diff.save('test-fixtures/imgs/diffs/diff_{}_{}.jpg'.format(img_1_name, img_2_name))
# diff.close()

#######################################################

# Image attributes: filepath 
# Image methods: getinfo(size, method, format)


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


img_1 = InputImage(img_1_path)
img_2 = InputImage(img_2_path)
diff_input_1 = Image.open(img_1.filepath)
diff_input_2 = Image.open(img_2.filepath)

diff = ImageChops.difference(diff_input_1, diff_input_2)

diff.save('test-fixtures/imgs/diffs/diff_{}_{}.jpg'.format(img_1.filename, img_2.filename))

diff.close()



##########################################################


#### FOR DOCTESTS LATER #####

# img_1_path = '/Users/mulloverit/mulloverit-gh/hba-main-proj/test-fixtures/imgs/inputs/img_1.jpg'
# im1 = InputImage(img_1_path)
# im1.get_info()
# >>>        Filepath: /Users/mulloverit/mulloverit-gh/hba-main-proj/test-fixtures/imgs/inputs/img_1.jpg,
#                   Size: (2283, 2283),
#                   Mode: RGB,
#                   Format: JPEG