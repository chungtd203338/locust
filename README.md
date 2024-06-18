# Trịnh Đức Chung - K65 - HUST <3
# Trace data with Locust #
# Cách sử dụng #
Clone project về máy
```console
git clone https://github.com/chungtd203338/locust.git
```
Cách sử dụng <br>
Config thông số trong file locust.conf
```
host = http://100.72.82.40:31304/ # ip workload app
users = 1
spawn-rate = 1
# headless = true
# run-time = 30sec
```
Thực hiện test tải
```console
locust -f loading.py
```
Truy cập http://localhost:8089 thể ra giao diện quản lý và theo dõi locust <br>
Đọc thêm tại: https://locust.io/
