import os
from zipfile import ZipFile

EXPORT_NAME = "stem_packer_export.zip"


def create_export_zip(processed_dir):
    zip_path = os.path.join(processed_dir, EXPORT_NAME)

    with ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(processed_dir):
            for f in files:
                if f.endswith(".json") or f == EXPORT_NAME:
                    continue

                full_path = os.path.join(root, f)
                arcname = os.path.relpath(full_path, processed_dir)
                zipf.write(full_path, arcname)

    return zip_path
