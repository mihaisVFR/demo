def caesar_cipher(text, shift):  # encode shift/ decode -shift
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюяё'
    result = []
    lower_text = text.lower()
    for char in lower_text:
        if char in alphabet:  # Добавляем 'ё'
            shift_amount = shift % 33  # Теперь 33 символа (32 буквы + 'ё')
            new_char = alphabet[(alphabet.index(char) + shift_amount) % 33]
            result.append(new_char)
        elif char.isdigit():  # Шифруем цифры
            shift_amount = shift % 10
            new_char = chr(((ord(char) - ord('0') + shift_amount) % 10) + ord('0'))
            result.append(new_char)
        else:  # Шифруем специальные символы
            if 33 <= ord(char) <= 47:  # ASCII-коды для !"#$%&'()*+,-./
                shift_amount = shift % 15
                new_char = chr(((ord(char) - ord('!') + shift_amount) % 15) + ord('!'))
                result.append(new_char)
            else:
                result.append(char)
    return ''.join(result)
