# printers values
HORZRES = 8
VERTRES = 10
LOGPIXELSX = 88
LOGPIXELSY = 90
PHYSICALWIDTH = 110
PHYSICALHEIGHT = 110
PHYSICALOFFSETX = 5
PHYSICALOFFSETY = 5
# commands of power board
TURN_ON = b'\x02\x06\x00\xff\x11\x01\xe9\x03'
TURN_OFF = b'\x02\x06\x00\xff\x11\x00\xe8\x03'
# commands for init validator KD10
CMD1 = b"\x02\x00\xa1\xc0\x08\x03"
CMD2 = b"\x02\x03\xa8\x01\x01\x87\x50\x52\x03"
CMD3 = b"\x02\x04\xac\xf0\x00\x00\x00\xa2\x87\x03"
CMD4 = b"\x02\x04\xa6\x00\x00\x00\x00\x09\x86\x03"
CMD5 = b"\02\x02\xa4\x01\x00\x41\xef\x03"
RESP_45 = b"\02\x02\x45\x06\x00\x13\xe9\x03"  # Response "Deposit_ready_ok cmd6
CMD_B1 = b'\x02\x00\xB1\xC1\xC4\x03'  # User ready
CMD_B2 = b'\x02\x00\xB2\x81\xC5\x03'  # Deposit start
CMD_B5 = b'\x02\x00\xb5\xc0\x07\x03'  # reset error
RESP_48 = b"\x02\x02\x48\x06\x00\x82\x2a\x03"  # answer 48 command Send Error information
RESP_HOP_OFF = b"\x02\x02\x21\x06\x00\x52\x36\x03"  # hopper off
RESP_HOP_ON = b"\x02\x02\x22\x06\x00\xa2\x36\x03"  # hopper on
RESP_REJ_ON = b"\x02\x02\x27\x06\x00\xb2\x37\x03"  # reject on
RESP_REJ_OFF = b"\x02\x02\x28\x06\x00\x82\x34\x03"  # reject off
RESP_B5 = b"\x02\x02\x41\x06\x00\x52\x28\x03"  # answer for b5 command
RESP_24 = b"\x02\x02\x24\x06\x00\x42\x37\x03"  # answer for 24 command

REJECT_GROUP = {b"01": "Ошибка распознавания", b"02": "Ошибка SC ", b"03": "Потеряна информация Reco",
                       b"04": "Ошибка цепочки", b"05": "Неверный размер", b"06": "Неверный карман",
                       b"07": "Amount Ошибка пачки (переполнение)", b"08": "Denom Ошибка пачки (переполнение)",
                       b"09": "Нераспознан номинал"}

RECO_ERROR = {
    "Insert_Jam": b"1001", "No_NN_Patern": b"1101", "Wrong_NN_Patern": b"1201",
    "No_PCA_Patern": b"1301", "Wrong_PCA_Patern": b"1401", "Wrong_RP → _No_MNY": b"1501",
    "Wrong_RPC → _Wrong_MNY": b"1601", "DSF_Queue_Overflow →  _No_SVM": b"1701",
    "DSF_Abnormal_Size → _Wrong_SVM": b"1801", "No_Reco_Param_": b"1901",
    "Internal_Index_Sync_Error → _Wrong_Reco_Param": b"2001", "No_Reco_Param": b"2101",
    "No_Reco_Param_Config": b"2201", "No_Sensor_Data": b"3001", "Insert_Chain": b"0102",
    "US_TS_Double": b"0202", "IRT_Double  → _IR_Double": b"0302", "Image_Double": b"0402",
    "MG_Radian_Limit_Over": b"0502", "Too_Much_Skew": b"0602", "Image0_Paralle_Lines_Error": b"0802",
    "Image1_Parallel_Lines_Error": b"0902", "Image0_Apexs_Out_Of_Range_Error": b"1002",
    "Image1_Apexs_Out_Of_Range_Error": b"1102", "Image0_Overflow_Into_Range_Error": b"1202",
    "Image1_Overflow_Into_Range_Error": b"1302", "Image0_Too_Little_Edge_Data_Error": b"1402",
    "Image1_Too_Little_Edge_Data_Error": b"1502", "Image_Out_Of_Scan_Area_Error_Top": b"1602",
    "Image_Out_Of_Scan_Area_Error_Bottom": b"1702", "Image_Out_Of_Scan_Area_Error_Left": b"1802",
    "Image_Out_Of_Scan_Area_Error_Right": b"1902", "Find_Image_Centering_Info_Error": b"2002",
    "US_Preprocessing_Error": b"3202", "UV_Preprocessing_Error": b"3302",
    "MG_Preprocessing_Error": b"3402", "TS_Preprocessing_Error": b"3502", "IRT_Double": b"3602",
    "VLT_Double": b"3702", "Invalid_Size": b"0103", "Not_Matched_Denom": b"0203", "Reco_Chain": b"0303",
    "Over_Batch": b"0403", "Not_Defined_Denom": b"0503", "Other_Denom": b"0603", "Other_Face_Orient":
        b"0703", "Too_Close_2nd_Candidate": b"0803", "Pattern_Making_Failure": b"0903", "Insert_Change_Reco"
    : b"1003", "SN_Denom_Reco_Fail": b"1103", "Not_Matching_Size": b"0104", "Suspect_MG": b"0105",
    "Suspect_IRR": b"0205", "Suspect_IRT": b"0405", "Suspect_UV": b"0805",
    "Suspect_VLT → _Suspect_CF_RFU1": b"1005", "Suspect_RGB → _Suspect_CF_RFU2": b"2005",
    "Suspect_CF_RFU3": b"4005", "Suspect_CF_RFU4": b"8005", "Tape": b"0106", "Deink": b"0206",
    "Stain": b"0306", "Hologram": b"0406", "UV_Washed": b"0506",
    "Missing_Corner": b"0107", "Tear": b"0207", "Hole": b"0307", "DogEar": b"0407",
    "Oil": b"0507", "Unfit": b"0607", "Not_Supported_Banknote": b"0108",
    "No_Serial_Number_Face": b"0208", "Unknown_Denomination": b"0308",
    "Blob_Number_Overflow_": b"0408", "Too_Big_Blob": b"0508", "Mismatched_Digit_Number_of_SN":
        b"0608", "Too_Many_Mismatched_SN": b"0708", "Black_List_Detect": b"0808", "OCR_Image_preprocess":
        b"9108", "Image_Size_Over": b"9208", "Blob_Number_Overflow": b"9308", "Load_SVN_Model": b"9408",
    "Undefined_SN_Function": b"9508", "Undefined_SN_Rotate_Opt": b"9608",
    "Not_Matched_RPC_SVM_Patern": b"9708", "Suspect_Composite_CF": b"0209", "Barcode_Reading_Error":
        b"010a", "Unknown_Barcode_Error": b"020a", "Start_End_Mismatch_Error": b"030a",
    "Parity_Mismatch_Error": b"040a", "Bar_Number_Mismatch_Error": b"050a",
    "Too_Many_Noise_Error": b"060a", "Multi_Error_4": b"0f06", "Counterfeit_UV_MG_IRR_IRT": b"0f05",
    "Multi_Error_3": b"0f04", "Multi_Error_2": b"0f03", "Multi_Error_": b"0f02",
    "Multi_Error_1": b"0f01"
}

# self.cmd_tst_d_r = b"\x02\x02\xa4\x06\x03\x03\xde\x03"  # switch to test sc mode deposit\reject
# self.cmd_tst_off = b"\x02\x02\xa4\x01\x01\x80\x2f\x03"  # switch to normal sc mode 1
# self.cmd_tst_off1 = b"\x02\x02\xa4\x01\x02\xc0\x2e\x03"  # switch to normal sc mode 2
# self.cmd_tst_off2 = b"\x02\x02\xa4\x01\x04\x40\x2c\x03"  # switch to normal sc mode 3
# self.feed_motor_on = b"\x02\x01\xc5\x01\xb2\x90\x03"
# self.feed_motor_off = b"\x02\x01\xc5\x00\x73\x50\x03"
# self.main_motor_on = b'\x02\x01\xc7\x01\xb3\xf0\x03'
# self.main_motor_off = b'\x02\x01\xc7\x00\x72\x30\x03'
# self.get_env = b"\x02\x02\x65\x00\x00\x11\x83\x03"
# self.get_a2 = b"\x02\x00\xa2\x80\x09\x03" # Request version
# self.cmd_a5 = b"\x02\x00\xa5\xc1\xcb\x03"  # check status
# self.cmd_71 = b"\x02\x00\x71\xc1\x94\x03"  # sensor status
# self.cmd6 = b'\x02\x01\xca\x00\x76\xa0\x03'  # switch devertor to reject
# self.cmd7 = b'\x02\x01\xca\x01\xb7\x60\x03'  # switch devertor to deposit