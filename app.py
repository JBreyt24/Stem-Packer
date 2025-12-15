from flask import Flask, render_template, request, send_file
import os
from classifier import classify_package
from stem_map import STEM_PACKAGES
from project_state import (
    load_state,
    is_package_completed,
    mark_package,
    get_package_status,
    is_project_complete
)
from exporter import create_export_zip

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "processed"

app = Flask(__name__)


def clear_uploads():
    if os.path.exists(UPLOAD_DIR):
        for f in os.listdir(UPLOAD_DIR):
            os.remove(os.path.join(UPLOAD_DIR, f))


@app.route("/", methods=["GET"])
def index():
    state = load_state()
    package_status = {
        p: get_package_status(state, p)
        for p in STEM_PACKAGES.keys()
    }

    project_complete = is_project_complete(state)

    return render_template(
        "index.html",
        packages=STEM_PACKAGES.keys(),
        state=state,
        package_status=package_status,
        project_complete=project_complete,
        stem_packages=STEM_PACKAGES
    )


@app.route("/upload", methods=["POST"])
def upload():
    package = request.form["package"]
    state = load_state()

    if is_package_completed(state, package):
        return render_template(
            "results.html",
            package=package,
            matched=[],
            missing=[],
            error="This package has already been completed."
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clear_uploads()

    for f in request.files.getlist("files"):
        if f.filename:
            f.save(os.path.join(UPLOAD_DIR, f.filename))

    matched, missing, completed, validations = classify_package(
        UPLOAD_DIR,
        OUTPUT_DIR,
        package
    )

    mark_package(
        state,
        package,
        completed=completed,
        matched=matched,
        missing=missing
    )

    return render_template(
        "results.html",
        package=package,
        matched=matched,
        missing=missing,
        completed=completed,
        validations=validations
    )


@app.route("/download", methods=["GET"])
def download():
    state = load_state()

    if not is_project_complete(state):
        return "Project is not complete. Cannot export.", 403

    zip_path = create_export_zip(OUTPUT_DIR)
    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
