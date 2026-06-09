"""Host Agent 🎯 — agent หลักที่ต่อกับโลกภายนอก 2 ทาง

1. MCP  → ใช้ tools จาก Paper MCP Server (process แยกต่างหาก)
2. A2A  → ส่งงานต่อให้ Summarizer Agent (อีก server / อีกเครื่อง)

         ┌─────────────┐   MCP    ┌──────────────────┐
 เรา ──▶ │ Host Agent  │ ───────▶ │ paper_mcp.py     │  ค้น paper / จดโน้ต
         │             │          └──────────────────┘
         │             │   A2A    ┌──────────────────┐
         │             │ ───────▶ │ Summarizer Agent │  สรุปงานวิจัย
         └─────────────┘          │ (port 8001)      │
                                  └──────────────────┘
"""

import os
import sys
from pathlib import Path

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import (
    AGENT_CARD_WELL_KNOWN_PATH,
    RemoteA2aAgent,
)
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from mcp import StdioServerParameters

# ---------- ส่วนที่ 1: ต่อ MCP server ----------
# agent จะ start process ของ paper_mcp.py ให้เอง แล้วคุยกันผ่าน stdio
PAPER_MCP = str(Path(__file__).parent.parent / "mcp_server" / "paper_mcp.py")

paper_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,   # python ตัวเดียวกับที่รัน adk web
            args=[PAPER_MCP],
        ),
        timeout=30,
    ),
)

# ---------- ส่วนที่ 2: ต่อ A2A agent ----------
# SUMMARIZER_URL = ที่อยู่ของ Summarizer Agent
# - เครื่องตัวเอง: http://localhost:8001 (ค่าเริ่มต้น)
# - เครื่องเพื่อน: ตั้ง env ก่อนรัน adk web เช่น
#     SUMMARIZER_URL=http://192.168.1.42:8001 adk web
SUMMARIZER_URL = os.environ.get("SUMMARIZER_URL", "http://localhost:8001")

summarizer = RemoteA2aAgent(
    name="summarizer_agent",
    description="ผู้เชี่ยวชาญด้านการสรุปเนื้อหางานวิจัยเป็นภาษาไทย",
    agent_card=f"{SUMMARIZER_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
)

# ---------- Host Agent ----------
root_agent = Agent(
    name="host_agent",
    model="gemini-2.5-flash",
    description="ผู้ช่วยวิจัยหลัก ค้น paper ผ่าน MCP และส่งต่อให้ผู้เชี่ยวชาญสรุปผ่าน A2A",
    instruction="""
คุณคือผู้ช่วยทำวิจัยหลักของนักศึกษา พูดไทยเป็นกันเอง

- ค้นหา paper / จดโน้ต / อ่านโน้ต → ใช้ tools ที่มี (มาจาก MCP server)
- เมื่อผู้ใช้อยากได้ "สรุป" เนื้อหางานวิจัย → ส่งต่อให้ summarizer_agent
  (ผู้เชี่ยวชาญที่อยู่อีก server) เป็นคนสรุป
- ห้ามแต่งข้อมูล paper ขึ้นมาเอง
""",
    tools=[paper_toolset],
    sub_agents=[summarizer],
)
