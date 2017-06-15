from initialize import *
from audit_phone_numbers import *

#mapping the node IDs to the phone numbers
phone_numbers_dict={
    '2565708227':'+12129669983',
    '3147863535':'+12122199545'
}

phone_number_chars=set('+0123456789')

def clean_phone_numbers(elem):
    for tag in elem.iter('tag'):
        keytext=tag.attrib['k']
        if keytext.find('phone')>-1:
            orig_phone=tag.attrib['v']
            phone=orig_phone.translate(None,' )(-.')
            if len(phone)==10: 
                phone='+1'+phone
            if len(phone)==11 and phone[0]=='1':
                phone='+'+phone
            if len(phone)!=12:
                phone=phone_numbers_dict[elem.attrib['id']]
            tag.set('v',phone)
    return elem
    
for elem in get_element(OSM_FILE):
    elem=clean_phone_numbers(elem)
    audit_phone_numbers(elem)

print phone_number_chars
