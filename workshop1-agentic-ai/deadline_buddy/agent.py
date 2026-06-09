"""Deadline Buddy ⏰ — agent ที่เราจะพาสร้างสดใน workshop

เวอร์ชันนี้คือ "ผลลัพธ์สุดท้าย" เก็บไว้เผื่อพิมพ์ตามไม่ทัน
(ขั้นตอนการสร้างทีละบรรทัดอยู่ใน README ของ workshop 1)
"""

import random
from datetime import date

from google.adk.agents import Agent


def days_left(deadline: str) -> str:
    """นับว่าเหลืออีกกี่วันจะถึงกำหนดส่งงานหรือวันสอบ

    Args:
        deadline: วันกำหนดส่ง รูปแบบ YYYY-MM-DD เช่น "2026-06-30"

    Returns:
        ข้อความบอกจำนวนวันที่เหลือ
    """
    target = date.fromisoformat(deadline)
    days = (target - date.today()).days
    if days < 0:
        return f"เลยกำหนดมาแล้ว {-days} วัน! 😱"
    return f"เหลืออีก {days} วัน"


def pick_one(choices: list[str]) -> str:
    """จับสลากเลือก 1 อย่างจากตัวเลือกที่ให้มา เช่น เลือกหัวข้อรายงาน เลือกคนนำเสนอ

    Args:
        choices: รายการตัวเลือก เช่น ["หัวข้อ A", "หัวข้อ B"]

    Returns:
        ตัวเลือกที่สุ่มได้
    """
    return f"ผลจับสลาก: {random.choice(choices)} 🎲"


root_agent = Agent(
    name="deadline_buddy",
    model="gemini-2.5-flash",
    description="เพื่อนเตือนเดดไลน์และช่วยตัดสินใจของนักศึกษา",
    instruction="""
คุณคือ Deadline Buddy เพื่อนรักนักศึกษา พูดไทยติดตลกนิดๆ

- ถามถึงเดดไลน์/วันสอบว่าเหลือกี่วัน → ใช้ tool days_left
- ตัดสินใจไม่ได้ ให้ช่วยเลือก → ใช้ tool pick_one
- ถ้าเหลือเวลาน้อยกว่า 7 วัน ให้แซวเบาๆ แล้วช่วยวางแผนคร่าวๆ ให้ด้วย
""",
    tools=[days_left, pick_one],
)
