"""Paper MCP Server 📚 — เครื่องมือค้น paper ที่ "ใครก็มาต่อใช้ได้"

MCP (Model Context Protocol) = มาตรฐานกลางสำหรับเสียบเครื่องมือให้ AI
เปรียบเหมือน USB-C: เขียน server ครั้งเดียว → Claude, Gemini, ADK, Cursor ใช้ได้หมด

ช่วงเช้า tools อยู่ "ใน" agent ของเรา
ช่วงบ่าย tools ย้ายมาอยู่ "นอก" agent — เป็น server แยกต่างหากตัวนี้
"""

import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

NOTES_FILE = Path(__file__).parent / "group_notes.txt"

mcp = FastMCP("paper-server")


@mcp.tool()
def search_papers(topic: str, max_results: int = 3) -> list[dict]:
    """ค้นหางานวิจัย (paper) จากเว็บ arXiv ตามหัวข้อที่สนใจ (ภาษาอังกฤษ)"""
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({
        "search_query": f"all:{topic}",
        "max_results": max_results,
        "sortBy": "relevance",
    })
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            xml_data = response.read()
    except Exception:
        return [{"title": f"[ข้อมูลสำรอง] A Survey on {topic}",
                 "summary": "ต่อ arXiv ไม่ได้ตอนนี้", "link": "https://arxiv.org"}]

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    for entry in ET.fromstring(xml_data).findall("atom:entry", ns):
        papers.append({
            "title": entry.find("atom:title", ns).text.strip(),
            "summary": entry.find("atom:summary", ns).text.strip()[:300],
            "link": entry.find("atom:id", ns).text.strip(),
        })
    return papers


@mcp.tool()
def save_note(text: str) -> str:
    """จดโน้ตของกลุ่มเก็บไว้ในไฟล์"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {text}\n")
    return f"จดโน้ตแล้ว: {text}"


@mcp.tool()
def read_notes() -> str:
    """อ่านโน้ตทั้งหมดของกลุ่มที่เคยจดไว้"""
    if not NOTES_FILE.exists():
        return "ยังไม่มีโน้ตเลย"
    return NOTES_FILE.read_text(encoding="utf-8")


if __name__ == "__main__":
    # สื่อสารผ่าน stdio — agent จะเป็นคน start process นี้ให้เอง
    mcp.run()
