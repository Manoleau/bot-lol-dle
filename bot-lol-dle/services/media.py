import os
from models.media import Media
import importlib.util

base_path = 'media'
commands_folder_path = 'commands'
def creer_dossier(path_dossier:str):
    if not os.path.exists(path_dossier):
        os.mkdir(path_dossier)
creer_dossier(base_path)

def creer_image(nom_fichier:str) -> Media:
    creer_dossier(f"{base_path}/images")
    if os.path.exists(f'{base_path}/images/{nom_fichier}.jpg'):
        return Media(f'{nom_fichier}.jpg', f'{base_path}/images/{nom_fichier}.jpg')

    ## Logique d'ajout
    return Media(f'{nom_fichier}.jpg', f'{base_path}/images/{nom_fichier}.jpg')

def execute_get_commands():
    """
    Parcourt tous les fichiers Python dans un dossier et exécute la fonction `get` de chaque fichier, si elle existe.
    """
    if not os.path.isdir(commands_folder_path):
        print(f"Le chemin spécifié '{commands_folder_path}' n'est pas un dossier valide.")
        return

    for filename in os.listdir(commands_folder_path):
        if filename.endswith(".py"):
            file_path = os.path.join(commands_folder_path, filename)
            module_name = os.path.splitext(filename)[0]

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                if hasattr(module, "get") and callable(module.get):
                    print(f"Exécution de la fonction `get` dans {filename}...")
                    module.get()
            except Exception as e:
                print(f"Erreur lors de l'exécution de {filename}: {e}")



