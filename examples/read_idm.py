# read_idm.py
import binascii
from binascii import hexlify
import nfc
import urllib2

class MyCardReader(object):
    def on_connect(self, tag):
        print 'touched'
        self.idm = binascii.hexlify(tag.idm)
        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')
        print clf
        try:
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()

print __name__ 

if __name__ == '__main__':
    cr = MyCardReader()
    while True:
        print "touch card:"
        cr.read_id()
        print "released"
        print tag
        print cr.idm