import pyqrcode
import qrcode

url = pyqrcode.create("12345675352341")
print(url.terminal())


def make_qr(qr_input):
    qr = qrcode.make(qr_input, box_size=5)
    qr.save("tmpqr.png")
    print("sdfsf")

make_qr("sgsgwrt56356365jsrjy")