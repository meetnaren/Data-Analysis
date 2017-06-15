from initialize import *

phone_number_chars=set()

def audit_phone_numbers(elem):
    for tag in elem.iter('tag'):
        if tag.attrib['k'].find('phone')>-1:
            phone=tag.attrib['v']
            for i in range(len(phone)):
                phone_number_chars.add(phone[i])
    return None

for elem in get_element(OSM_FILE):
    audit_phone_numbers(elem)

print phone_number_chars
