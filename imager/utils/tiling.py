import cv2

def generate_tiles(image_path, output_path, tile_size=512):
    img = cv2.imread(image_path)
    x_tile_num = int(img.shape[0]/tile_size) + 1
    y_tile_num = int(img.shape[1]/tile_size) + 1

    for row in range(x_tile_num):
        for col in range(y_tile_num):
            y0 = row * tile_size
            y1 = y0 + tile_size
            x0 = col * tile_size
            x1 = x0 + tile_size
            cv2.imwrite(output_path + '/tile_%d_%d.jpg' % (row, col), img[y0:y1, x0:x1])

    x_size = x_tile_num * tile_size
    y_size = y_tile_num * tile_size
    return [x_size, y_size]
