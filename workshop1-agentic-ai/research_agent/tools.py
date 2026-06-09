"""เครื่องมือ (tools) ของ Research Buddy 🔧

tool = ฟังก์ชัน Python ธรรมดา ที่ agent "เลือกหยิบใช้เอง" ตามคำถามของผู้ใช้
สิ่งสำคัญที่สุดคือ docstring — agent อ่านมันเพื่อตัดสินใจว่าจะใช้ tool นี้เมื่อไหร่
"""

import io
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from pypdf import PdfReader

# ไฟล์เก็บโน้ตของเรา (อยู่ข้างๆ ไฟล์นี้)
NOTES_FILE = Path(__file__).parent / "my_notes.txt"


def search_arxiv(topic: str, max_results: int = 3) -> list[dict]:
    """ค้นหางานวิจัย (paper) จากเว็บ arXiv ตามหัวข้อที่สนใจ

    Args:
        topic: หัวข้อที่อยากค้นหา เป็นภาษาอังกฤษ เช่น "multi agent systems"
        max_results: จำนวน paper ที่ต้องการ (ค่าเริ่มต้น 3)

    Returns:
        รายการ paper แต่ละอันมี title, summary, link
    """
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({
        "search_query": f"all:{topic}",
        "max_results": max_results,
        "sortBy": "relevance",
    })
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            xml_data = response.read()
    except Exception:
        return _mock_papers(topic)  # เน็ตล่ม? ใช้ข้อมูลสำรองไปก่อน

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    for entry in ET.fromstring(xml_data).findall("atom:entry", ns):
        papers.append({
            "title": entry.find("atom:title", ns).text.strip(),
            "summary": entry.find("atom:summary", ns).text.strip()[:300],
            "link": entry.find("atom:id", ns).text.strip(),
        })
    return papers


def read_paper(pdf_url: str) -> str:
    """ดึงเนื้อหาจากไฟล์ PDF ของ paper เพื่อนำมาอ่านหรือสรุป

    Args:
        pdf_url: ลิงก์ของ paper เช่น "https://arxiv.org/abs/2304.03442"
            หรือลิงก์ไฟล์ .pdf ตรงๆ ก็ได้

    Returns:
        ข้อความในเนื้อหา paper (ถ้ายาวมากจะตัดมาเฉพาะช่วงต้น)
    """
    # ลิงก์ arXiv แบบหน้า abstract → แปลงเป็นลิงก์ PDF ให้เอง
    pdf_url = pdf_url.replace("arxiv.org/abs/", "arxiv.org/pdf/")

    request = urllib.request.Request(
        pdf_url, headers={"User-Agent": "research-buddy-workshop/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            pdf_data = response.read()
    except Exception as e:
        return f"ดาวน์โหลด PDF ไม่สำเร็จ: {e}"

    try:
        reader = PdfReader(io.BytesIO(pdf_data))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return f"อ่านเนื้อหา PDF ไม่สำเร็จ (อาจไม่ใช่ไฟล์ PDF): {e}"

    if not text.strip():
        return "PDF นี้ไม่มีข้อความให้อ่าน (อาจเป็นไฟล์สแกนรูปภาพ)"

    # กันเนื้อหายาวเกิน context — เอาช่วงต้น (intro/abstract อยู่ตรงนี้แหละ)
    max_chars = 20_000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n...(เนื้อหายาวเกิน ตัดมาเฉพาะช่วงต้น)..."
    return text


def save_note(text: str) -> str:
    """จดโน้ตเก็บไว้ในไฟล์ ใช้เมื่อผู้ใช้อยากบันทึกอะไรไว้กันลืม

    Args:
        text: ข้อความที่อยากจด

    Returns:
        ข้อความยืนยันว่าจดเรียบร้อยแล้ว
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {text}\n")
    return f"จดโน้ตแล้ว: {text}"


def read_notes() -> str:
    """อ่านโน้ตทั้งหมดที่เคยจดไว้ ใช้เมื่อผู้ใช้ถามว่าเคยจดอะไรไว้บ้าง

    Returns:
        โน้ตทั้งหมด หรือข้อความบอกว่ายังไม่มีโน้ต
    """
    if not NOTES_FILE.exists():
        return "ยังไม่มีโน้ตเลย"
    return NOTES_FILE.read_text(encoding="utf-8")


def _mock_papers(topic: str) -> list[dict]:
    """ข้อมูลสำรองกรณีต่อ arXiv ไม่ได้ (ขึ้นต้นด้วย _ คือไม่ใช่ tool)"""
    return [{
        "title": f"[ข้อมูลสำรอง] A Survey on {topic}",
        "summary": "ต่อ arXiv ไม่ได้ตอนนี้ — นี่คือข้อมูลตัวอย่างสำหรับทดสอบ",
        "link": "https://arxiv.org",
    }]
