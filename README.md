# 🎓 Workshop: Agentic AI + MCP & A2A

สร้าง **"Research Buddy"** — ผู้ช่วยทำวิจัยส่วนตัวของนักศึกษา ด้วย [Google ADK](https://google.github.io/adk-docs/)

| ช่วง | Workshop | โฟลเดอร์ |
|------|----------|----------|
| 11:00 – 12:00 | **Workshop 1: Agentic-AI** — สร้าง agent ตัวแรก + เขียน tool เอง | [`workshop1-agentic-ai/`](workshop1-agentic-ai/) |
| 14:15 – 15:15 | **Workshop 2: MCP & A2A** — ต่อ agent เข้ากับโลกภายนอก + คุยกับ agent ของเพื่อน | [`workshop2-mcp-a2a/`](workshop2-mcp-a2a/) |
| demo ปิดท้าย | **Project 3: AI Accounting Office** — บริษัทจำลอง multi-agent (CEO + นักวิเคราะห์ + นักบัญชี) รวม MCP + A2A | [`project3-accounting-office/`](project3-accounting-office/) |

## ⚙️ Setup (ทำก่อนเริ่ม workshop — ใช้เวลา ~5 นาที)

> ต้องมี **Python 3.10 – 3.13** (เช็คด้วย `python3 --version`)

### 1) Clone และติดตั้ง

```bash
git clone <repo-url>
cd workshop-TU-agent-mcp-a2a

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2) ขอ Gemini API key (ฟรี)

1. ไปที่ <https://aistudio.google.com/apikey>
2. ล็อกอินด้วย Google account → กด **Create API key**
3. copy key เก็บไว้ (จะใช้ในขั้นถัดไป)

### 3) ใส่ API key

```bash
cp workshop1-agentic-ai/research_agent/.env.example workshop1-agentic-ai/research_agent/.env
```

แล้วเปิดไฟล์ `.env` ใส่ key ของตัวเอง:

```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=ใส่_key_ของคุณตรงนี้
```

### 4) ทดสอบว่าใช้งานได้

```bash
cd workshop1-agentic-ai
adk web
```

เปิด browser ไปที่ <http://localhost:8000> — ถ้าเห็นหน้า chat UI แสดงว่าพร้อมแล้ว! 🎉

## 🗺️ ภาพรวมของทั้งวัน

```
Workshop 1 (เช้า)                    Workshop 2 (บ่าย)
┌─────────────────────┐             ┌────────────────────────────────┐
│  Research Agent      │             │  Host Agent                    │
│  ┌───────────────┐   │             │   ├── MCP ──▶ Paper Server     │
│  │ tools ของเรา   │   │   ───────▶  │   │          (อีก process)      │
│  │ search_arxiv  │   │             │   └── A2A ──▶ Summarizer Agent │
│  │ save_note     │   │             │              (อีกเครื่องก็ได้!)   │
│  └───────────────┘   │             └────────────────────────────────┘
└─────────────────────┘
        ทั้งหมดดูผ่าน adk web — เห็นทุก step ที่ agent คิดและเรียก tool
```

## 🆘 แก้ปัญหาที่เจอบ่อย

| อาการ | วิธีแก้ |
|-------|--------|
| `adk: command not found` | ยังไม่ activate venv → `source .venv/bin/activate` |
| `API key not valid` | เช็คว่า copy key ครบ ไม่มีช่องว่างหน้า-หลัง |
| `429 RESOURCE_EXHAUSTED` | free tier ติด rate limit → รอ 1 นาทีแล้วลองใหม่ |
| Python 3.14 ใช้ไม่ได้ | ติดตั้ง Python 3.13: `brew install python@3.13` |
