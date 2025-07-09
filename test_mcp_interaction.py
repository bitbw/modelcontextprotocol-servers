#!/usr/bin/env python3
"""
演示 MCP 服务器如何工作的简单示例
"""

import json
from datetime import datetime
from zoneinfo import ZoneInfo

def simulate_mcp_server():
    """
    模拟 Time MCP 服务器的工作原理
    """
    print("🤖 Claude: 发现用户问题 - '现在北京时间是几点？'")
    print("📋 Claude: 查询可用工具...")
    
    # 模拟服务器返回的工具列表
    available_tools = [
        {
            "name": "get_current_time",
            "description": "获取特定时区的当前时间",
            "parameters": {
                "timezone": "IANA时区名称，如 'Asia/Shanghai'"
            }
        },
        {
            "name": "convert_time", 
            "description": "在时区之间转换时间",
            "parameters": {
                "source_timezone": "源时区",
                "time": "时间(HH:MM)",
                "target_timezone": "目标时区"
            }
        }
    ]
    
    print("🔍 可用工具:")
    for tool in available_tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    print("\n🧠 Claude: 分析用户意图...")
    print("   用户问题: '现在北京时间是几点？'")
    print("   → 需要获取当前时间")
    print("   → 选择工具: get_current_time")
    print("   → 参数: timezone='Asia/Shanghai'")
    
    print("\n📞 Claude: 调用 MCP 服务器...")
    
    # 模拟实际的工具调用
    def get_current_time(timezone):
        tz = ZoneInfo(timezone)
        current_time = datetime.now(tz)
        return {
            "timezone": timezone,
            "datetime": current_time.isoformat(),
            "is_dst": bool(current_time.dst())
        }
    
    result = get_current_time("Asia/Shanghai")
    print(f"⚡ 服务器返回: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    print("\n💬 Claude: 生成用户友好的回复...")
    print(f"   现在北京时间是: {result['datetime'][:19].replace('T', ' ')}")

if __name__ == "__main__":
    simulate_mcp_server() 