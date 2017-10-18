# grasshopper-kml2xml
import paddocks from kml to grasshopper xml file

Tested only with polygons exported from [Google MyMaps](mymaps.google.com) on Python 3.x on Ubuntu Linux.

Dependencies: pykml, lxml, utm

How it works
------------
1. The Pykml parser is looking for all "Placemark"-tags inside the kml file. 
2. The program reads out all the polygon's coordinates and transforms them to UTM coordinate system. 
3. This coordinates are written to a bare FarmFile. Missing values are automatically added by the Grasshopper app upon the first measuring.

#What can I do with the output file?
------------------------------------
Copy the *.xml FarmFile to your Smartphone. Put it into folder "Grasshopper", so that the Grasshopper app can see the newly created Farmfile. Start using your new farm.

#Known limitations
------------------
- Polygons with more than 16 points may not behave correctly. Maybe the Grasshopper device may not work with a resulting FarmFile. <br> **Solution:** only use simplified polygons with up to 16 points.
