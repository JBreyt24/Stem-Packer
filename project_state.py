import json
import os

STATE_FILE = os.path.join("processed", "project_state.json")


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"packages": {}}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    os.makedirs("processed", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def is_package_completed(state, package):
    return state.get("packages", {}).get(package, {}).get("completed", False)


def mark_package(state, package, completed, matched, missing):
    state.setdefault("packages", {})
    state["packages"][package] = {
        "completed": completed,
        "matched": matched,
        "missing": missing
    }
    save_state(state)

def get_package_status(state, package):
    pkg = state.get("packages", {}).get(package)

    if not pkg:
        return "not_started"

    if pkg.get("completed"):
        return "completed"

    return "incomplete"

def is_project_complete(state):
    packages = state.get("packages", {})
    if not packages:
        return False
    return all(pkg.get("completed") for pkg in packages.values())
