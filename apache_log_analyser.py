#!/usr/bin/env python3

def load_file(filepath):
    with open(filepath, "r") as f:
        text = f.read()
    return text
