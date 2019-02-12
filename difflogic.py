from PIL import Image, ImageChops # imagechops -> "image channel operations"
import sys, os

# useful Image attributes: .format, .size, .mode, .bits, .pallette
# useful Image methods: .getbbox(), .histogram(), .putalpha(), .resize(), .rotate(), .crop(), .save(), .copy(), .open()

############# SPAGHETTI CODE FOR INITAL IMAGE DIFF #######################

try:

    img_1_path = sys.argv[0]
    img_2_path = sys.argv[1]

except:

    print("Please provide image inputs.\n")
    img_1_path = input("Image 1: ") # 'test-fixtures/imgs/inputs/img_1.jpg'
    img_2_path = input("Image 2: ") # 'test-fixtures/imgs/inputs/img_2.jpg'

img_1_basename = os.path.basename(img_1_path)
img_2_basename = os.path.basename(img_2_path)

img_1_suffix = os.path.splitext(img_1_basename)[0]
img_2_suffix = os.path.splitext(img_2_basename)[0]

img_1 = Image.open(img_1_path)
img_2 = Image.open(img_2_path)

diff = ImageChops.difference(img1, img2)

img1.close()
img2.close()

diff.show()
diff.save('test-fixtures/imgs/diffs/diff_{}_{}.jpg'.format())
diff.close()



#######################################################

# Image attributes: filepath 
# Image methods: getinfo(size, method, format)

# class Image:

#     def __init__(self, filepath):
#         self.filepath = filepath
#         self.info()

#     def get_info(self):
        
#         im_size = filepath.size
#         im_mode = filepath.mode
#         im_format = filepath.format

#         print(f"Filepath: {self.filepath}")


##########################################################


