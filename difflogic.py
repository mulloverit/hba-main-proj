from PIL import Image, ImageChops # imagechops -> "image channel operations"
import sys, os

# useful Image attributes: .format, .size, .mode, .bits, .pallette
# useful Image methods: .getbbox(), .histogram(), .putalpha(), .resize(), .rotate(), .crop(), .save(), .copy(), .open()

############# SPAGHETTI CODE FOR INITAL IMAGE DIFF #######################

try:
    
    img_1_path = sys.argv[1]
    img_2_path = sys.argv[2]

except:

    print("Please provide image inputs.\n")
    img_1_path = input("Image 1: ") # 'test-fixtures/imgs/inputs/img_1.jpg'
    img_2_path = input("Image 2: ") # 'test-fixtures/imgs/inputs/img_2.jpg'

# img_1_basename = os.path.basename(img_1_path)
# img_2_basename = os.path.basename(img_2_path)

# img_1_suffix = os.path.splitext(img_1_basename)[0]
# img_2_suffix = os.path.splitext(img_2_basename)[0]

# img_1 = Image.open(img_1_path)
# img_2 = Image.open(img_2_path)

# diff = ImageChops.difference(img1, img2)

# img1.close()
# img2.close()

# diff.show()
# diff.save('test-fixtures/imgs/diffs/diff_{}_{}.jpg'.format())
# diff.close()



#######################################################

# Image attributes: filepath 
# Image methods: getinfo(size, method, format)

class InputImage:

    def __init__(self, filepath):
        """Instantiate an Image class object"""
        self.filepath = filepath

    # method to retrieve basic information about an image
    def get_info(self):
        im = Image.open(self.filepath) # open file

        # retrieve data via PIL Image attributes
        im_size = im.size
        im_mode = im.mode
        im_format = im.format

        im.close() # responsibly close file

        print(f"""\t\tFilepath: {self.filepath},
                  Size: {im_size},
                  Mode: {im_mode},
                  Format: {im_format}""")


##########################################################


#### FOR DOCTESTS LATER #####

# img_1_path = '/Users/mulloverit/mulloverit-gh/hba-main-proj/test-fixtures/imgs/inputs/img_1.jpg'
# im1 = InputImage(img_1_path)
# im1.get_info()
# >>>        Filepath: /Users/mulloverit/mulloverit-gh/hba-main-proj/test-fixtures/imgs/inputs/img_1.jpg,
#                   Size: (2283, 2283),
#                   Mode: RGB,
#                   Format: JPEG