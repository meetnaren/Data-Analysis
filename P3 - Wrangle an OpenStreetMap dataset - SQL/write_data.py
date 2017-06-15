from initialize import *
from clean_street_words import *
from clean_zip_codes import *
from clean_phone_numbers import *
from clean_counties import *
from clean_cities import *
from shape_element import *

with codecs.open(NODES_PATH, 'w') as nodes_file, \
     codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
     codecs.open(WAYS_PATH, 'w') as ways_file, \
     codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
     codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

    nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
    node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
    ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
    way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
    way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

    nodes_writer.writeheader()
    node_tags_writer.writeheader()
    ways_writer.writeheader()
    way_nodes_writer.writeheader()
    way_tags_writer.writeheader()

    nodeCount=0
    wayCount=0

    for element in get_element(OSM_FILE):
        element.set('add','True')
        element=clean_street_words(element)
        element=clean_zip_codes(element)
        element=clean_phone_numbers(element)
        element=clean_counties(element)
        element=clean_cities(element)
        if element.attrib['add']=='False':
            continue
        el = shape_element(element)
        if el:
            if element.tag == 'node':
                nodes_writer.writerow(el['node'])
                node_tags_writer.writerows(el['node_tags'])
                nodeCount+=1
            elif element.tag == 'way':
                ways_writer.writerow(el['way'])
                way_nodes_writer.writerows(el['way_nodes'])
                way_tags_writer.writerows(el['way_tags'])
                wayCount+=1

    print "No. of nodes written: ",nodeCount
    print "No. of ways written: ",wayCount
