import os
import sys
import glob
import uuid
import shutil
import csv

from libs import tfrg

def loadCSV(filename):
    with open(filename, 'rU') as infile:
        # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]
    return data

def getUniqueFilelist(filename):
    data = loadCSV(filename)
    return list(set(data['filename']))

def concatCSV(filelist, output):
    header_saved = False
    with open(output,'w') as fout:
        for filename in filelist:
            with open(filename) as fin:
                header = next(fin)
                if not header_saved:
                    fout.write(header)
                    header_saved = True
                for line in fin:
                    fout.write(line)

def cleanup(session):
    shutil.rmtree("tmp/{}".format(session))

def main():
    print("----------------------------")
    print("  TFRecord generator v0.1   ")
    print("By Giovanni Cimolin da Silva")
    print("----------------------------")

    dataset = sys.argv[1]

    session = str(uuid.uuid4())
    print("Session UID: {}".format(session))

    # Set up working directories and paths
    owd = os.getcwd() # Save directory for return point

    print("Creating directories...")
    # Create tmp dir
    try:
        os.makedirs("tmp/{}/images".format(session))
    except OSError as e:
        pass
    # Create output dir
    try:
        os.makedirs("datasets/{}/TFRecords".format(dataset))
    except OSError as e:
        pass

    print("Locating csv label files...")
    # Find all csv generated from the step before
    train_labels = glob.glob("datasets/{}/train_labels.csv".format(dataset), recursive=True)
    test_labels  = glob.glob("datasets/{}/test_labels.csv".format(dataset), recursive=True)

    # Concatenate all train and test labels
    concatCSV(train_labels, "tmp/{}/train_labels.csv".format(session))
    concatCSV(test_labels, "tmp/{}/test_labels.csv".format(session))

    # Find and copy all the necessary files to the images folder
    print("Copying necessary files...")
    images = getUniqueFilelist("tmp/{}/train_labels.csv".format(session)) +\
             getUniqueFilelist("tmp/{}/test_labels.csv".format(session))

    for image in images:
        for filename in glob.iglob("datasets/{}/images/{}".format(dataset, image), recursive=True):
            shutil.copy2(filename, "tmp/{}/images/".format(session))

    # Open working directory and run TFRecord Generator
    print("Creating TFRecord files...")

    input("Press Enter to continue...")

    os.chdir("tmp/{}/".format(session))
    for item in ["train", "test"]:
        tfrg.main(
            "{}_labels.csv".format(item),
            "../../datasets/{}/TFRecords/{}.record".format(dataset,item)
        )

    # Finishing
    os.chdir(owd)
    print("Successfully created TFRecord files.")
    print("Cleaning up...")
    #cleanup(session)

main()
