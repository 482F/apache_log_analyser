#!/usr/bin/env python3

# ファイルの中身を str 型で返す
def load_file(filepath):
    with open(filepath, "r") as f:
        text = f.read()
    return text
