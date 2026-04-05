# Báo Cáo Hệ Thống Ứng Dụng NT101 Crypto App

## 1. Giới thiệu ứng dụng (mục đích, phạm vi)

Ứng dụng NT101 Crypto App là phần mềm desktop được xây dựng để minh họa nguyên lý hoạt động của hai thuật toán mật mã cơ bản là Playfair và RSA. Mục đích chính là hỗ trợ học tập, giúp người dùng quan sát được quá trình mã hóa và giải mã thông qua thao tác trực tiếp trên giao diện.

Phạm vi của ứng dụng tập trung vào:
- Thực hành nhập dữ liệu, xử lý dữ liệu và xem kết quả.
- Minh họa mối liên hệ giữa dữ liệu đầu vào, khóa và kết quả đầu ra.
- Hỗ trợ đọc/ghi file và xuất báo cáo để phục vụ ghi chép, thí nghiệm và viết tài liệu môn học.

Ứng dụng không hướng tới mục tiêu bảo mật triển khai thực tế trong hệ thống sản phẩm.

## 2. Mô tả tổng quan (kiến trúc, thành phần chính)

Ứng dụng được tổ chức theo kiến trúc đơn giản gồm 3 lớp thành phần chính:

- Lớp khởi chạy:
  - `main.py` có nhiệm vụ tạo đối tượng giao diện và chạy vòng lặp ứng dụng.
- Lớp giao diện và điều phối:
  - `ui.py` quản lý toàn bộ màn hình, widget, sự kiện nút bấm, kiểm tra dữ liệu đầu vào, hiển thị thông báo và thao tác file.
- Lớp thuật toán:
  - `algorithms/playfair.py` xử lý tạo ma trận khóa và phép biến đổi Playfair.
  - `algorithms/rsa.py` xử lý kiểm tra số nguyên tố, sinh khóa, mã hóa và giải mã RSA.

Dữ liệu đi theo hướng: người dùng nhập trên giao diện -> giao diện gọi hàm thuật toán -> kết quả trả về giao diện -> hiển thị/ghi file/xuất báo cáo.

## 3. Chi tiết giao diện (màn hình, widget, chức năng)

Giao diện gồm 3 tab chính:

### 3.1. Tab Playfair

Widget chính:
- Ô nhập `Plaintext / Ciphertext`.
- Ô nhập `Khóa`.
- Các nút chức năng: `Mã hóa`, `Giải mã`, `Ngẫu nhiên`, `Xóa`.
- Ô `Kết quả` ở trạng thái không cho sửa trực tiếp.
- Nhãn hiển thị kết quả bên dưới ô kết quả để dễ đọc.
- Bảng khóa (Keysquare) 5x5 hiển thị ở dạng lưới trung tâm.
- Nút `?` hướng dẫn cho từng trường.
- Nút thao tác file dưới từng trường liên quan:
  - Đọc/Lưu cho Plaintext-Ciphertext.
  - Lưu kết quả.
  - Xuất báo cáo Playfair.

### 3.2. Tab RSA

Widget chính:
- Chế độ thao tác: `Mã hóa` hoặc `Giải mã` (radio button).
- Các ô nhập tham số: `p`, `q`, `e`, `Plaintext`, `Ciphertext`, `Khóa bí mật d`, `Khóa bí mật n`.
- Nút chức năng: `Mã hóa/Giải mã` (đổi theo mode), `Ngẫu nhiên`, `Xóa`.
- Ô `Kết quả` bị vô hiệu hóa chỉnh sửa trực tiếp.
- Nhãn hiển thị kết quả bên dưới.
- Nút `?` hướng dẫn cho từng trường.
- Nút đọc/ghi file tương ứng dưới từng trường Plaintext, Ciphertext, Result.
- Nút `Xuất báo cáo` để xuất kết quả RSA chi tiết.

### 3.3. Tab Giới thiệu

Hiển thị thông tin môn học, giảng viên phụ trách, niên khóa, thành viên nhóm và mô tả ngắn gọn ứng dụng.

## 4. Luồng hoạt động (cách người dùng tương tác, phản hồi của ứng dụng)

Luồng tổng quát:
1. Người dùng mở ứng dụng.
2. Chọn tab Playfair hoặc RSA.
3. Nhập dữ liệu thủ công hoặc nạp từ file.
4. Nhấn nút xử lý (`Mã hóa`/`Giải mã`).
5. Ứng dụng kiểm tra dữ liệu đầu vào.
6. Nếu hợp lệ, gọi module thuật toán để tính toán.
7. Hiển thị kết quả trong ô Result và nhãn kết quả.
8. Người dùng có thể sao chép, lưu từng trường, hoặc xuất báo cáo đầy đủ.

Phản hồi của ứng dụng:
- Thông báo lỗi khi dữ liệu không hợp lệ.
- Thông báo thành công khi đọc file, ghi file, hoặc xuất báo cáo.
- Tự động khóa/mở một số ô trong RSA tùy theo mode nhằm giảm nhập sai.

## 5. Cấu trúc code (module, class, function chính)

### 5.1. Module `main.py`
- `if __name__ == "__main__":` khởi tạo `CryptoApp` và chạy `run()`.

### 5.2. Module `ui.py`
- Class chính: `CryptoApp`.
- Nhóm hàm tiện ích giao diện:
  - `add_input_row`, `add_field_action_row`, `set_entry_state`, `set_entry_value`, `set_result_display`.
- Nhóm hàm thao tác file:
  - `read_text_file_to_entry`, `save_entry_to_text_file`, `save_text_report`.
- Nhóm hàm Playfair:
  - `build_playfair`, `handle_pf_encrypt`, `handle_pf_decrypt`, `render_pf_keysquare`, `export_playfair_result`, ...
- Nhóm hàm RSA:
  - `build_rsa`, `update_rsa_mode`, `handle_rsa_encrypt`, `handle_rsa_decrypt`, `export_rsa_result`, ...
- Nhóm hàm tab giới thiệu:
  - `build_about_us`.

### 5.3. Module `algorithms/playfair.py`
- `prepare_text`: chuẩn hóa chuỗi đầu vào theo quy tắc Playfair.
- `generate_matrix`: tạo ma trận khóa 5x5.
- `find_position`: tìm tọa độ ký tự trong ma trận.
- `encrypt`, `decrypt`: xử lý mã hóa và giải mã.

### 5.4. Module `algorithms/rsa.py`
- `is_prime`: kiểm tra số nguyên tố.
- `extended_gcd`, `mod_inverse`: tính nghịch đảo modular.
- `generate_keys`: sinh public/private key từ p, q, e.
- `encrypt`, `decrypt`: mã hóa/giải mã theo khóa.

## 6. Kịch bản triển khai

### Kịch bản chạy cục bộ
1. Cài Python 3.9+.
2. Mở terminal tại thư mục dự án.
3. Chạy lệnh:

```bash
python3 main.py
```

### Kịch bản kiểm tra nhanh mã nguồn

```bash
python3 -m py_compile main.py ui.py algorithms/playfair.py algorithms/rsa.py
```

### Kịch bản sử dụng báo cáo
- Sau khi thao tác mã hóa/giải mã, chọn `Xuất báo cáo` để tạo file `.txt` phục vụ lưu trữ kết quả thí nghiệm.

## 7. Đánh giá & Nhận xét (điểm mạnh, hạn chế, đề xuất cải tiến)

### Điểm mạnh
- Giao diện trực quan, thao tác rõ ràng cho người mới.
- Có mô tả thuật toán ngay trên tab chức năng.
- Có hỗ trợ đọc/ghi file và xuất báo cáo chi tiết.
- Có cơ chế kiểm tra đầu vào giúp giảm lỗi thao tác.
- Cấu trúc module tách riêng phần thuật toán và giao diện, dễ đọc và dễ bảo trì.

### Hạn chế
- Chưa có bộ kiểm thử tự động.
- RSA là phiên bản minh họa học tập, chưa có padding chuẩn cho môi trường thực tế.
- Giao diện hiện thiên về chức năng, chưa tối ưu sâu về bố cục responsive hoặc theme.

### Đề xuất cải tiến
- Bổ sung test tự động cho các ca kiểm thử thuật toán và giao diện lõi.
- Tách lớp xử lý nghiệp vụ trung gian để giảm độ lớn của `ui.py`.
- Bổ sung tùy chọn xuất báo cáo sang JSON/CSV.
- Tối ưu thông điệp lỗi theo ngữ cảnh chi tiết hơn.

## 8. Kết luận (giá trị ứng dụng, hướng phát triển)

NT101 Crypto App có giá trị cao trong bối cảnh học tập vì giúp chuyển kiến thức lý thuyết mật mã thành thao tác trực quan, dễ quan sát và dễ kiểm chứng. Ứng dụng phù hợp cho thực hành trên lớp, làm bài tập lớn và chuẩn bị báo cáo môn học.

Trong giai đoạn tiếp theo, hệ thống có thể phát triển theo hai hướng song song:
- Nâng chất lượng kỹ thuật phần mềm (kiểm thử, tái cấu trúc mã, tài liệu hóa).
- Mở rộng chức năng học thuật (thêm thuật toán mới, thêm định dạng xuất dữ liệu, thêm mô phỏng bước xử lý chi tiết).
