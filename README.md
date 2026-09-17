# 🛡️ Ứng Dụng Học Máy Trong Phát Hiện Botnet Từ Lưu Lượng Mạng
### *Machine Learning for Botnet Detection from Network Traffic*

> **HỌC PHẦN:** AN TOÀN VÀ BẢO MẬT THÔNG TIN  
> **TRƯỜNG:** ĐẠI HỌC XÂY DỰNG HÀ NỘI (HUCE) -- KHOA CÔNG NGHỆ THÔNG TIN  
> **GIẢNG VIÊN HƯỚNG DẪN:** ThS. Nguyễn Việt Nhật  

---

## 👥 Danh sách Nhóm sinh viên thực hiện
| STT | Họ và Tên | Mã số sinh viên | Vai trò |
| :---: | :--- | :---: | :--- |
| 1 | **Nguyễn Bá Hùng** | `0368269` | Trưởng nhóm, Xây dựng Pipeline & Báo cáo |
| 2 | **Nguyễn Duy Hùng** | `0368369` | Xử lý dữ liệu & Huấn luyện mô hình |
| 3 | **Lê Quang Huy** | `0368469` | Đánh giá chỉ số & Trực quan hóa dữ liệu |
| 4 | **Ngô Xuân Trung** | `0373569` | Nghiên cứu đặc trưng mạng & Feature Selection |
| 5 | **Bùi Đức Thắng** | `0373069` | Thiết kế Slide trình chiếu & Demo thời gian thực |

---

## 📌 Giới thiệu đề tài
Hệ thống phát hiện xâm nhập truyền thống (DPI / Snort) chủ yếu dựa vào chữ ký tĩnh và kiểm tra nội dung gói tin, do đó bị vô hiệu hóa khi lưu lượng mạng bị mã hóa TLS/HTTPS ($>90\%$ lưu lượng Internet) hoặc trước các biến thể mã độc mới (*Zero-day*).

Dự án này ứng dụng **Machine Learning** phân tích các **đặc trưng hành vi của luồng mạng hai chiều (Flow-based Analysis)** từ bộ dữ liệu chuẩn quốc tế **CTU-13** (thu thập bởi *Stratosphere Laboratory*, tác giả hệ thống *Slips*), bóc tách bởi công cụ **CICFlowMeter**.

---

## 📊 Kết quả thực nghiệm (92,212 luồng mạng)
Thử nghiệm độc lập trên **18,443 luồng kiểm thử (Test set)**:

| Thuật toán | Accuracy (%) | Precision (%) | Recall (%) | F1-Score | ROC-AUC | Thời gian train |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 92.88% | 93.37% | 89.46% | 0.9137 | 0.9699 | 1.44 s |
| **Decision Tree** | 99.59% | 99.73% | 99.31% | 0.9952 | 0.9957 | 1.84 s |
| **Random Forest (Best)** | **99.71%** | **99.79%** | **99.51%** | **0.9965** | **0.9999** | **2.38 s** |

* **Độ nhạy phát hiện (Recall = 99.51%):** Bỏ sót dưới 0.49% các cuộc tấn công Botnet.
* **Tối ưu hóa đặc trưng (Feature Selection):** Rút gọn từ 57 đặc trưng xuống **Top 10 đặc trưng quan trọng nhất**, độ chính xác vẫn đạt **99.82%**, giảm **82.5% tải tính toán** cho Router/Firewall.

---

## 📂 Cấu trúc thư mục dự án
```text
├── CTU13_Attack_Traffic.csv          # Tập dữ liệu lưu lượng Botnet (38,898 flows)
├── CTU13_Normal_Traffic.csv          # Tập dữ liệu lưu lượng bình thường (53,314 flows)
├── train_models.py                   # Script huấn luyện & xuất biểu đồ đánh giá
├── demo_detect.py                    # Chương trình phát hiện Botnet thời gian thực
├── saved_models/                     # Thư mục lưu trữ mô hình đã huấn luyện (.pkl)
│   ├── random_forest_botnet.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
├── output_charts/                    # Biểu đồ trực quan hóa
│   ├── 1_metrics_comparison.png
│   ├── 2_confusion_matrix_rf.png
│   ├── 3_roc_curves.png
│   └── 4_feature_importance_rf.png
├── bao_cao_huce.tex                  # Báo cáo chuẩn quy định ĐH Xây dựng (LaTeX)
├── presentation.tex                  # Slide báo cáo chuẩn HUCE Beamer (LaTeX)
├── BAO_CAO_BAI_TAP_LON.md            # Báo cáo chi tiết dạng Markdown
└── HUCE_Full_Bao_Cao_Va_Slide.zip    # Trọn gói nén nộp bài / biên dịch Overleaf
```

---

## 🚀 Hướng dẫn cài đặt & Chạy chương trình

### 1. Cài đặt thư viện yêu cầu
```bash
pip install pandas numpy scikit-learn matplotlib joblib
```

### 2. Huấn luyện mô hình từ đầu & Xuất biểu đồ
```bash
python train_models.py
```

### 3. Chạy Demo phát hiện trực tiếp
```bash
python demo_detect.py
```

---
*© 2026 Nhóm nghiên cứu Khoa Công nghệ Thông tin -- Trường Đại học Xây dựng Hà Nội (HUCE).*
