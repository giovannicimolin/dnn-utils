import glob
import os
import pprint
import csv
from PIL import Image
from random import randint


# Printing results
pp = pprint.PrettyPrinter(indent=4)


def process():
    # Finds all csv files on data/ and append to list
    pascal_voc_contents = []
    os.chdir("data")

    print("Found {} files in data directory!".format(
        str(len(glob.glob("*.csv")))))
    for file in glob.glob("*.csv"):
        f_handle = open(file, 'r')
        reader = csv.reader(f_handle)
        headers = next(reader)
        print("Parsing file '{}'...".format(file))
        pascal_voc_contents.append(list(reader))

    pascal_voc_contents = pascal_voc_contents[0]

    # Process each file individually
    for index in pascal_voc_contents:
        image_file = index[0]
        # If there's a corresponding file in the folder,
        # process the images and save to output folder
        if os.path.isfile(image_file):
            extractDataset(index)
        else:
            print("Image file '{}' not found, skipping file...".format(image_file))


# Extract image samples and save to output dir
def extractDataset(dataset):
    # Open image and get ready to process
    img = Image.open(dataset[0])

    # Create output directory
    save_dir = "output"
    try:
        os.mkdir(save_dir)
    except:
        pass
    # Image name preamble
    sample_preamble = "output/" + dataset[0].split('.')[0]

    print(dataset)
    bndbox = [int(dataset[4]), int(dataset[5]), int(dataset[6]), int(dataset[7])]
    # Crop image
    im = img.crop((bndbox[0], bndbox[1],
                   bndbox[2], bndbox[3]))
    # Save
    im.save(sample_preamble + str(randint(0,100000)) + '.jpg')

if __name__ == '__main__':
    print("\n------------------------------------")
    print("----- PascalVOC-to-Images v0.1 -----")
    print("Created by Giovanni Cimolin da Silva")
    print("------------------------------------\n")
    process()
