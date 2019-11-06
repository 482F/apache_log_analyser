#!/usr/bin/env python3

import re
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

# access_log のテキストを辞書型を要素に持つリストにして返す
def log_text_to_list(text):
    logs = [log for log in text.split("\n") if log != ""]
    
    pattern = re.compile(r"(?P<remote_host_name>\S*) (?P<client_id>\S*) (?P<user_name>\S*) \[(?P<time>[^\]]*)\] \"(?P<first_row>.*?)\" (?P<last_response_status>\S*) (?P<response_bytes>\S*) \"(?P<header_referer>.*?)\" \"(?P<header_user_agent>.*?)\"")

    log_groupdict = [None for k in logs]

    for index, log in enumerate(logs):
        match = pattern.match(log)
        groupdict = match.groupdict()
        groupdict["time"] = parse_time(groupdict["time"])
        log_groupdict[index] = groupdict
    return log_groupdict

# log_list を引数に取り、ホストごとのアクセス回数を辞書で返す
def access_count_each_host(log_list):
    access_count = {}
    for log in log_list:
        remote_host_name = log["remote_host_name"]
        access_count[remote_host_name] = access_count.get(remote_host_name, 0) + 1
    return access_count
