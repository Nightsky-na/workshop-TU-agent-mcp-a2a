"""เปิด Summarizer Agent เป็น A2A server 🌐

A2A (Agent2Agent) = มาตรฐานให้ agent คุยกันข้าม process / ข้ามเครื่อง / ข้ามองค์กร
agent ที่เปิดเป็น A2A server จะมี "นามบัตร" (Agent Card) ให้ agent อื่นมาอ่าน
ว่าตัวเองชื่ออะไร ทำอะไรได้บ้าง

วิธีรัน (จากโฟลเดอร์ workshop2-mcp-a2a):

    uvicorn summarizer_agent.a2a_server:app --host 0.0.0.0 --port 8001

แล้วลองเปิดดูนามบัตรที่ http://localhost:8001/.well-known/agent-card.json
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# โหลด API key จากไฟล์ .env ในโฟลเดอร์นี้
load_dotenv(Path(__file__).parent / ".env")

from google.adk.a2a.utils.agent_to_a2a import to_a2a

from summarizer_agent.agent import root_agent

# A2A_HOST = ที่อยู่ที่จะประกาศในนามบัตร
# - ทดลองในเครื่องตัวเอง: localhost (ค่าเริ่มต้น)
# - ให้เพื่อนเรียกข้ามเครื่อง: ตั้งเป็น IP ของเรา เช่น A2A_HOST=192.168.1.42
A2A_HOST = os.environ.get("A2A_HOST", "localhost")

app = to_a2a(root_agent, host=A2A_HOST, port=8001)
