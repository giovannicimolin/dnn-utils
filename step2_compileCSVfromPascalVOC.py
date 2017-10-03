import glob, os, sys
import shutil

import random

from libs import pvoc2img, xml2csv


def main(image_set="1", data_split=30, tile_size=500):
    # Try catching parameters
    try:
        image_set  = sys.argv[1]
        data_split = sys.argv[2]
        tile_size  = sys.argv[3]
    except:
        print("Parameter error! Using defaults...")

    # Set up working directories and paths
    image_set_directory = "datasets/{}".format(image_set)
    os.chdir(image_set_directory)
    owd = os.getcwd() # Save directory for return point

    # Separate classified images from non-classified
    available_files = []
    try:
        os.makedirs("classified_tiles")
    except OSError as e:
        pass
    try:
        os.makedirs("output/images")
    except OSError as e:
        pass
    for file in glob.glob("*.xml"):
        name = file.split(".")[0]
        available_files.append(os.path.basename(name))
        for samename in glob.glob("{}.*".format(name)):
            shutil.copy(samename, "classified_tiles/")
            shutil.copy(samename, "output/images/")

    pvoc2img.process("classified_tiles", count=True)

    # Separate file into train and test samples
    # Get directories ready
    os.chdir("classified_tiles")
    try:
        os.makedirs("train")
        os.makedirs("test")
    except OSError as e:
        pass

    # Shuffle list and copy files
    random.shuffle(available_files)
    test = available_files[0:int(len(available_files)*data_split/100)]
    train = available_files[(int(len(available_files)*data_split/100)+1):]
    for item in train:
        for file in glob.glob("{}.*".format(item)):
            shutil.copy(file, "train/")
    for item in test:
        for file in glob.glob("{}.*".format(item)):
            shutil.copy(file, "test/")

    # Convert to xml
    os.chdir(owd)
    xml2csv.main()

main()
