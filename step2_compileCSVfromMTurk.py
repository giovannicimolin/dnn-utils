import glob, os, sys
import shutil
import random
import pandas
from libs import pvoc2img, xml2csv

def separate_images(train, test):
    try:
        os.makedirs("train")
        os.makedirs("test")
    except OSError as e:
        pass

    for filename in train:
        shutil.copy("images/{}".format(filename), "train/")
    for filename in test:
        shutil.copy("images/{}".format(filename), "test/")

def main(image_set="rgb", separate=False, data_split=30, tile_size=512):
    # Try catching parameters
    try:
        image_set  = sys.argv[1]
        separate = sys.argv[2]
        data_split = sys.argv[3]
        tile_size  = sys.argv[4]
    except:
        print("Using defaults...")

    # Set up working directories and paths
    image_set_directory = "datasets/{}".format(image_set)
    os.chdir(image_set_directory)
    owd = os.getcwd() # Save directory for return point

    # Read all files and split the dataset in images
    csv = pandas.read_csv('output.csv', sep=',')
    image_files = list(set(csv['filename']))
    random.shuffle(image_files)
    test  = image_files[0:int(len(image_files)*data_split/100)]
    train = image_files[(int(len(image_files)*data_split/100)+1):]

    train_dataset = csv[csv['filename'].isin(train)]
    test_dataset = csv[csv['filename'].isin(test)]

    train_dataset.to_csv('train_labels.csv', index=False)
    test_dataset.to_csv('test_labels.csv', index=False)

    # Separate images into train and test folders if asked
    if separate:
        separate_images(train, test)

main()
