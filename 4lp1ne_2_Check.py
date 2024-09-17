import os
import hashlib
import json
from collections import defaultdict
from tqdm import tqdm  # Pour la barre de progression


# Fonction qui te calcule un hash (genre une signature unique) pour chaque fichier
def hash_file(file_path, block_size=65536):
    hasher = hashlib.md5()  # On utilise l'algorithme MD5 pour générer un hash
    with open(file_path, 'rb') as file:
        buf = file.read(block_size)
        while buf:
            hasher.update(buf)
            buf = file.read(block_size)
    return hasher.hexdigest()  # On renvoie le hash en mode string


# Fonction pour sauvegarder la progression dans un fichier JSON, au cas où ça plante
def save_progress(progress_file, data):
    with open(progress_file, 'w') as f:
        json.dump(data, f)


# Fonction pour charger une sauvegarde si elle existe (reprise là où on s'était arrêté)
def load_progress(progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return defaultdict(list)  # Si y a pas de sauvegarde, on démarre à zéro


# Fonction qui va scanner les fichiers et enregistrer les doublons avec une barre de progression
def find_duplicates(directory, progress_file='progress.json'):
    hashes = load_progress(progress_file)  # On check si y'a une sauvegarde et on la charge
    total_files = sum([len(files) for r, d, files in os.walk(directory)])  # Compte le nombre total de fichiers

    # Progression avec tqdm (la barre qui défile)
    with tqdm(total=total_files, desc="Scan des fichiers", unit="fichier") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # On évite de recalculer les hash déjà trouvés dans la sauvegarde
                if any(file_path in paths for paths in hashes.values()):
                    continue  # On passe au fichier suivant, celui-ci est déjà fait

                try:
                    file_hash = hash_file(file_path)  # Génération du hash
                    hashes[file_hash].append(file_path)  # On ajoute le fichier à la liste des doublons potentiels
                    save_progress(progress_file, hashes)  # On sauvegarde la progression à chaque fichier
                except Exception as e:
                    print(f"Impossible de lire {file_path}: {e}")  # Si ça foire, on prévient

                pbar.update(1)  # On met à jour la barre de progression

    # On filtre pour ne garder que les hash qui ont plusieurs fichiers associés (les doublons quoi)
    duplicates = {hash: paths for hash, paths in hashes.items() if len(paths) > 1}
    return duplicates


# Fonction pour dégager les doublons tout en conservant un fichier
def delete_duplicates(duplicates):
    for file_hash, file_list in duplicates.items():
        print(f"\nOn garde ce fichier: {file_list[0]}")
        for file_path in file_list[1:]:
            try:
                os.remove(file_path)  # Là on supprime les doublons
                print(f"Supprimé: {file_path}")
            except Exception as e:
                print(f"Impossible de supprimer {file_path}: {e}")


if __name__ == "__main__":
    # On récupère le chemin du disque externe ou du répertoire à scanner
    external_drive_path = input("Entrez le chemin du disque externe à scanner: ")

    # Étape 1: On cherche les doublons
    print("Recherche des doublons...")
    duplicates = find_duplicates(external_drive_path)

    # Si on trouve des doublons
    if duplicates:
        print("\nFichiers en double trouvés:")
        for file_hash, file_list in duplicates.items():
            print(f"Doublons pour le hash {file_hash}:")
            for file in file_list:
                print(f" - {file}")

        # Étape 2: Demande si on veut supprimer les doublons ou pas
        confirm = input("\nVoulez-vous supprimer les doublons (sauf un) ? (o/n): ").lower()
        if confirm == 'o':
            print("Suppression des fichiers en cours...")
            delete_duplicates(duplicates)
        else:
            print("Aucune suppression effectuée.")
    else:
        print("Aucun fichier en double trouvé.")

