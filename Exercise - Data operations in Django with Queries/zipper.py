import zipfile
import os
from time import strftime
from pathlib import Path

files_to_zip = [
    "main_app",
    "orm_skeleton",
    'caller.py',
    'manage.py',
    'requirements.txt'
]

downloads_path = Path.home() / 'Desktop' / 'Softuni_zips'

dt = strftime('%d-%m-%Y %H-%M-%S')
zipfile_name = f"{dt}.zip"
zip_path = downloads_path / zipfile_name

def zip_items(zip_name, items):

    base_path = os.getcwd()

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:

        for item in items:
            item_path = os.path.join(base_path, item)

            if os.path.isdir(item_path):

                for root, dirs, files in os.walk(item_path):

                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, base_path)
                        zipf.write(full_path, arcname)

            elif os.path.isfile(item_path):
                zipf.write(item_path, item)


if __name__ == "__main__":
    zip_items(zip_path, files_to_zip)
    print("Zip file created: " + zipfile_name)


