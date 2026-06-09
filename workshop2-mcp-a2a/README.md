# 🔌 Workshop 2: MCP & A2A — ต่อ Agent เข้ากับโลกภายนอก

**เวลา 14:15 – 15:15** | เอา Research Buddy จากช่วงเช้ามา "ต่อปลั๊ก" กับ MCP server และ "คุยกับ agent ของเพื่อน" ผ่าน A2A

## ภาพรวม

```
         ┌─────────────┐   MCP    ┌──────────────────┐
 เรา ──▶ │ Host Agent  │ ───────▶ │ Paper MCP Server │  ← tools ย้ายมาอยู่นี่แล้ว
         │  (adk web)  │  stdio   │  (paper_mcp.py)  │
         │             │          └──────────────────┘
         │             │   A2A    ┌──────────────────┐
         │             │ ───────▶ │ Summarizer Agent │  ← agent อีกตัว
         └─────────────┘  HTTP    │   (port 8001)    │     อีกเครื่องก็ได้!
                                  └──────────────────┘
```

| Protocol | เปรียบเหมือน | ใช้ทำอะไร |
|----------|--------------|-----------|
| **MCP** (Model Context Protocol) | USB-C ของ AI | เสียบ "เครื่องมือ" ให้ agent ใช้ — เขียน server เดียว ใช้ได้กับทุก AI |
| **A2A** (Agent2Agent) | นามบัตร + โทรศัพท์ | ให้ "agent คุยกับ agent" ข้าม process ข้ามเครื่อง ข้ามองค์กร |

> จำง่ายๆ: **MCP = agent ↔ เครื่องมือ** ส่วน **A2A = agent ↔ agent**

## เตรียมตัว (5 นาที)

copy `.env` จากช่วงเช้ามาใส่ทั้ง 2 agent:

```bash
cd workshop2-mcp-a2a
cp ../workshop1-agentic-ai/research_agent/.env host_agent/.env
cp ../workshop1-agentic-ai/research_agent/.env summarizer_agent/.env
```

## 🔧 Step 1 — MCP: tools ย้ายออกไปนอก agent (15 นาที)

ช่วงเช้า tools เป็น function **ใน code ของ agent** — ช่วงบ่ายมันย้ายไปอยู่ **server แยกต่างหาก** (`mcp_server/paper_mcp.py`)

เปิดดู 2 ไฟล์เทียบกัน:
- `mcp_server/paper_mcp.py` — tools เดิมจากช่วงเช้า แต่ห่อด้วย `@mcp.tool()`
- `host_agent/agent.py` — ไม่มี code ของ tool เลย! มีแค่ `McpToolset` ชี้ไปที่ server

รัน:

```bash
adk web
```

เลือก `host_agent` แล้วลอง:

> หา paper เรื่อง "agent communication protocol" หน่อย

**สิ่งที่ต้องดู 👀:** agent ใช้ tool `search_papers` ได้ ทั้งที่ code ของ tool ไม่ได้อยู่ในตัวมัน —
มันถูกส่งมาจาก MCP server ที่เป็นอีก process หนึ่ง (ลองดูใน trace)

💡 server แบบเดียวกันนี้ ถ้าเอาไปเสียบ Claude Desktop หรือ Cursor ก็ใช้ได้ทันที — นี่คือพลังของ "มาตรฐานกลาง"

## 🌐 Step 2 — A2A: agent คุยกับ agent (25 นาที)

### 2.1 เปิด Summarizer Agent เป็น A2A server (terminal ใหม่)

```bash
cd workshop2-mcp-a2a
source ../.venv/bin/activate
uvicorn summarizer_agent.a2a_server:app --host 0.0.0.0 --port 8001
```

เปิดดู **นามบัตร (Agent Card)** ของมัน: <http://localhost:8001/.well-known/agent-card.json>
— นี่คือสิ่งที่ agent อื่นอ่านเพื่อรู้ว่า agent ตัวนี้ทำอะไรได้

### 2.2 ให้ Host Agent ส่งงานต่อ

กลับมาที่ adk web (host_agent) แล้วลอง:

> หา paper เรื่อง "large language model agents" แล้วส่งให้ผู้เชี่ยวชาญช่วยสรุปหน่อย

**สิ่งที่ต้องดู 👀:** ใน trace จะเห็น host agent **transfer งาน** ไปให้ `summarizer_agent`
ซึ่งวิ่งอยู่คนละ process ผ่าน HTTP — และใน terminal ของ uvicorn จะเห็น request วิ่งเข้ามาจริง

### 2.3 🔥 ไฮไลท์: เรียก agent ของเพื่อน (ข้ามเครื่องจริงๆ)

จับคู่กับเพื่อน (ต้องอยู่ Wi-Fi วงเดียวกัน):

**เพื่อน (ฝั่งเปิด server):** หา IP ตัวเองแล้วเปิด server ใหม่

```bash
ipconfig getifaddr en0        # Mac — สมมติได้ 192.168.1.42 (Windows: ipconfig)
A2A_HOST=192.168.1.42 uvicorn summarizer_agent.a2a_server:app --host 0.0.0.0 --port 8001
```

**เรา (ฝั่งเรียก):** ปิด adk web เดิม แล้วเปิดใหม่โดยชี้ไปเครื่องเพื่อน

```bash
SUMMARIZER_URL=http://192.168.1.42:8001 adk web
```

ลองสั่งสรุป paper อีกครั้ง — งานจะวิ่งไปประมวลผลบน **เครื่องของเพื่อน** 🤝
(เพื่อนจะเห็น log วิ่งใน terminal ของตัวเอง)

## 🎤 Step 3 — โจทย์กลุ่ม เตรียม present (20 นาที)

แต่ละกลุ่มแก้ `summarizer_agent/agent.py` (ตรง `instruction`) ให้กลายเป็น **specialist ประจำกลุ่ม** เช่น:

- 🌏 นักแปลศัพท์เทคนิคเป็นภาษาบ้านๆ
- 🔍 นักวิจารณ์ระเบียบวิธีวิจัย (ชี้จุดอ่อนของ paper)
- 💡 นักตั้งคำถามต่อยอด (อ่านแล้วเสนอหัวข้อวิจัยใหม่)
- 🎭 อะไรก็ได้ที่กลุ่มคิดเอง!

แล้ว present (15:15): ตั้งชื่อ agent, demo การเรียกข้ามเครื่อง, เล่าว่าถ้ามีเวลาต่อจะพัฒนาอะไรเพิ่ม

## 📌 สรุปสิ่งที่ได้เรียนรู้

| แนวคิด | เห็นได้จาก |
|--------|-----------|
| MCP = มาตรฐานเสียบ tools (agent ↔ เครื่องมือ) | `McpToolset` ใน `host_agent/agent.py` |
| A2A = มาตรฐาน agent คุยกัน (agent ↔ agent) | `RemoteA2aAgent` + Agent Card |
| Agent Card = นามบัตรของ agent | `/.well-known/agent-card.json` |
| ระบบ multi-agent ข้ามเครื่อง/องค์กร ทำได้จริง | เรียก agent เครื่องเพื่อน |
