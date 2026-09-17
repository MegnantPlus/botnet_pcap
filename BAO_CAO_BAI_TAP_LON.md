# BÁO CÁO BÀI TẬP LỚN
## ĐỀ TÀI: ỨNG DỤNG HỌC MÁY TRONG PHÁT HIỆN BOTNET TỪ LƯU LƯỢNG MẠNG
*(Machine Learning for Botnet Detection from Network Traffic)*

**HỌC PHẦN:** AN TOÀN VÀ BẢO MẬT THÔNG TIN  
**TRƯỜNG:** ĐẠI HỌC XÂY DỰNG HÀ NỘI (HUCE) - KHOA CÔNG NGHỆ THÔNG TIN  
**GIẢNG VIÊN HƯỚNG DẪN:** ThS. Nguyễn Việt Nhật  

**DANH SÁCH NHÓM SINH VIÊN THỰC HIỆN:**
1. **Nguyễn Bá Hùng** - MSV: 0368269
2. **Nguyễn Duy Hùng** - MSV: 0368369
3. **Lê Quang Huy** - MSV: 0368469
4. **Ngô Xuân Trung** - MSV: 0373569
5. **Bùi Đức Thắng** - MSV: 0373069

---

### MỤC LỤC & KỊCH BẢN THUYẾT TRÌNH (SLIDE OUTLINE)

* **Slide 1:** Trang bìa: Tên đề tài, Giảng viên hướng dẫn, Sinh viên thực hiện.
* **Slide 2:** Tính cấp thiết & Đặt vấn đề (Tại sao cần Học máy cho Botnet?).
* **Slide 3:** Kiến trúc Pipeline hệ thống (Từ PCAP -> Flow -> Feature Extraction -> ML -> Alert).
* **Slide 4:** Bộ dữ liệu thực nghiệm chuẩn quốc tế CTU-13.
* **Slide 5:** Lựa chọn các thuật toán Học máy (Logistic Regression, Decision Tree, Random Forest).
* **Slide 6:** Kết quả thực nghiệm & Bảng so sánh chỉ số.
* **Slide 7:** Phân tích Ma trận nhầm lẫn (Confusion Matrix) & Đường cong ROC.
* **Slide 8:** Phân tích đặc trưng quan trọng nhất (Feature Importance & Ý nghĩa ATTT).
* **Slide 9:** Demo chạy thực tế thời gian thực.
* **Slide 10:** Kết luận, Đánh giá liên hệ hệ thống Slips (Stratosphere IPS) & Hướng phát triển.

---

### PHẦN 1. ĐẶT VẤN ĐỀ VÀ MỤC TIÊU NGHIÊN CỨU

#### 1. Tính cấp thiết của đề tài
* **Sự nguy hiểm của Botnet:** Botnet (mạng máy tính ma) là công cụ hàng đầu của tội phạm mạng để thực hiện các cuộc tấn công từ chối dịch vụ phân tán (DDoS), phát tán mã độc tống tiền (Ransomware), đánh cắp dữ liệu và thiết lập kênh điều khiển ngầm Command & Control (C2).
* **Hạn chế của giải pháp truyền thống (Signature-based IDS):**
  * Các hệ thống như Snort hay Suricata chủ yếu dựa vào chữ ký tĩnh (Signatures) và kiểm tra nội dung gói tin (Deep Packet Inspection - DPI).
  * *Hạn chế chí mạng:* Khi lưu lượng mạng bị mã hóa qua TLS/HTTPS hoặc botnet thay đổi biến thể (Zero-day), các hệ thống dựa trên luật hoàn toàn bị qua mặt.
* **Giải pháp Học máy (Machine Learning):**
  * Chuyển từ phân tích nội dung gói tin sang **phân tích đặc trưng hành vi luồng mạng (Flow-based Analysis)**.
  * Nhận diện được hành vi bất thường của Botnet dựa vào các quy luật thống kê (thời gian ngắt quãng, kích thước luồng, chu kỳ gửi tin C2) kể cả khi gói tin đã bị mã hóa.

---

### PHẦN 2. KIẾN TRÚC PIPELINE XỬ LÝ

Quy trình phát hiện Botnet được thiết kế theo chuẩn công nghiệp:

```
[Lưu lượng mạng PCAP] 
          ↓
[Bóc tách Flow & Trích xuất đặc trưng] (CICFlowMeter / Zeek)
          ↓ 57 Đặc trưng thống kê (Flow Duration, IAT, Byte/s, TCP Flags...)
[Tiền xử lý & Chuẩn hóa] (StandardScaler, Xử lý giá trị Inf/NaN)
          ↓
[Huấn luyện & Phân loại ML] (Logistic Regression, Decision Tree, Random Forest)
          ↓
[Cảnh báo xâm nhập & Dự đoán thời gian thực] (Độ trễ < 2ms/flow)
```

---

### PHẦN 3. BỘ DỮ LIỆU THỰC NGHIỆM (CTU-13 DATASET)

* **Nguồn gốc:** CTU-13 được thu thập và công bố bởi **Stratosphere Laboratory (Đại học Kỹ thuật Séc - CTU Prague)** – cũng chính là nhóm tác giả phát triển hệ thống phòng thủ mã nguồn mở nổi tiếng **Stratosphere Linux IPS (Slips)**.
* **Đặc điểm tập dữ liệu:**
  * Ghi lại lưu lượng thực tế gồm cả mạng bình thường (Normal) và 13 kịch bản Botnet đa dạng (Neris, Rbot, Virut, Menti, Sogou...).
  * Được bóc tách thành các luồng mạng hai chiều (Bidirectional NetFlow) bằng công cụ **CICFlowMeter**.
* **Phân bố dữ liệu thực nghiệm:**
  * **Tổng số luồng:** 92,212 flows.
  * **Lưu lượng tấn công (Botnet Attack):** 38,898 flows (~42.2%).
  * **Lưu lượng an toàn (Normal Traffic):** 53,314 flows (~57.8%).
  * **Chia tập dữ liệu:** 80% Huấn luyện (73,769 mẫu) và 20% Kiểm thử độc lập (18,443 mẫu) với phương pháp Stratified Sampling nhằm giữ nguyên tỷ lệ nhãn.

---

### PHẦN 4. KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ

*(Dữ liệu từ thực nghiệm chạy trực tiếp trên máy kiểm thử)*

#### 1. Bảng so sánh hiệu năng các mô hình

| Thuật toán | Accuracy (%) | Precision (%) | Recall (%) | F1-Score | ROC-AUC | Thời gian huấn luyện (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 92.88% | 93.37% | 89.46% | 0.9137 | 0.9699 | 1.44 s |
| **Decision Tree** | 99.59% | 99.73% | 99.31% | 0.9952 | 0.9957 | 1.84 s |
| **Random Forest (Best)** | **99.71%** | **99.79%** | **99.51%** | **0.9965** | **0.9999** | **2.38 s** |

#### 2. Phân tích chi tiết mô hình Random Forest
* **Độ chính xác vượt trội:** Đạt **99.71%** với F1-score đạt **0.9965**.
* **Độ nhạy phát hiện (Recall = 99.51%):** Trong bài toán an toàn thông tin, chỉ số Recall cực kỳ quan trọng vì nếu bỏ lọt Botnet (False Negative), hệ thống sẽ bị chiếm quyền điều khiển. Mô hình chỉ để lọt dưới 0.5% các luồng tấn công.
* **Tỷ lệ báo động giả (False Positive) cực thấp:** Precision đạt **99.79%**, giúp nhân viên SOC/vận hành mạng không bị ngập trong cảnh báo giả.
* **Đường cong ROC:** Chỉ số AUC đạt **0.9999**, chứng minh khả năng phân tách ranh giới giữa lưu lượng Botnet và lưu lượng sạch gần như hoàn hảo.

*(Xem các biểu đồ xuất ra tại thư mục `output_charts/`:*
* *`output_charts/1_metrics_comparison.png`*
* *`output_charts/2_confusion_matrix_rf.png`*
* *`output_charts/3_roc_curves.png`*
* *`output_charts/4_feature_importance_rf.png`)*

#### 3. Ý nghĩa an toàn thông tin của các đặc trưng quan trọng nhất (Feature Importance)
Biểu đồ Top 15 đặc trưng chỉ ra những thông số mạng quyết định việc nhận dạng Botnet:
1. **`Idle Max` & `Idle Mean`:** Thời gian tĩnh của luồng mạng. Botnet thường có các khoảng dừng định kỳ để "nghe ngóng" hoặc chờ lệnh từ máy chủ C2 (chu kỳ Beaconing/Keep-alive).
2. **`Flow Duration`:** Thời gian tồn tại của luồng. Kênh điều khiển C2 thường duy trì kết nối âm ỉ kéo dài hoặc rất ngắn (quét cổng).
3. **`TotLen Bwd Pkts` & `Bwd Pkt Len Max`:** Kích thước phản hồi từ máy chủ đích. Các lệnh điều khiển C2 thường có kích thước rất đặc trưng so với việc duyệt web thông thường.
4. **`Flow IAT Mean` (Inter-Arrival Time):** Thời gian giữa các gói tin liên tiếp, phản ánh hành vi tự động của mã độc thay vì thao tác tự nhiên của con người.

---

### PHẦN 5. LIÊN HỆ VỚI HỆ THỐNG THỰC TẾ (STRATOSPHERE IPS - SLIPS)

* Dự án **Stratosphere Linux IPS (Slips)** là một minh chứng tiêu chuẩn trong việc đưa các nghiên cứu học máy từ bộ dữ liệu CTU-13 vào sản phẩm thực tế.
* Slips kết hợp kiến trúc đa tầng:
  * Sử dụng Zeek để parse PCAP thành Flow.
  * Chuyển đổi các đặc trưng luồng thành các chuỗi ký tự hành vi (Behavioral State Letters).
  * Tích hợp module Machine Learning (như Random Forest, LSTM cho DGA) kết hợp với các nguồn Threat Intelligence IoC.
* **Đóng góp của đề tài:** Pipeline mà nhóm xây dựng đã giải mã trọn vẹn lớp lõi Machine Learning: chứng minh rằng việc sử dụng các đặc trưng luồng (Flow features) hoàn toàn đủ khả năng nhận diện chính xác 99.7% hành vi Botnet với độ trễ tính bằng mili-giây, là cơ sở để tích hợp vào các hệ thống IPS như Slips.

---

### PHẦN 6. BỘ CÂU HỎI VÀ ĐÁP ÁN PHẢN BIỆN (DÀNH CHO HỘI ĐỒNG BẢO VỆ)

**Câu 1: Tại sao em không dùng Deep Learning (CNN/RNN) mà lại chọn Random Forest?**
> *Trả lời:* Trong bài toán phát hiện luồng mạng thời gian thực (NIDS), dữ liệu là dạng bảng có cấu trúc (Tabular Data). Nhiều nghiên cứu thực nghiệm đã chỉ ra Random Forest và XGBoost hoạt động ổn định, hiệu quả và ít tốn tài nguyên hơn Deep Learning trên dạng dữ liệu này. Ngoài ra, Random Forest có thời gian suy luận (Inference time) cực nhanh (< 2ms/flow) và có tính giải thích cao (Feature Importance), phù hợp cho việc triển khai ở cổng mạng thực tế mà không cần trang bị GPU đắt tiền.

**Câu 2: Nếu Botnet mã hóa lưu lượng qua HTTPS/SSH thì mô hình có phát hiện được không?**
> *Trả lời:* Hoàn toàn phát hiện được! Bởi vì mô hình của nhóm không dựa vào nội dung bên trong gói tin (Payload), mà dựa vào các đặc trưng siêu dữ liệu của luồng (Metadata/Statistical Features) như: thời lượng luồng, thời gian cách quãng giữa các gói (IAT), kích thước gói tin, và các cờ TCP. Dù mã hóa thì các đặc trưng hành vi này vẫn không bị thay đổi.

**Câu 3: Bộ dữ liệu CTU-13 thu thập từ năm 2011, liệu có còn giá trị với Botnet hiện đại không?**
> *Trả lời:* CTU-13 là bộ benchmark kinh điển được trích dẫn hàng nghìn lần trong giới học thuật bảo mật. Mặc dù các họ mã độc mới xuất hiện liên tục, nhưng kiến trúc cốt lõi của Botnet (quét mạng để lây nhiễm, duy trì kênh kết nối ngầm C2 định kỳ, phát động DDoS) vẫn tuân theo các quy luật hành vi thống kê mạng cơ bản. Mô hình học được "hành vi" chứ không học "chữ ký cố định", do đó vẫn có giá trị nền tảng rất cao.

**Câu 4: Làm thế nào để chạy thử nghiệm thời gian thực?**
> *Trả lời:* Nhóm đã đóng gói mô hình thành file `random_forest_botnet.pkl` và viết sẵn script `demo_detect.py`. Chỉ cần nạp luồng mạng vào, mô hình sẽ tính toán và trả về kết quả nhãn kèm độ tin cậy (Confidence Score) ngay lập tức.
