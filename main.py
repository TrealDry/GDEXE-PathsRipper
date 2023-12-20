import os
import json
from sys import exit
import base64 as b64
from uuid import uuid4


localization_folder = os.getcwd() + os.sep + "localization"
settings_sample = {"selected_language": ""}


def clear_screen(): os.system('cls||clear')


def create_settings():
    with open(f"{localization_folder}{os.sep}settings.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(settings_sample))


def load_lang(name):
    name = name + ".json"
    
    try:
        with open(f"{localization_folder}{os.sep}{name}", "r", encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[Error!] localization file \"{name}\" does not exist.")
        
        while 1:
            choice = input("Reset localization settings? (yes = 1, no = 0): ")
            
            if int(choice) == 1:
                create_settings()
            
            exit()


def localization_selection():
    try:
        with open(f"{localization_folder}{os.sep}settings.json", "r", encoding='utf-8') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = settings_sample
        
    if settings["selected_language"] != "":
        return load_lang(settings["selected_language"])
    
    localizations = os.listdir(localization_folder)
    
    if not localizations:
        input("[Error!] There are no files with localizations in the \"localization\" folder ")
        exit()
    
    localizations = [i[:-5] for i in localizations if i[-5:] == ".json" and i != "settings.json"]
    
    print("Выберите язык | Select a language.\n")
    
    for i in range(len(localizations)):
        print(f"{i + 1}. {localizations[i]}")
    
    while 1:
        try:
            lang_selection = int(input(">>> "))
            selected_lang = localizations[lang_selection - 1]
            
            with open(f"{localization_folder}{os.sep}settings.json", "w", encoding='utf-8') as file:
                settings["selected_language"] = selected_lang
                file.write(json.dumps(settings))
            
            return load_lang(selected_lang)
        except:
            continue


def main():
    lang = localization_selection()
    clear_screen()
    
    print(lang["logo"].format(lang["translator"]))

    path_to_gd_exe = input(lang["messages"]["get_path_to_gd_exe"])
    path_to_gd_exe = path_to_gd_exe.replace("\"", "").replace("\'", "")

    print(f"\n{lang['logs']['open_gd_exe']}")

    gd = open(path_to_gd_exe, "rb")
    gd_text = gd.read()
    gd.close()

    print(f"{lang['logs']['pathway_detection_in_gd_exe']}\n")

    index_p = gd_text.find(b"/accounts/loginGJAccount.php")

    if index_p < 0:
        input(lang["errors"]["paths_have_not_been_found"])
        exit()

    initial_paths = gd_text[index_p - 33: index_p]

    if initial_paths[:5].decode('utf-8') == "ttps:":  # 2.2 https
        initial_paths = gd_text[index_p - 34: index_p]

    print(lang["messages"]["paths_were_found"].format(initial_paths.decode('utf-8')))
    new_path = ""

    while 1:
        new_path = input(lang["messages"]["enter_new_paths"].format(len(initial_paths)))

        if len(new_path) != len(initial_paths):
            print(f"\n{lang['errors']['incorrect_length_of_new_paths'].format(len(new_path))}\n")
        else:
            new_path = new_path.encode()
            break

    print(f"\n{lang['logs']['change_of_paths']}")

    gd_text = gd_text.replace(initial_paths, new_path)
    gd_text = gd_text.replace(b64.b64encode(initial_paths), b64.b64encode(new_path))

    new_path_to_exe = path_to_gd_exe.split(os.path.sep)
    new_path_to_exe[-1] = f"{str(uuid4())}.exe"

    with open(f"{os.path.sep}".join(new_path_to_exe), "wb") as file:
        file.write(gd_text)

    print(f"{lang['logs']['done']}\n")
    input(lang["messages"]["press_enter_to_exit"])


if __name__ == "__main__":
    main()
