#!/usr/bin/env python3

import re
import time

# ファイルの中身を str 型で返す
def load_file(filepath):
    with open(filepath, "r") as f:
        text = f.read()
    return text

# 複数ファイルの中身を結合して str で返す
def load_files(*files):
    text = ""
    for file in files:
        text += load_file(file)
    return text

# access_log 内にあるアクセス時刻を表す文字列を struct_time 型で返す
def parse_time(time_str):
    t = time.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z")
    return t

# YYYYMMDD 形式の文字列を struct_time 型で返す
def YYYYMMDD_to_struct_time(string):
    t = time.strptime(string, "%Y%m%d")
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

# key にメソッドを指定し、そのメソッドの返り値でログをグルーピングして個数を返す
def count_by_key(log_list, key):
    count = {}
    for log in log_list:
        key_value = key(log)
        count[key_value] = count.get(key_value, 0) + 1
    return count

# sdate から edate までの期間のログのみ抽出したものを返す
def select_only_specified_date(log_list, sdate, edate):
    selected_log_list = [log for log in log_list if sdate <= log["time"] <= edate]
    return selected_log_list
    

# log_list を引数に取り、時間 (hour) ごとのアクセス回数を辞書で返す
def access_count_each_hour(log_list):
    access_count = count_by_key(log_list, lambda k: k["time"].tm_hour)
    return access_count

# log_list を引数に取り、ホストごとのアクセス回数を辞書で返す
def access_count_each_host(log_list):
    access_count = count_by_key(log_list, lambda k: k["remote_host_name"])
    return access_count
