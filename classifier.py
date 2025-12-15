import os
import shutil
from stem_map import STEM_PACKAGES
from validator import validate_audio

AUDIO_EXTS = {".wav", ".mp3", ".aif", ".aiff", ".flac"}


def is_audio(filename):
    return os.path.splitext(filename)[1].lower() in AUDIO_EXTS


def matches(filename, keywords):
    name = filename.lower()
    return all(k in name for k in keywords)


def classify_package(upload_dir, output_dir, package_name):
    files = [f for f in os.listdir(upload_dir) if is_audio(f)]
    matched = []
    missing = []
    validations = {}

    stems = STEM_PACKAGES[package_name]
    package_out = os.path.join(output_dir, package_name)
    os.makedirs(package_out, exist_ok=True)

    for stem_id, keywords, rules in stems:
        found = None
        for f in files:
            if matches(f, keywords):
                found = f
                break

        if found:
            src = os.path.join(upload_dir, found)
            dst = os.path.join(package_out, found)
            shutil.copy2(src, dst)

            issues = validate_audio(
                dst,
                expect_stereo=rules.get("stereo")
            )

            matched.append(stem_id)
            validations[stem_id] = issues
        else:
            missing.append(stem_id)

    completed = len(missing) == 0
    return matched, missing, completed, validations

