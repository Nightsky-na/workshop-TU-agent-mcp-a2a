# 🤖 Workshop 1: Agentic-AI — สร้าง Agent ตัวแรกของคุณ

**เวลา 11:00 – 12:00** | ดู agent ตัวอย่างทำงาน แล้ว **พาสร้าง agent + tool ใหม่ของตัวเองตั้งแต่ศูนย์**

## Agent คืออะไร?

```
                    ┌──────────────────────────────┐
   คำถามของเรา ───▶ │           AGENT              │
                    │                              │
                    │  🧠 model       = สมอง (LLM)  │
                    │  📜 instruction = บุคลิก/กติกา │
                    │  🔧 tools       = เครื่องมือ    │ ──▶ คำตอบ
                    │                              │
                    │  agent "คิดเอง" ว่าจะใช้        │
                    │  เครื่องมือไหน เมื่อไหร่          │
                    └──────────────────────────────┘
```

ความต่างจาก chatbot ธรรมดา: agent **ตัดสินใจเองและลงมือทำ** (เรียก tool) ไม่ใช่แค่ตอบข้อความ

## 🏃 Step 1 — รัน agent ตัวอย่าง: Research Buddy (15 นาที)

```bash
cd workshop1-agentic-ai
adk web
```

เปิด <http://localhost:8000> เลือก `research_agent` แล้วลองพิมพ์:

> หา paper เกี่ยวกับ "multi agent systems" ให้หน่อย

> ช่วยจดไว้หน่อยว่าพรุ่งนี้ต้องส่งรายงาน

> สรุป paper อันแรกให้หน่อย แล้วจดเก็บไว้เลย

**สิ่งที่ต้องดู 👀:** คลิก event ในแถบซ้าย — จะเห็นว่า agent:
1. อ่านคำถามของเรา
2. **เลือกเรียก** `search_arxiv` / `save_note` เอง พร้อม arguments ที่มันคิดขึ้น
3. ได้ผลลัพธ์กลับมา แล้วเรียบเรียงเป็นคำตอบ

ข้อสุดท้าย agent จะต่อ tool หลายตัวเอง: `read_paper` ดึง PDF → สรุปเป็นไทย → `save_note` บันทึกให้

นี่คือหัวใจของ "agentic" — เราไม่ได้สั่งให้เรียก function, agent ตัดสินใจเอง
(โครงสร้าง code อยู่ใน `research_agent/` — แค่ 2 ไฟล์: `agent.py` กับ `tools.py`)

## ✨ Step 2 — พาสร้าง agent ใหม่ด้วยกัน: "Deadline Buddy" (25 นาที)

พิมพ์ตามทีละขั้น (ใครหลุดดูฉบับเต็มได้ที่ `solutions/deadline_buddy/`)

### 2.1 สร้างโฟลเดอร์ agent ใหม่ (ใน `workshop1-agentic-ai/`)

```bash
mkdir deadline_buddy
```

### 2.2 สร้างไฟล์ `deadline_buddy/__init__.py`

```python
from . import agent
```

### 2.3 สร้างไฟล์ `deadline_buddy/agent.py` — เริ่มจาก tool ก่อน

> 💡 tool = ฟังก์ชัน Python ธรรมดา + docstring ที่อธิบายชัดๆ ว่าใช้ทำอะไร

```python
from datetime import date

from google.adk.agents import Agent


def days_left(deadline: str) -> str:
    """นับว่าเหลืออีกกี่วันจะถึงกำหนดส่งงานหรือวันสอบ

    Args:
        deadline: วันกำหนดส่ง รูปแบบ YYYY-MM-DD เช่น "2026-06-30"
    """
    target = date.fromisoformat(deadline)
    days = (target - date.today()).days
    if days < 0:
        return f"เลยกำหนดมาแล้ว {-days} วัน! 😱"
    return f"เหลืออีก {days} วัน"
```

### 2.4 ต่อท้ายด้วยตัว agent

```python
root_agent = Agent(
    name="deadline_buddy",
    model="gemini-2.5-flash",
    description="เพื่อนเตือนเดดไลน์ของนักศึกษา",
    instruction="""
คุณคือ Deadline Buddy เพื่อนรักนักศึกษา พูดไทยติดตลกนิดๆ
- ถามถึงเดดไลน์/วันสอบว่าเหลือกี่วัน → ใช้ tool days_left
- ถ้าเหลือน้อยกว่า 7 วัน ให้แซวเบาๆ แล้วช่วยวางแผนให้
""",
    tools=[days_left],
)
```

### 2.5 ใส่ API key แล้วรัน

```bash
cp research_agent/.env deadline_buddy/.env
```

กลับไปหน้า adk web → refresh → เลือก `deadline_buddy` แล้วลอง:

> สอบ final วันที่ 30 มิ.ย. เหลือกี่วัน?

**จุดสังเกต 👀:** เราพิมพ์ "30 มิ.ย." แต่ใน trace จะเห็น agent แปลงเป็น `"2026-06-30"`
ให้ตรงรูปแบบที่ docstring บอกไว้เอง — docstring สำคัญขนาดนี้!

## 🔧 Step 3 — เพิ่ม tool ตัวที่สอง (15 นาที)

เพิ่มฟังก์ชันนี้เหนือ `root_agent` แล้วอย่าลืมใส่ใน `tools=[...]`:

```python
import random

def pick_one(choices: list[str]) -> str:
    """จับสลากเลือก 1 อย่างจากตัวเลือกที่ให้มา เช่น เลือกหัวข้อรายงาน เลือกคนนำเสนอ

    Args:
        choices: รายการตัวเลือก เช่น ["หัวข้อ A", "หัวข้อ B"]
    """
    return f"ผลจับสลาก: {random.choice(choices)} 🎲"
```

refresh แล้วลอง:

> เลือกไม่ถูกว่าจะทำรายงานเรื่อง LLM หรือ Computer Vision ดี จับสลากให้หน่อย

> งานส่ง 25 มิ.ย. เหลือกี่วัน แล้วช่วยเลือกหน่อยว่าควรเริ่มจากอ่าน paper หรือเขียน code ก่อน

ข้อหลังนี้ agent จะใช้ **2 tools ต่อกันเอง** — ดูลำดับใน trace!

## 🧪 Step 4 — อิสระ: tool ในแบบของคุณ (5 นาที + ทำต่อพักเที่ยงได้)

ไอเดีย: `gpa_calculator(grades: list[float])` · `coin_flip()` · `count_words(text: str)`
หรือคิดเองเลย — แค่เขียนฟังก์ชัน + docstring ดีๆ แล้วใส่ใน `tools=[...]`

## 📌 สรุปสิ่งที่ได้เรียนรู้

| แนวคิด | เห็นได้จาก |
|--------|-----------|
| Agent = model + instruction + tools | `agent.py` ที่เราพิมพ์เอง |
| Tool = ฟังก์ชัน Python + docstring ดีๆ | `days_left`, `pick_one` |
| Agent เลือก tool เอง + แปลง input ให้ตรง spec เอง | trace ใน adk web |

ช่วงบ่ายเราจะเอา agent ไป **ต่อกับโลกภายนอก** ผ่าน MCP และให้มัน **คุยกับ agent ของเพื่อน** ผ่าน A2A 🚀
