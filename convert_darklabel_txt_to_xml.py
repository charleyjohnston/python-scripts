#convert_darklabel_txt_to_xml.py
#Converts output file from DarkLabel (in the form frame#,n[x1,y1,x2,y2,label])
#to an XML file 
#Author: Charley Johnston
#Date: December 2, 2018

import os
import fnmatch
import datetime
import time
import sys
import cv2
from lxml import etree

#############################################################################

def find_files(directory, pattern):
   for root, dirs, files in os.walk(directory):
       for basename in files:
           if fnmatch.fnmatch(basename, pattern):
               filename = os.path.join(root, basename)
               yield filename
               
#############################################################################
               
def find_image_name(imagepath):
        
    index = find_str(imagepath, "vlabs")
    imagename = ""
    
    while imagepath[index] != ".":
        imagename = imagename + imagepath[index]
        index = index + 1
        
    imagename = imagename + ".jpg"
    
    return imagename

#############################################################################

def find_frame_number(imagename):
        
    index = find_str(imagename, "image")
    index = index + 5
    framenum = ""
    
    while imagename[index] != ".":
        framenum = framenum + imagename[index]
        index = index + 1
    
    return int(framenum)

#############################################################################
               
def find_str(s, char):
   index = 0

   if char in s:
       c = char[0]
       for ch in s:
           if ch == c:
               if s[index:index+len(char)] == char:
                   return index

           index += 1

   return -1

#############################################################################

#Extract xmin, ymin, xmax, ymax, and the label name from the line from the file
def get_values_from_line(line, num_objects):

    global frames, labels, xmin, xmax, ymin, ymax, img_height, img_width

    index = 0
    temp = ""

    #frame_index
    while line[index] != ",":
        temp = temp + line[index]
        index = index + 1

    #frame N
        
    index = index + 1
    temp = ""

    while line[index] != ",":
            temp = temp + line[index]
            index = index + 1


    for i in range(int(num_objects)):

######################################## #xmin

        temp = ""
        index = index + 1
        
        while line[index] != ",":
            temp = temp + line[index]
            index = index + 1

        index = index + 1

        x_min = int(temp)
        if x_min < 0:
            x_min = 0
        xmin.append(x_min)

######################################## #ymin

        temp = ""
        
        while line[index] != ",":
            temp = temp + line[index]
            index = index + 1

        index = index + 1

        y_min = int(temp)
        if y_min < 0:
            y_min = 0
        ymin.append(y_min)

######################################## #xmax
        
        temp = ""

        while line[index] != ",":
            temp = temp + line[index]
            index = index + 1

        index = index + 1
        x_max = int(temp) 
        if x_max > int(img_width):
            x_max = int(img_width)
        xmax.append(x_max)


######################################## #ymax
        
        temp = ""

        while line[index] != ",":
            temp = temp + line[index]
            index = index + 1

        index = index + 1
        y_max = int(temp)
        if y_max > int(img_height):
            y_max = int(img_height)
        ymax.append(y_max)

######################################## #label
        
        temp = ""

        while line[index] != "\n" and line[index] != ",":
            temp = temp + line[index]
            index = index + 1

        label = temp
        labels.append(label)

#############################################################################

#Get number of objects in the frame
def get_num_objects(line):

    index = 0
    commas = 0

    while line[index] != "\n":
        if line[index] == ",":
            commas = commas + 1
        index = index + 1

    #print "Objects: " + str(commas/5)
    #print line

    return int(commas/5)

#############################################################################

#Writes values to xml file with same name as image
def write_to_xml(num_objects):

        global frames, frames_path, labels, xmin, xmax, ymin, ymax, directory_to_save_xml

        image_name = frames[0]
        name_in_xml = image_name.split(".", 1)[0]

        image_path = frames_path[0]
        image_raw = cv2.imread(image_path)
        height, width, channel = image_raw.shape

        root = etree.Element("annotation")
        etree.SubElement(root, "folder").text = "images"
        etree.SubElement(root, "filename").text = image_name
        size = etree.SubElement(root, "size")
        etree.SubElement(root, "segmented").text = str(0)
        etree.SubElement(size, "width").text = str(width)
        etree.SubElement(size, "height").text = str(height)

        for i in range(num_objects):
            
            x_min = xmin[i]
            x_max = xmax[i]
            y_min = ymin[i]
            y_max = ymax[i]
            label = labels[i]

            obj = etree.SubElement(root, "object")
            etree.SubElement(obj, "name").text = label
            bndbox = etree.SubElement(obj, "bndbox")
            etree.SubElement(bndbox, "xmin").text = str(x_min)
            etree.SubElement(bndbox, "ymin").text = str(y_min)
            etree.SubElement(bndbox, "xmax").text = str(x_max)
            etree.SubElement(bndbox, "ymax").text = str(y_max)

            if not os.path.exists(directory_to_save_xml):
                os.makedirs(directory_to_save_xml)

            with open(directory_to_save_xml + name_in_xml +'.xml', 'wb') as f:
                f.write(etree.tostring(root, pretty_print=True))

        for i in range(num_objects):

            del xmin[0]
            del xmax[0]
            del ymin[0]
            del ymax[0]
            del labels[0]

        del frames_path[0]
        del frames[0]

#############################################################################
            
path = "C:/Users/Charley/Desktop/annotated/paperplate_napkins_papercup/images"
directory_to_save_xml = "C:/Users/Charley/Desktop/annotated/paperplate_napkins_papercup/xmls/"

frames_path = []
frames = []
labels = []
xmin = []
xmax = []
ymin = []
ymax = []

count = 0
time_start = time.time()

for imagepath in find_files(path,'*.jpg'):
    
        imagename = find_image_name(imagepath)
        framenum = find_frame_number(imagename)
        frames_path.append(imagepath)
        frames.append(imagename)

path_to_get_size = frames_path[0]
image_raw = cv2.imread(path_to_get_size)
img_height, img_width, channel = image_raw.shape

#Load lines from file into list
with open('gt.txt') as f:
    lines = f.readlines()

    for line in lines:

        count = count + 1
        
        num_objects = get_num_objects(line)
        get_values_from_line(line, num_objects)
        write_to_xml(num_objects)

print "Time elapsed: " + str(time.time() - time_start) + " seconds. Number of xml files generated: " + str(count) + "."
        
    
