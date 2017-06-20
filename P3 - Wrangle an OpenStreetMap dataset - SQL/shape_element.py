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
    """This function takes in the element tag from the XML file and reshapes the data in the format that we need to load it into the database.

    Args:
        element (XML Element)   : The element that needs to be parsed into the node and way variables
        node_attr_fields (list) : The list of attributes that need to be extracted from the element level tag for the node tags. Defaults to NODE_FIELDS
        way_attr_fields (list)  : The list of attributes that need to be extracted from the element level tag for the way tags. Defaults to WAY_FIELDS
        problem_chars (regex pattern) : A regex compiled pattern with the list of characters that are not acceptable in the element's key tags. Defaults to PROBLEMCHARS
        default_tag_type (str)  : the default type for the tag, when the key of the tag does not have two colon characters. Defaults to 'regular'

    Returns:
        If passed element is a node:
            {
                'node'      : Dictionary of the node's attributes and the corresponding values
                'node_tags' : Dictionary of the node's tags (key, value and type)
            }
        If passed element is a way:
            {
                'way'       : Dictionary of the way's attributes and the corresponding values
                'way_nodes' : Dictionary of the way's node references
                'way_tags'  : Dictionary of the way's tags (key, value and type)
            }
    """
    
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
