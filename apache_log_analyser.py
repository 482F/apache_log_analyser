#!/usr/bin/env python3

import time

# ファイルの中身を str 型で返す
def load_file(filepath):
    with open(filepath, "r") as f:
        text = f.read()
    return text

# access_log 内にあるアクセス時刻を表す文字列を struct_time 型で返す
def parse_time(time_str):
    t = time.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z")
    return t
