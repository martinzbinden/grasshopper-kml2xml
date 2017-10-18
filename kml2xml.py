#!/usr/bin/env python

##import libraries  (check manually if installed! if not, do install first)
import os
from pykml import parser
from lxml import etree as et
import utm
import easygui

print "Choosing file from dialog, or set filename in script file"

################################
## change user settings here
filename = easygui.fileopenbox()
# filename = # set filename statically here if you want (i.e. for debugging)

## end user settings
################################

print "set filename to "+filename


##create output skeleton
root = et.XML('''\
<?xml version="1.0" encoding="UTF-8"?>
<farm id="example farm" sampleCount="10" residual="0" version="2.38" email="mail@example.com" herdCode="1" ieNumber="" animalNO="40" allocationPerPeriod="0" rotationPeriod="0" dmPercent="18" cover="Total Cover" emailCc="" region="Almaigne Nord" discussionGroup="" shareResults="PastureBase" dbUsername="">
</farm>
''')


##read input file
doc = parser.fromstring(open(filename,'r').read())


##extract paddock data
paddocks = []
for paddock in doc.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
    name =  paddock.name
    coordinates = paddock.Polygon.outerBoundaryIs.LinearRing.coordinates
    # conversion of coordinates
    coords = coordinates.text.split('\n')
    coords = [x.strip(' ') for x in coords]    
    coords = filter(None, coords)
    utms =  []
    for xy in coords:
        long =  float(xy.split(',')[0])
        lat =  float(xy.split(',')[1])
        utm_string =  utm.from_latlon(lat, long)[0:2] 
        utm_rounded = [ '%.0f' % elem for elem in utm_string ]
        utms.append(utm_rounded)
    #utms = [ round(elem, 0) for elem in utms ]
    #print name, utms
    paddocks.append([name, utms])


##transform paddock coordinates
paddocklist = []
for paddock in paddocks:
    p =  et.SubElement(root, "paddock", id=str(paddock[0]))
    for i in range(0,len(paddock[1])-1):
        j = i
        east = et.SubElement(p, "point"+str(i)+"east")
        east.text = paddock[1][j][0]
        north = et.SubElement(p, "point"+str(i)+"north")
        north.text = paddock[1][j][1]
        p.extend(east)
        p.extend(north)
    paddocklist.append(p)
root.extend(paddocklist)
        
## create XML-tree
tree = et.ElementTree(root)

## serialize and print out tree (for debugging)
print "OUTPUT:"
print (et.tostring(tree, pretty_print=True))

## Save tree to XML file
outfilename = os.path.splitext(filename)[0]+'_gh.xml'
outFile = open(outfilename, 'w')
tree.write(outFile, xml_declaration=True, encoding='utf-8') 
print "OUTPUT written to file "+filename

##end
