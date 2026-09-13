"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa.
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPAcademicServer:
    """
    Giả lập MCP Server tuân thủ chuẩn giao thức Model Context Protocol
    """
    def __init__(self, server_name: str = "vinmec-healthcare-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Thực thi tool Vinmec và đóng gói kết quả theo JSON-RPC 2.0.
        """
        tool_result = dispatch_tool_call(tool_name, arguments)
        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": json.loads(tool_result),
        }


if __name__ == "__main__":
    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (vinmec-healthcare-mcp-server)")
    print("==========================================================")
    
    server = MCPAcademicServer()
    tools = server.list_tools()
    print(f"✅ Khởi tạo thành công MCP Server: {server.server_name} (Version: {server.version})")
    print(f"📦 Số lượng Tools công bố: {len(tools)}")
    
    # Kiểm tra schema của hai tool phục vụ tra cứu và đặt lịch khám.
    schedule_tool = next((t for t in tools if t.get("name") == "get_doctor_schedule"), None)
    booking_tool = next((t for t in tools if t.get("name") == "book_appointment"), None)
    if not schedule_tool or not booking_tool:
        print("⏳ [SCHEMA]: Chưa công bố đủ get_doctor_schedule và book_appointment.")
    else:
        print("✅ [SCHEMA]: Đã công bố đủ tool tra cứu lịch và đặt lịch khám.")

    schedule_result = server.call_tool("get_doctor_schedule", {
        "doctor_name": "Trần Văn A",
        "specialty": "Tim mạch",
        "hospital": "Vinmec Times City",
    })
    booking_result = server.call_tool("book_appointment", {
        "doctor_name": "Nguyễn Thị B",
        "specialty": "Nhi",
        "hospital": "Vinmec Central Park",
        "appointment_datetime": "09:00 thứ 6, 18/09/2026",
        "patient_name": "Lê Văn C",
        "phone_number": "0901234567",
    })
    if schedule_result["result"].get("status") == "SUCCESS" and booking_result["result"].get("status") == "SUCCESS":
        print("✅ [TOOLS]: Tra cứu lịch và đặt lịch khám thành công.")
        print(f"   Phản hồi JSON-RPC: {json.dumps(booking_result, ensure_ascii=False)}")
    else:
        print("⚠️ [TOOLS]: Kiểm thử tool Vinmec chưa thành công.")
