import glob
import os
import xmltodict
import json
import pprint

from PIL import Image


# Printing results
pp = pprint.PrettyPrinter(indent=4)


# Look for XML files and parses then as if they were Pascal VOC Files
def process(directory="data", count=False):
    # Finds all XML files on data/ and append to list
    pascal_voc_contents = []
    owd = os.getcwd()
    os.chdir(directory)

    print("Found {} files...".format(
        str(len(glob.glob("*.xml")))))
    for file in glob.glob("*.xml"):
        f_handle = open(file, 'r')
        #print("Parsing file '{}'...".format(file))
        pascal_voc_contents.append(xmltodict.parse(f_handle.read()))

    # Process each file individually
    object_count = 0
    for index in pascal_voc_contents:
        image_file = index['annotation']['filename']
        # If there's a corresponding file in the folder,
        # process the images and save to output folder
        if os.path.isfile(image_file):
            if count==False:
                extractDataset(index['annotation'])
            else:
                object_count = object_count + countDataset(index['annotation'])
        else:
            print("Image file '{}' not found, skipping file...".format(image_file))

    if count==True:
        print("Found {} objects...".format(object_count))

    # Go back to original path
    os.chdir(owd)


# Extract image samples and save to output dir
def countDataset(dataset):
    try:
        size = len(dataset['object'])
    except:
        size = 0
    return size


# Extract image samples and save to output dir
def extractDataset(dataset):
    print("Found {} objects on image '{}'...".format(
        len(dataset['object']), dataset['filename']))

    # Open image and get ready to process
    img = Image.open(dataset['filename'])

    # Create output directory
    save_dir = dataset['filename'].split('.')[0]
    try:
        os.mkdir(save_dir)
    except:
        pass
    # Image name preamble
    sample_preamble = save_dir + "/" + dataset['filename'].split('.')[0] + "_"
    # Image counter
    i = 0

    # Run through each item and save cut image to output folder
    for item in dataset['object']:
        # Convert str to integers
        bndbox = dict([(a, int(b)) for (a, b) in item['bndbox'].items()])
        # Crop image
        im = img.crop((bndbox['xmin'], bndbox['ymin'],
                       bndbox['xmax'], bndbox['ymax']))
        # Save
        im.save(sample_preamble + str(i) + '.jpg')
        i = i + 1

if __name__ == '__main__':
    print("\n------------------------------------")
    print("----- PascalVOC-to-Images v0.1 -----")
    print("Created by Giovanni Cimolin da Silva")
    print("------------------------------------\n")
    process()
