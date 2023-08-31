import os
from sys import exit
import base64 as b64
from uuid import uuid4

print(
    """
    \tGDEXE [Paths Ripper] - Программа для изменении путей к серверам для игры Geometry Dash.
    \tСоздан Masaddox; Версия v01; Дата выхода версии 05.08.2023\n
    """
)

path_to_gd_exe = input("Перетащите EXE файл в это окно (или напишите путь к файлу): ")
path_to_gd_exe = path_to_gd_exe.replace("\"", "").replace("\'", "")

print("\n[Открытие файла...]")

gd = open(path_to_gd_exe, "rb")
gd_text = gd.read()
gd.close()

print("[Определение начальных путей...]\n")

index_p = gd_text.find(b"/accounts/loginGJAccount.php")

if index_p < 0:
    input("[Ошибка!] Начальные пути не определились!")
    exit()

initial_paths = gd_text[index_p - 33: index_p]

print(f"Начальные пути определились как: {initial_paths.decode('utf-8')}")
new_path = ""

while 1:
    new_path = input("Введите новый путь (ровно 33 символа): ")

    if len(new_path) != 33:
        print(f"\n[Ошибка!] Введённый вами путь состоит из {len(new_path)} символа(-ов)!\n")
    else:
        new_path = new_path.encode()
        break

print("\n[Изменение путей...]")

gd_text = gd_text.replace(initial_paths, new_path)
gd_text = gd_text.replace(b64.b64encode(initial_paths), b64.b64encode(new_path))

new_path_to_exe = path_to_gd_exe.split(os.path.sep)
new_path_to_exe[-1] = f"{str(uuid4())}.exe"

with open(f"{os.path.sep}".join(new_path_to_exe), "wb") as file:
    file.write(gd_text)

print("[Готово!]\n")
input("Нажмите ENTER для выхода: ")
