"""เปิด Analyst Agent เป็น A2A server (port 8003)

วิธีรัน (จากโฟลเดอร์ project3-accounting-office):

    uvicorn analyst_agent.a2a_server:app --host 0.0.0.0 --port 8003

ดูนามบัตรได้ที่ http://localhost:8003/.well-known/agent-card.json
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from google.adk.a2a.utils.agent_to_a2a import to_a2a

from analyst_agent.agent import root_agent

# ตั้ง A2A_HOST=<IP ของเรา> ถ้าจะให้เครื่องอื่นเรียกข้ามเครื่อง
A2A_HOST = os.environ.get("A2A_HOST", "localhost")

app = to_a2a(root_agent, host=A2A_HOST, port=8003)
