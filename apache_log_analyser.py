#!/usr/bin/env python3

import re
import time
import sys
import glob
import os

# 多次元配列を一次元に直して返す
def resolve_nest(*target):
    resolved_target = []
    for elem in target:
        resolved_target += resolve_nest(*elem) if type(elem) == list else [elem]
    return resolved_target

# ファイルの中身を str 型で返す
def load_file(filepath):
    with open(filepath, "r") as f:
        line = f.readline()
        while line:
            line = line.strip("\n")
            yield line
            line = f.readline()

# 複数ファイルの中身を結合して str で返す
def load_files(*files):
    text = ""
    for file_path in files:
        for line in load_file(file_path):
            yield line

# パスのワイルドカードとホームディレクトリのチルダを展開する
def expand_path(path):
    e_path = glob.glob(os.path.expanduser(path))
    return e_path

# access_log 内にあるアクセス時刻を表す文字列を struct_time 型で返す
def parse_time(time_str):
    t = time.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z")
    return t

# YYYYMMDD 形式の文字列を struct_time 型で返す
def YYYYMMDD_to_struct_time(string):
    t = time.strptime(string, "%Y%m%d")
    return t

# logs を辞書に変換して返す
def logs_to_dict(logs):
    pattern = re.compile(r"(?P<remote_host_name>\S*) (?P<client_id>\S*) (?P<user_name>\S*) \[(?P<time>[^\]]*)\] \"(?P<first_row>.*?)\" (?P<last_response_status>\S*) (?P<response_bytes>\S*) \"(?P<header_referer>.*?)\" \"(?P<header_user_agent>.*?)\"")
    for log in logs:
        if log == "":
            continue
        match = pattern.match(log)
        groupdict = match.groupdict()
        groupdict["time"] = parse_time(groupdict["time"])
        yield groupdict

# key にメソッドを指定し、そのメソッドの返り値でログをグルーピングして個数を返す
def count_by_key(logs, key):
    count = {}
    for log in logs:
        key_value = key(log)
        count[key_value] = count.get(key_value, 0) + 1
    return count

# sdate から edate までの期間のログのみ抽出したものを返す
def select_only_specified_date(log_list, sdate, edate):
    selected_log_list = [log for log in log_list if sdate <= log["time"] <= edate]
    return selected_log_list
    

# logs を引数に取り、時間 (hour) ごとのアクセス回数を辞書で返す
def access_count_each_hour(logs):
    access_count = count_by_key(logs, lambda k: k["time"].tm_hour)
    return access_count

# logs を引数に取り、ホストごとのアクセス回数を辞書で返す
def access_count_each_host(logs):
    access_count = count_by_key(logs, lambda k: k["remote_host_name"])
    return access_count


paths = []
next_skip = False
start_time = None
end_time = None
mode = "host"

args = sys.argv[1:]
if len(args) == 0:
    paths.append("/var/log/httpd/access_log")

for index, arg in enumerate(args):
    if next_skip:
        next_skip = False
        continue
    elif arg == "-s":
        next_skip = True
        start_time = YYYYMMDD_to_struct_time(args[index + 1])
        if end_time == None:
            end_time = time.localtime()
    elif arg == "-e":
        next_skip = True
        end_time = YYYYMMDD_to_struct_time(args[index + 1])
        if start_time == None:
            start_time = YYYYMMDD_to_struct_time("00010101")
    elif arg == "-f":
        next_skip = True
        paths += resolve_nest([expand_path(line) for line in load_file(args[index + 1]).split("\n") if line != ""])
    elif arg == "-m":
        next_skip = True
        mode = args[index + 1]
        if mode not in ["host", "hour"]:
            raise ValueError("invalid mode: " + mode)
    else:
        paths += expand_path(arg)

access_count_method = {"host": access_count_each_host, "hour": access_count_each_hour}[mode]
sort_method = {"host": lambda k: k[1], "hour": lambda k: k[0]}[mode]

log_list = log_text_to_list(load_files(*paths))

if start_time != None:
    log_list = select_only_specified_date(log_list, start_time, end_time)

access_count = access_count_method(log_list)

output = mode + ",count"

for key, value in sorted(access_count.items(), key=sort_method, reverse=True):
    output += "\n" + str(key) + "," + str(value)

print(output)
