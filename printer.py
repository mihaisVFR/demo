from constants import *
from PIL import Image as Pic
from PIL import ImageWin
from win32print import GetDefaultPrinter
from win32ui import CreateDC as win32ui_CreateDC
from qrcode import make as qrcode_make


def make_qr(qr_data):
    qr = qrcode_make(qr_data, box_size=5)
    qr_print = qrcode_make(qr_data, box_size=1)
    qr.save("tmpqr.png")
    qr_print.save("print_qr.png")


def print_text(text, h_dc):
    x = 0
    y = 30
    string = text.split("\n")
    h_dc.StartPage()
    for line in string:
        h_dc.TextOut(x, y, line)
        y += 30
    h_dc.EndPage()


def print_qr(file_name, h_dc):

    printable_area = h_dc.GetDeviceCaps(HORZRES), h_dc.GetDeviceCaps(VERTRES)
    printer_size = h_dc.GetDeviceCaps(PHYSICALWIDTH), h_dc.GetDeviceCaps(PHYSICALHEIGHT)

    bmp = Pic.open(file_name)
    if bmp.size[0] > bmp.size[1]:
        bmp = bmp.rotate(90)

    ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
    scale = min(ratios)
    h_dc.StartPage()
    dib = ImageWin.Dib(bmp)
    scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
    x1 = int((printer_size[0] - scaled_width) / 2)
    y1 = int((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw(h_dc.GetHandleOutput(), (x1, y1+30, x2, y2+30))
    h_dc.EndPage()


def print_receipt(text, file_path="", receipt="", image=False):
    separator = f" \n \n \n \n  {'_' * 23}"
    h_dc = win32ui_CreateDC()
    h_dc.CreatePrinterDC(GetDefaultPrinter())  # "KPOS_58 Printer"
    h_dc.StartDoc(f"Printing receipt {receipt}")
    print_text(text, h_dc)
    if image:
        print_qr(file_path, h_dc)
    print_text(separator, h_dc)
    h_dc.EndDoc()
    h_dc.DeleteDC()
