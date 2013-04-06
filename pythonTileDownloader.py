# Python tile downloader
#
# Download tiles images from an online tile server
#

#################### IMPORTS

import math
import urllib2
import os

#################### VARIBALES

NW = {"lat" : , "long" : } 
SE = {"lat" : , "long" : }
ZOOM = []
URL = ""


fileFormat = ".png" 
nbDL = 0
normalizedUrl = ""

#################### FUNCTIONS

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def createDownloadDirecotryOrSwitch(directoryName):
    if os.path.exists(directoryName):
        os.chdir(directoryName)
    else:
        os.makedirs(directoryName)
        os.chdir(directoryName)

def isTheFileExists(fileName):
    return os.path.isfile(fileName)

def downloadFile(url, x, y, z):
    global nbDL
    
    if isTheFileExists(str(y) + fileFormat):
        print("/" + str(z) + "/" + str(x) + "/" + str(y) + fileFormat + "\t File already exists")
    else:
        response = urllib2.urlopen(url)
        localFile = open(str(y) + fileFormat, 'wb')
        localFile.write(response.read())
        localFile.close()
        print("/" + str(z) + "/" + str(x) + "/" + str(y) + fileFormat + "\t File downloaded")
        nbDL += 1

def getTileNum(NW, SE, zoom):
    return [deg2num(NW["lat"], NW["long"], zoom), deg2num(SE["lat"], SE["long"], zoom)]

def downloadTiles(NW, SE, zoom):
    global URL
	
    tileNum = getTileNum(NW, SE, zoom)
    nbFiles = (tileNum[1][0] - tileNum[0][0] +1) * (tileNum[1][1] - tileNum[0][1] +1)
    
    createDownloadDirecotryOrSwitch("tiles")
    createDownloadDirecotryOrSwitch(str(zoom))
     
    for x in range(tileNum[0][0], tileNum[1][0]+1, 1):
        createDownloadDirecotryOrSwitch(str(x))
        for y in range(tileNum[0][1], tileNum[1][1]+1, 1):
            url = getDownloadUrl(URL, x, y, zoom) 
            downloadFile(url, x, y, zoom)
        os.chdir(os.pardir)
    os.chdir(os.pardir)
    os.chdir(os.pardir)

def multipleZoomTileDownload(NW, SE, zoom):

    for z in zoom:
        print("Start zoom " + str(z) + "\n")
        downloadTiles(NW, SE, z)
        print("\n" + str(z) + " zoom completed\n")
    print("Download completed")

def getDownloadUrl(url, x, y, z):
  url = url.replace("[x]", str(x)) 
  url = url.replace("[y]", str(y)) 
  url = url.replace("[z]", str(z)) 

  return (url)

#################### MAIN

if (__name__ == "__main__"):
    multipleZoomTileDownload(NW, SE, ZOOM)
