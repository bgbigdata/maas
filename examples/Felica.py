# coding: utf-8
import nfc
import binascii
import time
import requests
import json
from threading import Thread, Timer

from sense_hat import SenseHat

sense = SenseHat()
R = [255, 0, 0]
G = [0, 255, 0]
O = [0, 0, 0]

green_check = [
O, O, O, O, O, O, O, G,
O, O, O, O, O, O, G, G,
O, O, O, O, O, G, G, O,
G, O, O, O, G, G, O, O,
G, G, O, G, G, O, O, O,
O, G, G, G, O, O, O, O,
O, O, G, O, O, O, O, O,
O, O, O, O, O, O, O, O
]
red_cross = [
R, O, O, O, O, O, O, R,
R, R, O, O, O, O, R, R,
O, R, R, O, O, R, R, O,
O, O, R, R, R, R, O, O,
O, O, O, R, R, O, O, O,
O, O, R, R, R, R, O, O,
O, R, R, O, O, R, R, O,
R, R, O, O, O, O, R, R
]
heart = [
O, R, O, O, O, O, R, O,
R, R, R, O, O, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
O, R, R, R, R, R, R, O,
O, O, R, R, R, R, O, O,
O, O, O, R, R, O, O, O
]

 # 待ち受けの1サイクル秒
TIME_cycle = 10.0
# 待ち受けの反応インターバル秒
TIME_interval = 0.2
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_wait = 1

# NFC接続リクエストのための準備
# 212F(FeliCa)で設定
target_req_felica = nfc.clf.RemoteTarget("212F")

# 106A(NFC type A)で設定
target_req_nfc = nfc.clf.RemoteTarget("106A")

color = 'g'

url = 'https://prod-25.japaneast.logic.azure.com:443/workflows/5d5618e7a2294861be819e7670dc3723/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=I_LqCnMFnrbKGeRqQMdf5dVBBMlnB2PcxfOekSY--4I'
userAddress = 'testUser'
carKey = 'testCar'

def check_FeliCa():
    global color
    print  'FeliCa waiting...'
    # USBに接続されたNFCリーダに接続してインスタンス化
    clf = nfc.ContactlessFrontend('usb')
    # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
    target_res = clf.sense(target_req_felica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
    if not target_res is None:
        tag = nfc.tag.activate(clf, target_res)

        #IDmを取り出す
        idm = binascii.hexlify(tag.idm)
        print 'FeliCa detected. idm = ' + idm
        
        if color == 'r':
            operateKey(url, userAddress, carKey, 'UnlockCar')
            sense.set_pixels(green_check)
            color = 'g'
        elif color == 'g':
            operateKey(url, userAddress, carKey, 'LockCar')
            sense.set_pixels(red_cross)
            color = 'r'

        #sleepなしでは次の読み込みが始まって終了する
        print 'sleep ' + str(TIME_wait) + ' seconds'
        time.sleep(TIME_wait)

    clf.close()
    
def operateKey(url, userAddress, carKey, keyOperation):
    response = requests.post(url,
                             json.dumps({'userAddress':userAddress,
                                         'carKey':carKey,
                                         'operation':keyOperation}),
                                         headers={'Content-Type':'application/json'})
    print(response.status_code)
    if response.status_code == 200:
        print(response.json())
        return True
    return False

while True:
    check_FeliCa()

'''
 # 待ち受けの1サイクル秒
TIME_cycle = 10.0
# 待ち受けの反応インターバル秒
TIME_interval = 0.2
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_wait = 3

# NFC接続リクエストのための準備
# 212F(FeliCa)で設定
target_req_felica = nfc.clf.RemoteTarget("212F")

# 106A(NFC type A)で設定
target_req_nfc = nfc.clf.RemoteTarget("106A")

str = 'g'

def check_FeliCa():
    print  'FeliCa waiting...'
    global str
    # USBに接続されたNFCリーダに接続してインスタンス化
    clf = nfc.ContactlessFrontend('usb')
    # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
    target_res = clf.sense(target_req_felica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
    if not target_res is None:
        tag = nfc.tag.activate(clf, target_res)

        #IDmを取り出す
        idm = binascii.hexlify(tag.idm)
        print 'FeliCa detected. idm = ' + idm
        if str == 'r':
            sense.set_pixels(green_check)
            str = 'g'
        elif str == 'g':
            sense.set_pixels(red_cross)
            str = 'r'
        #sleepなしでは次の読み込みが始まって終了する
        time.sleep(TIME_wait)

    clf.close()
#    return {"idm": idm}
#while True:



@route("/NFC")
def check_NFC():
    print  'NFC waiting...'
    # USBに接続されたNFCリーダに接続してインスタンス化
    clf = nfc.ContactlessFrontend('usb')

    mydict = {}
    while True:
        target_res = clf.sense(target_req_nfc,target_req_felica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
        if not target_res is None:
            tag = nfc.tag.activate(clf, target_res)
            print 'TAG type: ' + tag.type

            # FeliCaカードをタッチしたら読み込みをやめる
            if tag.type == "Type3Tag":
                break
            # Type1,Type2:NFCタグ、Type4:Android端末でのNFCなど
            else:
                # NFCタグに埋めたtextを読む
                print tag.ndef
                records = tag.ndef.records
                for record in records:
                    print 'NFC detected. record.text = ' + record.text
                    # str()で変換するとユニコードオブジェクトにならない
                    key = str(record.text)
                    mydict[key] = key

                print 'sleep ' + str(TIME_wait) + ' seconds'
                time.sleep(TIME_wait)
    for dic in mydict :
        print(dic)

    clf.close()

    return {"dic": dic}
'''