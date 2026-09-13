# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Minh Dương

> **Mã Sinh Viên / Mã Học viên:** 20225439

> **Chủ đề Lựa chọn:** Trợ lý Tư vấn Sức khỏe Vinmec: Tra cứu lịch làm việc bác sĩ chuyên khoa và đặt lịch khám bệnh.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Bài toán có yêu cầu chia nhỏ nhiều bước suy luận nối tiếp nhau không? |
| **2. Tool Interaction** | 5 / 5 | Hệ thống có cần kết nối với MCP Server / Cơ sở dữ liệu bên ngoài không? |
| **3. Dynamic Decision** | 3 / 5 | Bước tiếp theo có phụ thuộc vào kết quả quan sát bước trước không? |
| **4. Long Horizon Goal** | 4 / 5 | Hệ thống có phải giữ mục tiêu xuyên suốt qua nhiều lượt xử lý không? |
| **TỔNG ĐIỂM AGENTIC FIT** | **16 / 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Đặt cho tôi một lịch khám với Bác sĩ Nguyễn Thị B chuyên khoa Nhi tại Vinmec Central Park vào sáng thứ 6 tuần này lúc 9:00. Thông tin bệnh nhân: Lê Văn C, SĐT: 0901234567.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "book_appointment",
    "arguments": {
      "doctor_name": "Nguyễn Thị B",
      "patient_name": "Lê Văn C",
      "specialty": "Nhi",
      "appointment_datetime": "sáng thứ 6 tuần này lúc 9:00",
      "hospital": "Vinmec Central Park",
      "phone_number": "0901234567"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "VM-4567-99",
      "doctor_name": "Nguyễn Thị B",
      "specialty": "Nhi",
      "hospital": "Vinmec Central Park",
      "appointment_datetime": "sáng thứ 6 tuần này lúc 9:00",
      "patient_name": "Lê Văn C",
      "phone_number": "0901234567",
      "message": "Đặt lịch khám thành công cho bệnh nhân Lê Văn C với bác sĩ Nguyễn Thị B vào lúc sáng thứ 6 tuần này lúc 9:00."
    },
    "latency_ms": 2891.49
  },
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ x ] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 3 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
