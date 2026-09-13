"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
import re
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "search_doctors",
        "description": "Tìm bác sĩ phù hợp theo chuyên khoa, chức danh và cơ sở Vinmec để đề xuất lịch khám.",
        "parameters": {
            "type": "object",
            "properties": {
                "specialty": {
                    "type": "string",
                    "description": "Chuyên khoa cần tìm (ví dụ: 'Nhi')"
                },
                "title": {
                    "type": "string",
                    "description": "Chức danh hoặc tiêu chí bác sĩ (ví dụ: 'Trưởng khoa')"
                },
                "hospital": {
                    "type": "string",
                    "description": "Cơ sở Vinmec cần tìm bác sĩ"
                },
                "date": {
                    "type": "string",
                    "description": "Ngày cần tìm lịch trống"
                },
                "preferred_datetime": {
                    "type": "string",
                    "description": "Ngày hoặc giờ người dùng mong muốn, nếu có"
                }
            },
            "required": ["specialty", "hospital"]
        }
    },
    {
        "name": "get_doctor_schedule",
        "description": "Tra cứu lịch làm việc và các khung giờ khám của bác sĩ chuyên khoa tại cơ sở Vinmec.",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_name": {
                    "type": "string",
                    "description": "Họ tên bác sĩ cần tra cứu (ví dụ: 'Trần Văn A')"
                },
                "specialty": {
                    "type": "string",
                    "description": "Chuyên khoa của bác sĩ (ví dụ: 'Tim mạch')"
                },
                "hospital": {
                    "type": "string",
                    "description": "Cơ sở Vinmec cần tra cứu (ví dụ: 'Vinmec Times City')"
                },
                "date": {
                    "type": "string",
                    "description": "Ngày hoặc khoảng thời gian cần tra cứu, nếu người dùng có nêu"
                }
            },
            "required": ["doctor_name", "specialty", "hospital"]
        }
    },
    {
        "name": "book_appointment",
        "description": "Đặt lịch khám bệnh với bác sĩ chuyên khoa tại cơ sở Vinmec.",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_name": {
                    "type": "string",
                    "description": "Họ tên bác sĩ muốn đặt lịch"
                },
                "specialty": {
                    "type": "string",
                    "description": "Chuyên khoa khám bệnh"
                },
                "hospital": {
                    "type": "string",
                    "description": "Cơ sở Vinmec nơi người bệnh muốn khám"
                },
                "appointment_datetime": {
                    "type": "string",
                    "description": "Ngày và giờ khám mong muốn (ví dụ: '09:00 thứ 6, 18/09/2026')"
                },
                "patient_name": {
                    "type": "string",
                    "description": "Họ tên bệnh nhân"
                },
                "phone_number": {
                    "type": "string",
                    "description": "Số điện thoại liên hệ của bệnh nhân"
                }
            },
            "required": [
                "doctor_name",
                "specialty",
                "hospital",
                "appointment_datetime",
                "patient_name",
                "phone_number"
            ]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DOCTOR_SCHEDULES = [
    {
        "doctor_name": "Trần Văn A",
        "specialty": "Tim mạch",
        "hospital": "Vinmec Times City",
        "title": "Bác sĩ chuyên khoa",
        "working_hours": ["08:00-12:00 thứ 3", "13:30-17:00 thứ 6"]
    },
    {
        "doctor_name": "Nguyễn Thị B",
        "specialty": "Nhi",
        "hospital": "Vinmec Central Park",
        "title": "Bác sĩ chuyên khoa",
        "working_hours": ["08:00-12:00 thứ 2", "09:00-11:30 thứ 6"]
    },
    {
        "doctor_name": "Bác sĩ Lê Minh C",
        "specialty": "Nhi",
        "hospital": "Vinmec Times City",
        "title": "Trưởng khoa Nhi",
        "working_hours": ["09:00-10:00 hôm nay", "14:00-16:00 thứ 6"]
    }
]


def execute_search_doctors(
    specialty: str,
    hospital: str,
    title: str = "",
    date: str = "",
    preferred_datetime: str = "",
) -> str:
    """Tìm danh sách bác sĩ phù hợp để agent có thể đề xuất cho người dùng."""
    matches = [
        item for item in MOCK_DOCTOR_SCHEDULES
        if item["specialty"].casefold() == specialty.strip().casefold()
        and item["hospital"].casefold() == hospital.strip().casefold()
        and (not title or title.strip().casefold() in item["title"].casefold())
    ]
    if matches:
        recommended_doctor = matches[0]
        recommended_slot = recommended_doctor["working_hours"][0]
        requested_hour = re.search(r"\b([01]?\d|2[0-3])(?::\d{2})?\b", preferred_datetime)
        if requested_hour:
            hour = requested_hour.group(1).zfill(2)
            for doctor in matches:
                matching_slot = next(
                    (slot for slot in doctor["working_hours"] if hour in slot),
                    None,
                )
                if matching_slot:
                    recommended_doctor = doctor
                    recommended_slot = matching_slot
                    break
        return json.dumps({
            "status": "SUCCESS",
            "specialty": specialty,
            "hospital": hospital,
            "title": title,
            "date": date,
            "preferred_datetime": preferred_datetime,
            "recommended_slot": {
                "doctor_name": recommended_doctor["doctor_name"],
                "datetime": recommended_slot,
                "reason": "Khung giờ sớm nhất trong dữ liệu lịch hiện có."
            },
            "data": matches
        }, ensure_ascii=False)
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy bác sĩ chuyên khoa {specialty} phù hợp tại {hospital}."
    }, ensure_ascii=False)


def execute_get_doctor_schedule(
    doctor_name: str, specialty: str, hospital: str, date: str = ""
) -> str:
    """Thực thi tra cứu lịch làm việc bác sĩ theo các tiêu chí đã chọn."""
    schedule = next(
        (
            item for item in MOCK_DOCTOR_SCHEDULES
            if item["doctor_name"].casefold() == doctor_name.strip().casefold()
            and item["specialty"].casefold() == specialty.strip().casefold()
            and item["hospital"].casefold() == hospital.strip().casefold()
        ),
        None,
    )
    if schedule:
        return json.dumps({
            "status": "SUCCESS",
            "doctor_name": doctor_name,
            "specialty": specialty,
            "hospital": hospital,
            "date": date,
            "data": schedule
        }, ensure_ascii=False)
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy lịch của bác sĩ {doctor_name} chuyên khoa {specialty} tại {hospital}."
    }, ensure_ascii=False)


def execute_book_appointment(
    doctor_name: str,
    specialty: str,
    hospital: str,
    appointment_datetime: str,
    patient_name: str,
    phone_number: str,
) -> str:
    """Thực thi đặt lịch khám bệnh."""
    doctor_exists = any(
        item["doctor_name"].casefold() == doctor_name.strip().casefold()
        and item["specialty"].casefold() == specialty.strip().casefold()
        and item["hospital"].casefold() == hospital.strip().casefold()
        for item in MOCK_DOCTOR_SCHEDULES
    )
    if not doctor_exists:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy bác sĩ {doctor_name} chuyên khoa {specialty} tại {hospital}; chưa thể đặt lịch."
        }, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"VM-{phone_number[-4:]}-99",
        "doctor_name": doctor_name,
        "specialty": specialty,
        "hospital": hospital,
        "appointment_datetime": appointment_datetime,
        "patient_name": patient_name,
        "phone_number": phone_number,
        "message": f"Đặt lịch khám thành công cho bệnh nhân {patient_name} với bác sĩ {doctor_name} vào lúc {appointment_datetime}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "search_doctors": execute_search_doctors,
    "get_doctor_schedule": execute_get_doctor_schedule,
    "book_appointment": execute_book_appointment
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
