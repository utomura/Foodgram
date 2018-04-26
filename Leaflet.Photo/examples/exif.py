import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif(file,field):

    img = Image.open(file)
    exif = img._getexif()


    exif_data = []
    for id, value in exif.items():
        if TAGS.get(id) == field:
            tag = TAGS.get(id, id),value
            exif_data.extend(tag)


    return exif_data

def get_gps(file):
	my_img = file
	img_info = get_exif(my_img,"GPSInfo")

	latitude_ = img_info[1][2]
	latitude = list(latitude_)
	latitude_list = []
	for i in latitude:
	    latitude_list.append(list(i))
	latitude_list[0] = latitude_list[0][0]/latitude_list[0][1]
	latitude_list[1] = latitude_list[1][0]/latitude_list[1][1]
	latitude_list[2] = latitude_list[2][0]/latitude_list[2][1]
	latitudek = latitude_list[0]+latitude_list[1]/60 + latitude_list[2]/3600
	latitude = "%.6f" %(latitudek)
	longitude_ = img_info[1][4]
	longitude = list(longitude_)
	longitude_list = []
	for i in longitude:
	    longitude_list.append(list(i))
	longitude_list[0] = longitude[0][0]/longitude[0][1]
	longitude_list[1] = longitude[1][0]/longitude[1][1]
	longitude_list[2] = longitude[2][0]/longitude[2][1]
	longitudek = longitude_list[0]+longitude_list[1]/60+longitude_list[2]/3600
	longitude = "%.6f" %(longitudek)

	return latitude, longitude
