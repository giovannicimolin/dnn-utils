import csv
import sys, os
import numpy as np
import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def load_csv(filename):
    # Open ground truth file
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        kept2 = [row for row in reader]
    for item in kept2:
        for key, value in item.items():
            try:
                item[key] = int(value)
            except ValueError:
                try:
                    item[key] = float(value)
                except:
                    item[key] = value
    return kept2

def convert_box_to_center_point(network_output):
    output = []
    for item in network_output:
        output.append({
            'filename': item['filename'],
            'x': int((item['xmax']-item['xmin'])/2+item['xmin']),
            'y': int((item['ymax']-item['ymin'])/2+item['ymin'])
        })
    print("Converted {} squares to points...".format(len(output)))
    return output

def evaluate_network_results(ground_truth, network_output):
    # Set up output
    evaluated = []
    stats = {}
    # Get ground truth file set
    file_set = set([item['filename'] for item in ground_truth])
    # Iterate over each image on
    for image_file in file_set:
        print('Evaluating: {}...'.format(image_file))
        # Performance metrics
        detections = 0
        multiple_detections = 0
        real_detections = 0
        missing_detections = 0
        false_detections = 0
        # Get only images that are being analyzed here
        network_image_set = [item for item in network_output if item['filename']==image_file]
        to_remove = []
        # Get only squares from this file
        squares = get_squares_from_image(ground_truth, image_file)
        # Iterate over each square
        for square in squares:
            detections_in_square = 0
            poly = [square['x']-15, square['x']+15, square['y']-15, square['y']+15]
            bbPath = mplPath.Path(np.array([[poly[0], poly[1]],
                     [poly[1], poly[2]],
                     [poly[2], poly[3]],
                     [poly[3], poly[0]]]))

            # Now, for each detected point
            for item in network_image_set:
                if bbPath.contains_point((item['x'], item['y'])):
                    detections_in_square = detections_in_square + 1
            if detections_in_square > 0:
                detections += detections_in_square
                real_detections += 1
                if detections_in_square > 1:
                    multiple_detections += detections_in_square - 1
            else:
                missing_detections += 1
        if len(network_image_set) > 0:
            false_detections += len(network_image_set)
        tt = int(len(squares))
        print("Total: " + str(real_detections))
        print("Real: " + str(tt))
        print("Total %: " + str(real_detections/tt*100))
        # print("Errors: " + str(false_detections))
        # print("Errors %: " + str(false_detections/(real_detections+1)*100))

        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # for square in squares:
        #     poly = [square['x']-15, square['x']+15, square['y']-15, square['y']+15]
        #     ax.add_patch(
        #         patches.Rectangle(
        #             (poly[0], poly[2]),
        #             poly[1]-poly[0],
        #             poly[3]-poly[2],
        #             fill=False      # remove background
        #         )
        #     )
        # ax.set_xlim(0,512)
        # ax.set_ylim(0,512)
        # for item in network_output:
        #     plt.scatter(item['x'], item['y'])
        # print(detections_in_square)
        # plt.show()

    return 0

def get_squares_from_image(image_data, image_file):
    return [item for item in image_data if item['filename']==image_file]

def remove_bellow_threshold(image_set, threshold):
    print(image_set[0])
    return [
        item for item in image_set if item['score'] >= threshold
    ]

# Main program
if __name__ == "__main__":
    # Get parameters
    try:
        truth = sys.argv[1]
        image_types = sys.argv[2].split(',')
        networks = sys.argv[3].split(',')
        threshold = float(sys.argv[4])
    except:
        truth = 'all'
        image_types = ['rgb', 'vvi', 'gvi']
        networks = [
            'ssd_inception_v2_coco',
            'faster_rcnn_resnet101_coco',
            'faster_rcnn_inception_resnet_v2_atrous_coco'
        ]
        threshold = 0.5

    # Print information
    print('-----------------------------')
    print('- Tree count evaluator v0.1 -')
    print('By Giovanni Cimolin da Silva')
    print('-----------------------------')
    print('Ground truth: {}'.format(truth))
    print('Image types: {}'.format(image_types))
    print('Networks: {}'.format(networks))

    # Load ground truth
    if truth=='all':
        ground_truth = load_csv('output.csv')
    else:
        ground_truth = load_csv('test_labels.csv')

    # Get ground truth file set
    file_set = set([item['filename'] for item in ground_truth])

    # Iterate over every image type and over every network
    for image_type in image_types:
        for network in networks:
            # Load network output file
            network_output = load_csv(
                '{}/{}/map/boxes.csv'.format(image_type, network))
            # Remove all items that are not in the ground truth
            trimmed_network_output = \
                [box for box in network_output if box['filename'] in file_set]
            # Remove all items bellow threshold
            threshold_network_output = remove_bellow_threshold(trimmed_network_output, threshold)
            # Transform network box output to tree center point
            point_network_output = convert_box_to_center_point(threshold_network_output)
            # Run evaluation
            results = evaluate_network_results(convert_box_to_center_point(ground_truth), point_network_output)
            print(results)
