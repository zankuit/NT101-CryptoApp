# NT101 Crypto App

Ứng dụng desktop sử dụng Tkinter để minh họa trực quan hai thuật toán mật mã cơ bản:
- Playfair
- RSA (mục đích học tập)

Môn học: `An toàn mạng máy tính - NT101.Q22`

Giảng viên phụ trách: `Tô Nguyễn Nhật Quang`

Niên khóa: `Học kỳ 2, 2025-2026`

Thành viên nhóm:
1. `Mai Nguyễn Bình Tân`
2. `Lê Huy Hiếu`
3. `Phạm Thành Danh`

## Mục tiêu

- Giúp người học quan sát luồng mã hóa/giải mã ngay trên giao diện.
- Cung cấp thao tác nhanh để nhập dữ liệu, sinh dữ liệu mẫu, đọc/ghi file và xuất báo cáo kết quả.

## Cấu trúc dự án

- `main.py`: điểm vào ứng dụng.
- `ui.py`: toàn bộ giao diện và luồng xử lý tương tác.
- `algorithms/playfair.py`: thuật toán Playfair.
- `algorithms/rsa.py`: thuật toán RSA.

### Tổ chức file

```text
NT101-CryptoApp/
├── main.py
├── ui.py
└── algorithms/
	├── playfair.py
	└── rsa.py
```

Mô tả nhanh:
- `main.py`: chạy ứng dụng và khởi tạo giao diện.
- `ui.py`: quản lý toàn bộ tab, widget, sự kiện, đọc/ghi file và xuất báo cáo.
- `algorithms/playfair.py`: xử lý chuẩn hóa dữ liệu, tạo keysquare và mã hóa/giải mã Playfair.
- `algorithms/rsa.py`: xử lý sinh khóa, mã hóa/giải mã RSA và kiểm tra dữ liệu đầu vào.
- `README.md`: tài liệu hướng dẫn sử dụng.
- `BAO_CAO_UNG_DUNG.md`: tài liệu hệ thống phục vụ viết báo cáo môn học.
- `.gitignore`: quy tắc bỏ qua file không cần theo dõi bằng Git.

## Yêu cầu hệ thống

- Python 3.9 trở lên.
- Tkinter (thường có sẵn theo Python cài từ hệ điều hành).

Đối với người dùng **Ubuntu**, do Tkinter không có sẵn nên cần chạy dòng lệnh sau:
```bash
sudo apt install python3-tk
```


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


## Ghi chú kỹ thuật

- Ứng dụng đã loại bỏ `eval` khi xử lý ciphertext và dùng parse an toàn (`ast.literal_eval`).
- RSA dùng kiểm tra tính hợp lệ khóa và tính nghịch đảo modular bằng Extended Euclidean Algorithm.

## Giới hạn hiện tại

- Ứng dụng phục vụ học tập, không thay thế thư viện mật mã cho môi trường thực tế.
- RSA đang mã hóa theo từng ký tự, chưa áp dụng padding chuẩn như OAEP/PSS.

 
