f = open('output.csv','r')
f.readline()
x = []
for item in f.readlines():
	x.append(item)
image_set = set()
for item in x:
	image_set.add(item.split(',')[0])
result = {}
temp = []
for image in image_set:
	temp = []
	temp = [s for s in x if image in s]
	result[image] = temp
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
for image_file in result:
     source_img = Image.open("images/"+image_file).convert("RGB")
     draw = ImageDraw.Draw(source_img)
     for box in result[image_file]:
             name, sizex, sizey, dclass, xmin, ymin, xmax, ymax = box.split(',')
             draw.rectangle([(int(xmin), int(ymin)), (int(xmax), int(ymax))], fill="black")
     source_img.save("out_"+image_file, "JPEG")


for image_file in result:
     source_img = Image.open("images/"+image_file).convert("RGB")
     source_img.save("output/"+image_file, "JPEG")
