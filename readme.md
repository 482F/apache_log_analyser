### 概要
apache のログファイルを読み込んで、`時間帯ごとのアクセス件数` もしくは `リモートホストごとのアクセス件数` を csv 形式で表示する

### 使用方法
./apache_log_analyser.py [OPTION] [target_file_path]

target_file_path
    ログファイルのパスを指定する
    指定がなかった場合は "/var/log/httpd/access_log" が指定されたものとして扱われる

OPTION:
    -s YYYYMMDD     YYYYMMDD 以降のログのみを対象に計算して表示する
                    -e のみ指定した場合は 00010101 が指定されたものとして扱われる
    -e YYYYMMDD     YYYYMMDD 以前のログのみを対象に計算して表示する
                    -s のみ指定した場合は現在の年月日が指定されたものとして扱われる
    -f file_list    file_list に書かれているパスを target_file_path として扱う
                    file_list 内のパスは改行区切りで書く必要がある
    -m mode         時間帯ごとかリモートホストごとかを選択する
                    mode には host か hour かを指定する必要がある
                    デフォルト値は host
