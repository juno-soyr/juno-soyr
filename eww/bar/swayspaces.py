#!/usr/bin/python3

import subprocess
import json


def get_workspaces():
    output = subprocess.check_output(["swaymsg", "-t", "get_workspaces"])
    return json.loads(output.decode("utf-8"))


def generate_workspace_data() -> dict:
    data = {}
    for wsp in get_workspaces():
        if wsp["output"] not in data:
            data[wsp["output"]] = []
        wsp_class = "focused" if wsp["focused"] else "inactive"
        data[wsp["output"]].append(
            {
                "name": wsp["name"],
                "focused": wsp["focused"],
                "visible": wsp["visible"],
                "class": wsp_class  # ← added class field here
            }
        )
    return data


if __name__ == "__main__":
    process = subprocess.Popen(
        ["swaymsg", "-t", "subscribe", "-m", '["workspace"]', "--raw"],
        stdout=subprocess.PIPE,
    )
    if process.stdout is None:
        print("Error: could not subscribe to sway events")
        exit(1)
    while True:
        print(json.dumps(generate_workspace_data()), flush=True)
        line = process.stdout.readline().decode("utf-8")
        if line == "":
            break

