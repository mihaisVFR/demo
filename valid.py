def validator_init(self):
    self.label_deposit.configure(text="232323")
    port = self.find_in_descriptor("ch a")
    try:
        self.serial_port = serial.Serial(port, 115200, timeout=0.1, inter_byte_timeout=0.1)
        time.sleep(2)
        # Инициализация
        self.send_to_port(CMD1)
        self.send_to_port(CMD2)
        self.send_to_port(CMD3)
        self.send_to_port(CMD4)
        self.send_to_port(CMD5)
        # self.serial_port.flush()
        # self.serial_port.reset_output_buffer()
        # self.serial_port.close()

    except ValueError:
        self.serial_port.close()

    except Exception as e:
        text = f"error open port '{e}'"
        self.write_logs("a+", text)

    if not self.serial_port:
        text = "The validator control port with 'Ch A' was not found in the descriptor."
        self.write_logs("a+", text)


def send_to_port(self, data):
    time.sleep(0.1)
    self.serial_port.write(data)
    # print(f"Отправленно: {binascii.hexlify(data1)}")
    # print(f"Ответ: {binascii.hexlify(self.ser.readline())}")


def start(self):
    # self.read_data_from_port()
    # self.sc_listr = []
    self.sc_list = "22"
    self.label_deposit.configure(text=f"{str(sum(self.sc_list))}")
    self.send_to_port(CMD_B1)
    self.send_to_port(CMD_B2)


def read_data_from_port(self):
    """Считываем данные с порта"""
    print("dvdd")
    len_in_buffer = self.serial_port.in_waiting
    self.serial_port = Power_sitch.se
    if 0 < len_in_buffer < 65:  # чтение любых даннных
        self.data = self.data + self.serial_port.read(len_in_buffer)  # , size=len_in_buffer)
    elif 64 < len_in_buffer:
        self.data = self.data + self.serial_port.read(64)  # В пакете бывает по 2-3 события 64 размер b'23'
    if len(self.data) > 0:
        print(f"\nОтвет  {binascii.hexlify(self.data)}\n")

        #
        event = binascii.hexlify(self.data[2:3])  # байт события a23
        error_hex = binascii.hexlify(self.data[60:61])  # байт ошибки aerr
        denom_hex_first = binascii.hexlify(self.data[52:53])  # номинал просчета 16-ричный adenom
        denom_byte = self.data[52:53]  # adenom1
        denom_hex_second = binascii.hexlify(self.data[53:54])  # adenom2
        reject_reason = binascii.hexlify(self.data[8:10])
        chain_indicator = binascii.hexlify(self.data[10:60])
        #
        # if event == b"48":  # Реакция на 48 событие
        #     self.serial_port.write(self.sen.cmd48)
        #     self.skrtxt.insert(END, f"\nПОЛУЧЕН ОТЧЕТ ОБ ОШИБКЕ СОБЫТИЕ 48\n")
        #     self.skrtxt.tag_configure("cmd_", foreground="red", font=("Arial", 30), justify='center')
        #     self.skrtxt.see("end")
        #
        #         if binascii.hexlify(self.data[2: 3]) == b"21":  # Реакция на 21 on событие
        #             self.ser.write(self.sen.cmd_hopon)
        #             self.skrtxt.insert(END, f"\nБАНКНОТЫ НА HOPPER\n")
        #             self.skrtxt.see("end")
        #
        #         if binascii.hexlify(self.data[2: 3]) == b"22":  # Реакция на 22 on событие
        #             self.ser.write(self.sen.cmd_hopoff)
        #             self.skrtxt.insert(END, f"\nБАНКНОТ НЕТ НА HOPPER\n")
        #             self.skrtxt.see("end")
        #
        #         if binascii.hexlify(self.data[2: 3]) == b"28":  # Реакция на 28 on событие
        #             self.ser.write(self.sen.cmd_rejoff)
        #             self.skrtxt.insert(END, f"\nБАНКНОТ НЕТ В REJECT\n")
        #             self.skrtxt.see("end")
        #
        if binascii.hexlify(self.data[2: 3]) == b"27":  # Реакция на Hopper on событие
            self.start()
        threading.Timer(0.1, self.read_data_from_port).start()  # запускаем функцию read1 заново каждую 0.01
#         if binascii.hexlify(self.data[2: 3]) == b"41":  # Реакция на 41 on событие
#             self.ser.write(self.sen.cmd_answb5)
#             self.skrtxt.insert(END, f"\nПРИНЯТ ОТЧЁТ О СБРОСЕ ОШИБОК\n")
#             self.skrtxt.see("end")
#
#         if binascii.hexlify(self.data[2: 3]) == b"24":  # Реакция на 24 on событие
#
#             self.ser.write(self.sen.cmd_answ24)
#             self.skrtxt.insert(END, f"\nПРИНЯТA КОМАНДА SEND COUNT INFO\n")
#             self.skrtxt.see("end")
#
#         if binascii.hexlify(self.data) == b'00' * 28 or binascii.hexlify(self.data) == b'00' * 29 or \
#                 binascii.hexlify(self.data) == b'00' * 36:  # порт питания открыт не в 9600
#
#             self.btn_pwr_o.configure(state="normal")
#             self.btn_pwr_of.configure(state="normal")
#             self.speed_9600()
#             self.active = False
#             # self.skrtxt.insert(END, f"\nОТКРЫТ ПОРТ УПРАВЛЕНИЯ ПИТАНИЕМ\nНАЖМИТЕ КНОПКУ "
#             #                         f"ВКЛЮЧЕНИЕ/ВЫКЛЮЧЕНИЕ ПИТАНИЯ", "power")
#             # self.skrtxt.tag_configure("power", foreground="Green", font=("Arial", 20, "bold"), justify='center')
#             # self.skrtxt.see("end")
#
#         if binascii.hexlify(self.data[2: 3]) == b"45":  # Реакция на 45 on событие
#             if binascii.hexlify(self.data[3: 4]) == b"00":
#
#                 self.ser.write(self.sen.cmd_answ24)
#                 self.skrtxt.insert(END, f"\nПРИНЯТA КОМАНДА Deposit Ready Status OFF\n\n"
#                                         f"Отправлено\n{self.sen.cmd_answ24}\n")
#                 self.skrtxt.see("end")
#             else:
#                 self.ser.write(self.sen.cmd_answ24)
#                 self.skrtxt.insert(END, f"\nПРИНЯТA КОМАНДА Deposit Ready Status ON\n\n"
#                                         f"Отправлено\n{self.sen.cmd_answ24}\n")
#                 self.skrtxt.see("end")
#
#         if len(self.data) > 1 and self.a23 == b"23" and self.aerr == b"00":  # если событие 23 и нет ошибки
#
#             # Пустой список в инициализации класса
#             if self.adenom1 < b'fe':
#                 self.line = int(self.adenom, 16)  # номинал просчета десятичный
#                 self.sc_list.append(self.line)  # добавляем очередной результат просчета в список
#
#             elif self.adenom1 > b'fe':
#                 # Включение второго байта для купюр номиналом более 200рэ
#                 first = self.adenom
#                 second = self.adenom2
#                 self.lines = (second + first)
#                 self.line = int(self.lines, 16)  # номинал просчета десятичный
#                 self.sc_list.append(self.line)
#
#             self.conf_count_num()  # Вызываем кнопку
#
#         if 1 < len(self.data) and self.aerr in self.sen.reason.keys() \
#                 and self.rejerr != b"0000" and self.a23 != b'24':
#             # если ошибка в списке ошибок и код ошибки отличается от 0000
#             for key, self.value in self.sen.reco_err.items():
#                 if self.rejerr == self.value:
#                     self.sc_listr.append(key)
#                     self.btn_rejj.config(text=f"РЕДЖЕКТ\n         {len(self.sc_listr)}")
#
#         # else:
#         #     pass
#
#         if len(self.data) > 1 and self.a23 == b"23" and self.aduble == b'00' * 50:
#             self.sc_listr.append("Несколько банкнот сразу")
#
#         if self.active:
#             threading.Timer(0.01, self.read1).start()  # запускаем функцию read1 заново каждую 0.01
#
# def conf_count_num(self):
#     if not self.flag_rej_cont:
#         self.btn_cont.config(text=f"ПРОСЧИТАНО\n     {len(self.sc_list)}шт.  {str(sum(self.sc_list))}")
#     elif self.flag_rej_cont:
#         self.btn_cont.config(text=f"ПРОСЧИТАНО\n             {str(sum(self.sc_list))}")
