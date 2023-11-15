import win32print
import win32api

import tempfile
import win32api
import win32print
from http.server import BaseHTTPRequestHandler, HTTPServer
import qrcode
import win32print
import win32ui
import pyqrcode


x = 0  # ОТСТУПЫ
# y = 50
# # printer_name = "KPOS_58 Printer"
# # if your printer is standard, replace the printer_name:
# # win32print.GetDefaultPrinter()
# multi_line_string = "ejnejbnejbnejbnejbnejbneb\nekjfvberjknvejrrvnerkjvne\nnwjrnwrjgnewrjgnvewrjg\nkwjbwkrjbnwrjknwerjk\n"
# string = multi_line_string.split("\n")
# # with open("21.txt", "r", encoding = "utf-8") as fd:
# #     input_string = fd.read()
# #     multi_line_string = input_string.splitlines()
#
# hDC = win32ui.CreateDC()
# hDC.CreatePrinterDC()
# hDC.StartDoc("Printing...")
# hDC.StartPage()
# for line in string:
#     hDC.TextOut(x, y, line)
#     y+=50
#
# hDC.EndPage()
# hDC.EndDoc()





# import win32print
# import win32ui
#
# x = 0
# y = 50
# printer_name = "EPSON L382 Series (копия 1)"
# # if your printer is standard, replace the printer_name:
# # win32print.GetDefaultPrinter()
#
# fd = open("file.txt", "r", encoding = "utf-8")
# input_string = fd.read()
# multi_line_string = input_string.splitlines()
#
# hDC = win32ui.CreateDC()
# hDC.CreatePrinterDC()
# hDC.StartDoc("Printing...")
# hDC.StartPage()
# for line in multi_line_string:
# hDC.TextOut(x, y, line)
# y+=50
# hDC.EndPage()
# hDC.EndDoc()
# fd.close

x = 0
y = 50
# printer_name = win32print.GetDefaultPrinter()  # "KPOS_58 Printer"
# hPrinter = win32print.OpenPrinter(printer_name)
print_text = "fghjljkjhgfhjhjg\nghhjhkkhgfgfhjkhgf\nxcvhjkljhgfhjkljlgf\nfxdfghjlkkgcfghjhgjf\n"
string = print_text.split("\n")

hDC = win32ui.CreateDC()
hDC.CreatePrinterDC()
hDC.StartDoc("Printing...")
hDC.StartPage()
for line in string:
    hDC.TextOut(x, y, line)
    y += 50

hDC.EndPage()
hDC.EndDoc()
# win32print.ClosePrinter(hPrinter)