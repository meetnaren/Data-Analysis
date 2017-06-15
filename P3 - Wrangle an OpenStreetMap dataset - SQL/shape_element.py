from initialize import *

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    for tag in element.iter('tag'):
        if problem_chars.search(tag.attrib['k']):
            continue
        tagdict={}
        tagdict['id']=element.attrib['id']
        colonpos=tag.attrib['k'].find(':')
        if colonpos>-1:
            tagdict['key']=tag.attrib['k'][colonpos+1:]
            tagdict['type']=tag.attrib['k'][:colonpos]
        else:
            tagdict['key']=tag.attrib['k']
            tagdict['type']=default_tag_type
        tagdict['value']=tag.attrib['v']
        tags.append(tagdict)

    if element.tag == 'node':
        for a in element.attrib:
            if a in node_attr_fields:
                node_attribs[a]=element.attrib[a]
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        for a in element.attrib:
            if a in way_attr_fields:
                way_attribs[a]=element.attrib[a]

        pos=0
        for pos, nd in enumerate(element.iter('nd')):
            nodedict={}
            nodedict['id']=element.attrib['id']
            nodedict['node_id']=nd.attrib['ref']
            nodedict['position']=pos
            way_nodes.append(nodedict)            
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
