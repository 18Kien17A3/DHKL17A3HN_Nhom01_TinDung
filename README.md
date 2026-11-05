# Giám sát và phân tích hồ sơ phê duyệt tín dụng

Đề tài 3, môn Thực hành Trực quan hóa dữ liệu. Python 3.12.
Lớp DHKL17A3HN · Nhóm 01.

## Chạy trên Windows / VS Code

Mở Terminal tại thư mục chứa `app.py`, chạy lần lượt:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python analysis.py
python -m streamlit run app.py
```

Truy cập địa chỉ mà Streamlit in trên Terminal, thường là http://localhost:8501.
Trên macOS/Linux, dùng `source .venv/bin/activate` để kích hoạt môi trường.
Dashboard dùng file CSV đã kèm tại `data/loan_approval_dataset.csv`, không tải từ URL và không dùng dữ liệu mô phỏng.

## Cấu trúc

- `analysis.py`: đọc, kiểm tra, xử lý, phân nhóm, KPI và xuất kết quả.
- `app.py`: ba trang Dashboard dùng chung bộ lọc.
- `01_PhanTichTinDung.ipynb`: notebook có kết quả đã chạy, từng bước có giải thích.
- `test_project.py`: kiểm tra số liệu, dữ liệu tài sản và hành vi ứng dụng.
- `data/`: dữ liệu gốc giữ nguyên.
- `results/`: dữ liệu phân tích, bảng phân nhóm, chỉ số và nhật ký kiểm tra tự động.
- `.streamlit/config.toml`: bảng màu nhất quán.

## Cách đọc và thao tác

1. Trang Tổng quan: kiểm tra bốn KPI, phân bố CIBIL, tỷ lệ duyệt theo phân khúc.
2. Chọn bộ lọc ở bên trái. Chúng giữ trạng thái khi chuyển trang.
3. Trang Phân tích: rê chuột xem số lượng và tỷ lệ trong từng ô CIBIL/kỳ hạn.
4. Trang Tra cứu: chọn lọc nhanh, đổi ngưỡng khám phá, tìm đúng mã, sắp xếp và tải CSV.
5. Nút Đặt lại bộ lọc trả các bộ lọc chung và điều kiện tra cứu về mặc định.
6. Plotly hỗ trợ rê chuột, thu phóng và tải ảnh qua thanh công cụ trên biểu đồ.

## Quy ước dữ liệu

- Nguồn: https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset
- 4.269 hồ sơ, 13 cột gốc. CSV không có mô tả tiền tệ hoặc đơn vị kỳ hạn. Hiển thị đơn vị gốc, không gán VND/INR hoặc tháng/năm khi chưa xác minh.
- Chuẩn hóa khoảng trắng. Có 28 giá trị tài sản nhà ở bằng -100.000, chuyển riêng thành phần đó thành thiếu, giữ cột gốc và cờ `asset_issue`. Không bỏ hồ sơ.
- `total_assets` chỉ tính khi đủ 4 thành phần. Giá trị 0 trong tài sản được giữ nguyên, chưa có căn cứ đổi thành thiếu.
- Tỷ lệ duyệt = số Approved / số hồ sơ sau bộ lọc. Lọc riêng Approved sẽ cho 100%, đây là hệ quả của mẫu số.
- `loan_amount` là tiền đề nghị vay, không phải dư nợ hay giải ngân thực tế.
- Các nhóm CIBIL là khoảng phân tích tự chọn. Ngưỡng 550 phục vụ tra cứu ngoại lệ, không phải tiêu chuẩn ngân hàng.
- Q1–Q4 là tứ phân vị thu nhập tính từ toàn bộ nguồn để giữ nhóm ổn định giữa các lần lọc. Do trùng giá trị ở ranh giới nên số hồ sơ giữa các nhóm có thể khác nhau.
- Vay / thu nhập năm là số lần, không phải DTI vì không có nghĩa vụ trả nợ định kỳ.
- Chưa có ngày hồ sơ, mục đích vay, nợ xấu và lịch sử trả nợ. Không tạo biểu đồ thời gian, không kết luận nguyên nhân hoặc dự báo vỡ nợ.

## Kiểm tra lại

```bash
python -m unittest test_project -v
```

Nhóm cần tự chạy lại và hiểu các công thức trước khi vấn đáp. Sản phẩm hỗ trợ học tập có sử dụng AI. 

## Liên kết

- Dashboard: https://nhom1-loan-approval-dashboard.streamlit.app/
- Mã nguồn: https://github.com/18Kien17A3/DHKL17A3HN_Nhom01_TinDung
