# 🏢 Project 3: AI Accounting Office — บริษัทจำลองที่พนักงานเป็น Agent ทั้งหมด

โปรเจกต์รวมยอด **Multi-Agent + MCP + A2A** ในเรื่องเดียว: บริษัท "AGI Cafe Co., Ltd."
มี CEO เป็น orchestrator และพนักงาน 2 คนเป็น A2A agent ที่ถือเครื่องมือ MCP คนละชุด

```
                      ┌─────────────┐
              เรา ──▶ │  CEO Agent  │  (adk web — ไม่มี tool เลย!)
                      └──────┬──────┘
              A2A ┌──────────┼──────────┐ A2A
                  ▼          ▼          ▼
        ┌────────────┐ ┌────────────┐ ┌─────────────┐
        │ Analyst 📊 │ │Accountant🧮│ │ Finance 💰  │
        │ (:8003)    │ │ (:8002)    │ │ CFO (:8004) │
        └─────┬──────┘ └─────┬──────┘ └──────┬──────┘
          MCP │          MCP │           A2A │ ถามนักบัญชี
              ▼              ▼               │ (AgentTool)
        ┌────────────┐ ┌────────────┐        │
        │ set-mcp    │ │invoice_mcp │ ◀──────┘
        │ งบหุ้น SET  │ │ บิลPDF/บัญชี│
        │(community!)│ │(เราเขียนเอง)│
        └────────────┘ └────────────┘
```

| พนักงาน | หน้าที่ | จุดสอน |
|---------|--------|--------|
| Analyst 📊 | เช็คเครดิตบริษัท "ลูกค้า" จากงบหุ้น SET | ใช้ MCP server ของ community |
| Accountant 🧮 | ออกบิล PDF + ลงบัญชี + สรุปยอด | ใช้ MCP server ที่เราเขียนเอง |
| Finance (CFO) 💰 | วิเคราะห์การเงิน "บริษัทเรา" + ให้คำแนะนำ | **agent คุยกับ agent**: ไม่แตะบัญชีเอง แต่ถามนักบัญชีผ่าน A2A (AgentTool) แล้ววิเคราะห์ต่อ |

**Use case ต่อกันครบ loop ธุรกิจ:**

1. ลูกค้าใหม่เป็นบริษัทในตลาดหุ้น → CEO ส่งให้ **Analyst เช็คเครดิต** (ดึงงบจริงจาก SET)
2. ฐานะโอเค → ตกลงรับงาน
3. CEO สั่ง **Accountant ออกใบแจ้งหนี้** (VAT 7%) + ลงบัญชีรายรับ
4. สิ้นเดือนถาม **กำไร/ขาดทุน**

จุดเด่นที่ใช้สอน: `set-mcp` คือ MCP server **ของคนอื่นจาก community** (`pip install set-mcp`)
— เราไม่ได้เขียนสักบรรทัด แต่ agent ใช้ได้เลย นี่คือพลังของมาตรฐานกลาง

## วิธีรัน (ใช้ 4 terminals)

ทุก terminal ต้อง activate venv ก่อน: `source ../.venv/bin/activate`
และต้องมีไฟล์ `.env` (มี `GOOGLE_API_KEY`) ใน agent ทุกโฟลเดอร์

**Terminal 1 — นักบัญชี (ต้องเปิดก่อน CFO):**

```bash
cd project3-accounting-office
uvicorn accountant_agent.a2a_server:app --host 0.0.0.0 --port 8002
```

**Terminal 2 — นักวิเคราะห์:**

```bash
cd project3-accounting-office
uvicorn analyst_agent.a2a_server:app --host 0.0.0.0 --port 8003
```

**Terminal 3 — CFO (เปิดหลังนักบัญชี):**

```bash
cd project3-accounting-office
uvicorn finance_agent.a2a_server:app --host 0.0.0.0 --port 8004
```

**Terminal 4 — CEO (UI):**

```bash
cd project3-accounting-office
adk web
```

เปิด <http://localhost:8000> เลือก `ceo_agent`

## บทพูดสำหรับ demo (ลองตามลำดับ)

> ลูกค้าใหม่คือ CPALL อยากจ้างเราทำการตลาด ช่วยเช็คหน่อยว่าฐานะการเงินเขาโอเคไหม

> โอเค รับงานนี้ ออกใบแจ้งหนี้ค่าที่ปรึกษาการตลาด 50,000 บาทให้ CPALL แล้วลงบัญชีรายรับด้วย

> เดือนนี้บริษัทเรากำไรเท่าไหร่แล้ว?

> ช่วยวิเคราะห์การเงินบริษัทเราหน่อย มีอะไรต้องระวังไหม

ข้อสุดท้าย CEO จะส่งให้ **CFO** — แล้ว CFO จะไป "คุยกับนักบัญชี" ขอตัวเลขมาเอง (ดูใน terminal ของนักบัญชีจะเห็น request จาก CFO วิ่งเข้า) ก่อนวิเคราะห์อัตรากำไรและให้คำแนะนำ

**สิ่งที่ต้องดู 👀:**
- trace ใน adk web: CEO ไม่เรียก tool เอง แต่ `transfer_to_agent` ไปหาลูกน้อง
- terminal ของ accountant/analyst: เห็น request วิ่งเข้า (งานไปทำที่ process อื่นจริง)
- ไฟล์จริงเกิดขึ้น: **ใบแจ้งหนี้ PDF** `mcp_server/invoices/INV-0001.pdf` (เปิดโชว์บนจอได้เลย — หัวบริษัท ตาราง VAT ครบ) พร้อม `.txt` และ `mcp_server/ledger.csv`

## เรียกข้ามเครื่อง (ทีมละเครื่อง)

เครื่องเพื่อนเปิดนักบัญชี: `A2A_HOST=<ip เพื่อน> uvicorn accountant_agent.a2a_server:app --host 0.0.0.0 --port 8002`

เครื่องเราชี้ไปหา:

```bash
ACCOUNTANT_URL=http://<ip เพื่อน>:8002 adk web
```

## ไอเดียต่อยอด (โจทย์กลุ่ม)

- เพิ่ม **HR Agent** ที่มี tool คำนวณเงินเดือน/ภาษีหัก ณ ที่จ่าย
- เพิ่ม tool `list_invoices()` ให้นักบัญชีค้นบิลเก่า
- ให้ Analyst เปรียบเทียบงบ 2 บริษัทแล้วแนะนำว่าควรรับลูกค้ารายไหนก่อน
- ให้ CFO เปรียบเทียบกำไรบริษัทเรากับบริษัทในตลาดหุ้น (CFO คุยกับ Analyst!)
