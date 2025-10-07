# Ứng dụng tạo ảnh từ prompt

Ứng dụng web đơn giản giúp bạn nhập một đoạn mô tả (prompt) và nhận lại một hình ảnh minh hoạ chứa nội dung đó. Hình ảnh được tạo bằng Python và thư viện Pillow bằng cách kết hợp nền gradient và văn bản.

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
flask --app app run --debug
```

Sau khi chạy, mở trình duyệt và truy cập `http://127.0.0.1:5000/` để sử dụng.

## Cấu trúc dự án

- `app.py`: Mã nguồn Flask.
- `static/generated/`: Thư mục chứa các hình ảnh đã tạo.
- `requirements.txt`: Danh sách phụ thuộc Python.

## Ghi chú

- Ứng dụng tạo ảnh dựa trên prompt bằng cách hiển thị văn bản trên nền gradient, không sử dụng mô hình tạo ảnh nâng cao.
- Thư mục `static/generated/` được giữ trống trong Git; các ảnh tạo ra trong quá trình chạy sẽ được lưu tại đây.
