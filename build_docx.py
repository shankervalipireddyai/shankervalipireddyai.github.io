#!/usr/bin/env python3
"""Build Shanker's CV DOCX in the kaustubhsridhar.github.io/cv.pdf reference format."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BLUE = RGBColor(0x2E, 0x74, 0xB5)
LINK = RGBColor(0x2A, 0x7A, 0xE2)
GRAY = RGBColor(0x80, 0x80, 0x80)
DARK = RGBColor(0x11, 0x11, 0x11)

doc = Document()
for s in doc.sections:
    s.left_margin = Inches(0.85)
    s.right_margin = Inches(0.85)
    s.top_margin = Inches(0.7)
    s.bottom_margin = Inches(0.7)

style = doc.styles["Normal"]
style.font.name = "Helvetica"
style.font.size = Pt(10)
style.font.color.rgb = DARK
style.paragraph_format.space_after = Pt(2)

def para(text="", size=10, bold=False, italic=False, color=DARK, align=None,
         space_after=2, space_before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    r.font.name = "Helvetica"
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    r.font.color.rgb = color
    return p

def rich_para(segments, align=None, space_after=2, left_indent=None, bullet=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    if left_indent is not None:
        p.paragraph_format.left_indent = Inches(left_indent)
    if bullet:
        p.style = "List Bullet"
    for text, kw in segments:
        r = p.add_run(text)
        r.font.name = "Helvetica"
        r.font.size = Pt(kw.get("size", 10))
        r.bold = kw.get("bold", False)
        r.italic = kw.get("italic", False)
        if "color" in kw:
            r.font.color.rgb = kw["color"]
    return p

def hyperlink(p, url, text):
    part = p.part
    r_id = part.relate_to(url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    hl = OxmlElement("w:hyperlink")
    hl.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rF = OxmlElement("w:rFonts"); rF.set(qn("w:ascii"), "Helvetica"); rF.set(qn("w:hAnsi"), "Helvetica")
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "19")
    color = OxmlElement("w:color"); color.set(qn("w:val"), "2A7AE2")
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single")
    rPr.append(rF); rPr.append(sz); rPr.append(color); rPr.append(u)
    run.append(rPr)
    t = OxmlElement("w:t"); t.text = text
    run.append(t)
    hl.append(run)
    p._p.append(hl)

def section(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(title)
    r.font.name = "Helvetica"
    r.font.size = Pt(15.5)
    r.bold = False
    r.font.color.rgb = BLUE
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "18")
    bottom.set(qn("w:space"), "1"); bottom.set(qn("w:color"), "2E74B5")
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p

def entry(dates, company, title, location, bullets):
    t = doc.add_table(rows=1, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    t.columns[0].width = Inches(1.25)
    t.columns[1].width = Inches(4.1)
    t.columns[2].width = Inches(1.45)
    c0, c1, c2 = t.rows[0].cells
    for c in (c0, c1, c2):
        c.vertical_alignment = 1
        for par in c.paragraphs:
            par.paragraph_format.space_after = Pt(0)
    r = c0.paragraphs[0].add_run(dates)
    r.font.name = "Helvetica"; r.font.size = Pt(10)
    r = c1.paragraphs[0].add_run(company)
    r.font.name = "Helvetica"; r.font.size = Pt(10); r.bold = True
    r = c1.paragraphs[0].add_run("  " + title)
    r.font.name = "Helvetica"; r.font.size = Pt(10); r.italic = True
    r = c2.paragraphs[0].add_run(location)
    r.font.name = "Helvetica"; r.font.size = Pt(10); r.italic = True
    c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for b in bullets:
        rich_para([(b, {})], left_indent=1.35, bullet=True, space_after=1)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ---------- header ----------
ht = doc.add_table(rows=1, cols=2)
ht.alignment = WD_TABLE_ALIGNMENT.CENTER
ht.autofit = False
ht.columns[0].width = Inches(4.4)
ht.columns[1].width = Inches(2.4)
name_c, contact_c = ht.rows[0].cells
for c in (name_c, contact_c):
    for par in c.paragraphs:
        par.paragraph_format.space_after = Pt(0)
r = name_c.paragraphs[0].add_run("Shanker Valipireddy")
r.font.name = "Helvetica"; r.font.size = Pt(27); r.font.color.rgb = DARK
cp = contact_c.paragraphs[0]
cp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
for text, is_link, url in [
    ("San Francisco Bay Area", False, ""),
    ("+1 832-589-3878", False, ""),
    ("shanker.valipireddyai@gmail.com", True, "mailto:shanker.valipireddyai@gmail.com"),
    ("shankervalipireddyai.github.io", True, "https://shankervalipireddyai.github.io"),
]:
    if text != "San Francisco Bay Area":
        cp.add_run().add_break()
    if is_link:
        hyperlink(cp, url, text)
    else:
        run = cp.add_run(text)
        run.font.name = "Helvetica"; run.font.size = Pt(9.5)
        run.font.color.rgb = GRAY

para("Principal Architect / AI Enablement Lead @ Aflac", size=13, italic=True,
     color=GRAY, space_before=4, space_after=6)

# ---------- Education ----------
section("Education")
entry("Jan 1999 -\nJun 2003", "B.Tech, Computer Science and Engineering", "", "", [])

# ---------- Professional Summary ----------
section("Professional Summary")
rich_para([
    ("Principal Architect and applied-AI leader with 20+ years of experience taking AI systems "
     "from discovery through pilot, stabilization, and production rollout in enterprise environments. "
     "Currently ", {}),
    ("Principal Architect / AI Enablement Lead at Aflac", {"bold": True}),
    (", driving enterprise GenAI and agentic AI adoption across 100+ engineering teams. Hands-on "
     "builder of multi-agent systems (LangGraph, CrewAI, MCP, LangChain), enterprise LLM evaluation "
     "and governance, and cloud-scale deployment on AWS, Azure, and GCP.", {}),
], space_after=2)

# ---------- Work Experience ----------
section("Work Experience")
entry("Jan 2025 -\nPresent", "Aflac",
      "Principal Architect / AI Enablement Lead \u2014 AI/ML, Agentic AI, GenAI",
      "Georgia, USA", [
    "Spearheaded enterprise AI enablement: drove GenAI and agentic AI adoption across 100+ engineering teams via role-specific workshops and standardized \u2018AI Playbooks\u2019.",
    "Led migration of a legacy $3M/year ETL platform to cloud-native AWS (Airflow, Glue), using AI agents to refactor complex pipelines and modernize enterprise applications.",
    "Deployed an agentic code-generation pipeline (AWS Kiro agents) converting ~20k data pipelines across 82 business domains into Airflow DAGs and Glue jobs \u2014 99.3% QA pass rate.",
    "Implemented AI governance metrics (cycle time, defect-escape rates, token efficiency) and Human-in-the-Loop guardrails for production quality, security, and compliance.",
])
entry("Jan 2023 -\nJan 2025", "Brains Technology Solutions",
      "Principal Architect \u2013 AI/ML, Agentic AI, GenAI",
      "Michigan, USA", [
    "Designed multi-agent systems with LangGraph, CrewAI, MCP, and LangChain agents with LLM structured outputs for reasoning, tool use, and external interaction.",
    "Built Generative AI proof-of-concepts including regulatory text extraction (JPMC RCMA) on GCP/Vertex AI with GPT, Claude, Llama, and Mistral models.",
    "Established LLM fine-tuning and MLOps workflows (Llama 2/3.1, Mistral, Cohere, GPT-4) and transformer NLP (RoBERTa, DistilBERT) for text analytics and automation.",
])
entry("Jan 2016 -\nJan 2023", "Western Digital",
      "Senior Principal / Technologist \u2013 AI/ML, Big Data",
      "California, USA", [
    "Designed an AI/ML data platform on composable infrastructure and Kubernetes, delivered as on-demand SaaS for edge-to-cloud AI use cases (video analytics, threat intelligence).",
    "Delivered data-lakehouse components (MongoDB, Cassandra, Delta Lake), zoned-storage MySQL solutions, and smart archiving/analytics prototypes on OpenStack.",
    "Drove inference and data-pipeline performance optimization across GPUs, RDMA/RoCE, NVMe-oF, computational storage, and object storage.",
])
entry("Oct 2014 -\nDec 2015", "Cisco Systems, Inc.",
      "Principal Architect \u2013 Big Data, AI/ML, NLP (Contract)",
      "California, USA", [
    "Built deep-learning anomaly detection over network-device telemetry using pre-trained embeddings and clustering over log semantics and context.",
    "Integrated live devices for real-time detection with an operator dashboard and a human feedback loop for continuous model refinement.",
])
entry("Oct 2010 -\nOct 2014", "Franklin Templeton",
      "Sr. Java Developer",
      "California, USA", [
    "Built Hadoop/HBase ETL and MapReduce analytics; Hive/Pig reporting and Oracle integration via Sqoop; Twitter sentiment analysis served through the HBase REST API.",
])
entry("Jun 2003 -\nOct 2010", "IBM, Wipro & CF India",
      "Java Engineer",
      "Dublin, CA, USA", [
    "Enterprise application integration (Java/Spring, TIBCO); proof-of-concept design and development.",
])

# ---------- Patents ----------
section("Patents")
rich_para([
    ("Method and Apparatus for Smart Archiving and Analytics", {"bold": True}),
    (" \u2014 US 10,360,193, issued July 23, 2019.", {}),
], space_after=2)
rich_para([
    ("Intelligent Data Access Across Tiered Storage Systems", {"bold": True}),
    (" \u2014 US 11,544,216, issued January 3, 2023.", {}),
], space_after=2)

# ---------- Publications ----------
section("Publications & Conference Talks")
for title, venue in [
    ("Enabling an Optimal Application Ecosystem on ZNS Storage",
     "Flash Memory Summit, Santa Clara, CA, August 2022"),
    ("An Artificial Intelligence Data Pipeline for Storing and Processing Ingested Data",
     "Flash Memory Summit, Santa Clara, CA, 2019"),
    ("Flash Storage Complementing a Data Lake for Real-time Insight",
     "Flash Memory Summit, Santa Clara, CA, 2018"),
    ("An Analytics System on OpenStack for Manufacturing",
     "Western Digital corporate white paper, 2018"),
    ("An Analytics System for Optimizing Manufacturing Processes",
     "Western Digital corporate white paper, 2018"),
    ("Use Cases for ActiveScale Data Pipeline Service",
     "Western Digital corporate white paper, 2019"),
    ("ActiveScale Data Pipeline Service with Elasticsearch \u2014 Best Practices for Metadata Indexing and Search",
     "Western Digital corporate white paper, 2019"),
    ("AI Solution \u2014 Object Storage Content Analysis",
     "Corporate presentation, Western Digital, 2018"),
    ("AI/ML MLPerf/TensorFlow/PyTorch Performance Benchmark \u2014 Image Detection",
     "Corporate presentation, Western Digital, 2018"),
    ("AI/ML/Deep Learning (TensorFlow/Keras) for Analyzing Fraud Detection",
     "Presentation, 2019"),
]:
    rich_para([(title + ".", {"bold": True}), (" " + venue + ".", {"italic": True})],
              space_after=2)

# ---------- Certifications ----------
section("Certifications")
rich_para([(
    "AWS Certified Machine Learning \u2014 Specialty; Microsoft Azure AI Engineer (AZ-102); "
    "Generative AI with Large Language Models; Machine Learning, NLP, and Deep Learning "
    "specializations; Transformer Models and BERT; LLMs: Application through Production; Building "
    "Conversational AI Applications (NVIDIA); Responsible AI; AI in the Data Center (NVIDIA); "
    "Apache Cassandra Certified Developer; MongoDB Certified Developer; Spark ML; Big Data XSeries "
    "(UC BerkeleyX); Advanced Predictive Analytics using R (IIT Hyderabad); PMP Training.", {}),
], space_after=2)

# ---------- Awards ----------
section("Awards")
rich_para([("IBM Bravo Award.", {"bold": True})], space_after=2)
rich_para([("Best Employee Award.", {"bold": True})], space_after=2)

doc.save("/home/hatch/workspace/github-site/Shanker_Valipireddy_CV.docx")
print("docx written")
