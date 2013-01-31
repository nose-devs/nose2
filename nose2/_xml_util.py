#This module contains some xml utility functions which may
#be of use in multiple places

import six, sys, re

#six doesn't include a unichr function
def _unichr(string):
    if six.PY3:
        return chr(string)
    else:
        return unichr(string)

#etree outputs XML 1.0 so the 1.1 Restricted characters are invalid.
#and there are no characters that can be given as entities aside
#form & < > ' " which ever have to be escaped (etree handles these fine)
ILLEGAL_RANGES = [ (0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), 
                   (0xD800, 0xDFFF), (0xFFFE, 0xFFFF) ]
#0xD800 thru 0xDFFF are technically invalid in UTF-8 but PY2 will encode
#bytes into these but PY3 will do a replacement

#Other non-characters which are not strictly forbidden but
#discouraged.
RESTRICTED_RANGES = [ (0x7F, 0x84), (0x86, 0x9F), (0xFDD0, 0xFDDF) ]
#check for a wide build
if sys.maxunicode > 0xFFFF:
    RESTRICTED_RANGES += [ (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), 
                            (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF), 
                            (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF), 
                            (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF),
                            (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF), 
                            (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF), 
                            (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF),
                            (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF) ]

ILLEGAL_REGEX_STR = six.u('[') + \
                    six.u('').join(["%s-%s" % (_unichr(l), _unichr(h)) 
                                   for (l, h) in ILLEGAL_RANGES]) + \
                    six.u(']')
RESTRICTED_REGEX_STR = six.u('[') + \
                       six.u('').join(["%s-%s" % (_unichr(l), _unichr(h))
                                      for (l, h) in RESTRICTED_RANGES]) + \
                       six.u(']')

_ILLEGAL_REGEX = re.compile(ILLEGAL_REGEX_STR, re.U)
_RESTRICTED_REGEX = re.compile(RESTRICTED_REGEX_STR, re.U)

def string_cleanup(string, keep_restricted=False):

    if not issubclass(type(string), six.text_type):
        string = six.text_type(string, encoding='utf-8', errors='replace')

    string = _ILLEGAL_REGEX.sub(six.u('\uFFFD'), string)
    if not keep_restricted:
        string = _RESTRICTED_REGEX.sub(six.u('\uFFFD'), string)

    return string



