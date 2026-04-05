NT101 Crypto App

Ứng dụng desktop sử dụng Tkinter để minh họa trực quan hai thuật toán mật mã cơ bản:
- Playfair
- RSA (mục đích học tập)

## Mục tiêu

- Giúp người học quan sát luồng mã hóa/giải mã ngay trên giao diện.
- Cung cấp thao tác nhanh để nhập dữ liệu, sinh dữ liệu mẫu, đọc/ghi file và xuất báo cáo kết quả.

## Cấu trúc dự án

- `main.py`: điểm vào ứng dụng.
- `ui.py`: toàn bộ giao diện và luồng xử lý tương tác.
- `algorithms/playfair.py`: thuật toán Playfair.
- `algorithms/rsa.py`: thuật toán RSA.

## Yêu cầu hệ thống

- Python 3.9 trở lên.
- Tkinter (thường có sẵn theo Python cài từ hệ điều hành).

## Cách chạy

```bash
python3 main.py
```

## Tính năng chính

### Playfair

- Mã hóa và giải mã chuỗi chữ cái.
- Hiển thị bảng khóa (Keysquare) 5x5.
- Có nút hướng dẫn `?` cho từng trường nhập.
- Có nút sinh dữ liệu ngẫu nhiên, xóa nhanh, sao chép kết quả.
- Hỗ trợ đọc từ file, lưu ra file và xuất báo cáo kết quả.

### RSA

- Hai chế độ thao tác: mã hóa và giải mã.
- Kiểm tra dữ liệu đầu vào cho `p, q, e`, ciphertext và private key.
- Hỗ trợ đọc/ghi file riêng cho Plaintext và Ciphertext.
- Hỗ trợ xuất báo cáo kết quả với thông tin khóa và bản mã/bản rõ.
- Có nút hướng dẫn `?`, sinh dữ liệu ngẫu nhiên, xóa nhanh và sao chép.

### Giới thiệu

- Hiển thị thông tin môn học, giảng viên, niên khóa, thành viên nhóm.
- Mô tả ngắn gọn mục tiêu và phạm vi ứng dụng.

## Ghi chú kỹ thuật

- Ứng dụng đã loại bỏ `eval` khi xử lý ciphertext và dùng parse an toàn (`ast.literal_eval`).
- RSA dùng kiểm tra tính hợp lệ khóa và tính nghịch đảo modular bằng Extended Euclidean Algorithm.

## Giới hạn hiện tại

- Ứng dụng phục vụ học tập, không thay thế thư viện mật mã cho môi trường thực tế.
- RSA đang mã hóa theo từng ký tự, chưa áp dụng padding chuẩn như OAEP/PSS.

## Tác giả

Nhóm thực hiện môn An toàn mạng máy tính - NT101.Q22.
 