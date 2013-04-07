# Python tile downloader
# (https://github.com/SaruManiac/PythonTileDownloader)
#
# Download tiles images from online tile server
#
# author          : SaruManiac
# python_version  : 2.7.3 
#============================================================

############################## IMPORTS

import math
import urllib2
import os

############################## VARIBALES

NW = {"lat" : 0, "long" : 0}
SE = {"lat" : 0, "long" : 0}
ZOOM = []
URL = ""

# Do not modify following variables
fileFormat = ".png" 
nbDL = 0
errorUrl = []

############################## FUNCTIONS

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
    global errorUrl
    
    if isTheFileExists(str(y) + fileFormat):
        print("/" + str(z) + "/" + str(x) + "/" + str(y) + fileFormat + "\t\t File already exists")
    else:
      try:
        response = urllib2.urlopen(url)
        localFile = open(str(y) + fileFormat, 'wb')
        localFile.write(response.read())
        localFile.close()
        print("/" + str(z) + "/" + str(x) + "/" + str(y) + fileFormat + "\t File downloaded")
        nbDL += 1
      except urllib2.URLError, e:
        print("/" + str(z) + "/" + str(x) + "/" + str(y) + fileFormat + "\t" + str(e))
        errorUrl.append(url)
        

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

def checkSettings(NW, SE, URL, ZOOM):
  if (NW["lat"] == 0 or NW["long"] == 0):
    print("Invalid NW point : complete gps coordinates")
  if (SE["lat"] == 0 or SE["long"] == 0):
    print("Invalid SE point : complete gps coordinates")
  if (ZOOM == []):
    print("Invalide Zoom option : complete zoom option")
  if (URL == ""):
    print("Invalide URL : complete tile server url")
  if (NW["lat"] < SE["lat"] or NW["long"] > SE["long"]):
    print("Invalide points : check the gps coordinates of the two points")

  if (NW["lat"] != 0 and NW["long"] != 0 and SE["lat"] != 0 and SE["long"] != 0 and ZOOM != [] and URL != "" and NW["lat"] >= SE["lat"] and NW["long"] <= SE["long"]):
    return True
  else:
    return False
  

############################## MAIN

if (__name__ == "__main__"):
  if checkSettings(NW, SE, URL, ZOOM):
    multipleZoomTileDownload(NW, SE, ZOOM)
