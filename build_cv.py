#!/usr/bin/env python3
"""Build Shanker's CV PDF in the kaustubhsridhar.github.io/cv.pdf reference format."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = LETTER
ML, MR, MT, MB = 62, 62, 54, 54
BLUE = HexColor("#2e74b5")      # section titles + rules
LINK = HexColor("#2a7ae2")      # hyperlinks
GRAY = HexColor("#808080")
DARK = HexColor("#111111")
CONTENT_W = PAGE_W - ML - MR
DATE_X = ML
MAIN_X = ML + 92
RIGHT_X = PAGE_W - MR

st_name = ParagraphStyle("name", fontName="Helvetica", fontSize=27, leading=30, textColor=DARK)
st_sub = ParagraphStyle("sub", fontName="Helvetica-Oblique", fontSize=13, leading=16, textColor=GRAY)
st_contact = ParagraphStyle("contact", fontName="Helvetica", fontSize=9.5, leading=13, textColor=GRAY, alignment=2)
st_sec = ParagraphStyle("sec", fontName="Helvetica", fontSize=15.5, leading=18, textColor=BLUE)
st_body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=13.2, textColor=DARK)
st_bullet = ParagraphStyle("bullet", parent=st_body, leftIndent=14, firstLineIndent=0, spaceBefore=2.5,
                           bulletIndent=4)
st_date = ParagraphStyle("date", fontName="Helvetica", fontSize=10, leading=13.2, textColor=DARK)
st_right = ParagraphStyle("right", fontName="Helvetica-Oblique", fontSize=10, leading=13.2,
                          textColor=DARK, alignment=2)

c = canvas.Canvas("/home/hatch/workspace/github-site/cv.pdf", pagesize=LETTER)
c.setTitle("Shanker Valipireddy — CV")
c.setAuthor("Shanker Valipireddy")
y = PAGE_H - MT

def need(h):
    global y
    if y - h < MB:
        c.showPage()
        y = PAGE_H - MT

def draw_para(p, x, w):
    global y
    tw, th = p.wrap(w, 1000)
    need(th)
    p.drawOn(c, x, y - th)
    y -= th
    return th

def spacer(h=6):
    global y
    need(h)
    y -= h

# ---------- header ----------
name_p = Paragraph("Shanker Valipireddy", st_name)
tw, th = name_p.wrap(CONTENT_W * 0.62, 1000)
name_p.drawOn(c, ML, y - th)

contact_html = (
    '<font color="#808080">San Francisco Bay Area</font><br/>'
    '<font color="#808080">+1 832-589-3878</font><br/>'
    '<link href="mailto:shanker.valipireddyai@gmail.com" color="#2a7ae2">shanker.valipireddyai@gmail.com</link><br/>'
    '<link href="https://shankervalipireddyai.github.io" color="#2a7ae2">shankervalipireddyai.github.io</link>'
)
contact_p = Paragraph(contact_html, st_contact)
cw, chh = contact_p.wrap(CONTENT_W * 0.36, 1000)
contact_p.drawOn(c, PAGE_W - MR - cw, y - chh)
y -= max(th, chh) + 2
draw_para(Paragraph("Principal Architect / AI Enablement Lead @ Aflac", st_sub), ML, CONTENT_W)
spacer(10)

# ---------- helpers ----------
def section(title):
    global y
    need(34)
    spacer(4)
    c.setFillColor(BLUE)
    c.rect(ML, y - 5, 108, 4.2, stroke=0, fill=1)
    draw_para(Paragraph(title, st_sec), ML + 120, CONTENT_W - 120)
    spacer(7)

def entry(dates, main_html, right_html="", bullets=()):
    global y
    # measure main block height
    main_w = (RIGHT_X - MAIN_X - 8) - (150 if right_html else 0)
    protos = [Paragraph(main_html, st_body)]
    for b in bullets:
        protos.append(Paragraph(b, st_bullet, bulletText="\u2022"))
    total = sum(p.wrap(main_w, 1000)[1] for p in protos) + 8
    need(total)
    # dates (may be two lines)
    dp = Paragraph(dates.replace(" - ", "<br/>"), st_date)
    dw, dh = dp.wrap(88, 1000)
    dp.drawOn(c, DATE_X, y - dh)
    if right_html:
        rp = Paragraph(right_html, st_right)
        rw, rh = rp.wrap(150, 1000)
        rp.drawOn(c, RIGHT_X - rw, y - rh)
    yy = y
    for p in protos:
        tw, th = p.wrap(main_w, 1000)
        p.drawOn(c, MAIN_X, yy - th)
        yy -= th
    y = yy - 8

def simple_entry(dates, main_html, right_html=""):
    entry(dates, main_html, right_html, ())

# ---------- Education ----------
section("Education")
simple_entry("Jan 1999 - Jun 2003",
             "<b>B.Tech, Computer Science and Engineering</b>")

# ---------- Professional Summary (mirrors 'Research Interests') ----------
section("Professional Summary")
draw_para(Paragraph(
    "Principal Architect and applied-AI leader with 20+ years of experience taking AI systems "
    "from discovery through pilot, stabilization, and production rollout in enterprise environments. "
    "Currently <b>Principal Architect / AI Enablement Lead at Aflac</b>, driving enterprise GenAI and "
    "agentic AI adoption across 100+ engineering teams. Hands-on builder of multi-agent systems "
    "(LangGraph, CrewAI, MCP, LangChain), enterprise LLM evaluation and governance, and cloud-scale "
    "deployment on AWS, Azure, and GCP.", st_body), MAIN_X, RIGHT_X - MAIN_X - 8)
spacer(4)

# ---------- Work Experience ----------
section("Work Experience")

entry("Jan 2025 - Present",
      "<b>Aflac</b>, <i>Principal Architect / AI Enablement Lead — AI/ML, Agentic AI, GenAI</i>",
      "Georgia, USA",
      ("Spearheaded enterprise AI enablement: drove GenAI and agentic AI adoption across 100+ "
       "engineering teams via role-specific workshops and standardized \u2018AI Playbooks\u2019.",
       "Led migration of a legacy $3M/year ETL platform to cloud-native AWS (Airflow, Glue), using "
       "AI agents to refactor complex pipelines and modernize enterprise applications.",
       "Deployed an agentic code-generation pipeline (AWS Kiro agents) converting ~20k data pipelines "
       "across 82 business domains into Airflow DAGs and Glue jobs \u2014 99.3% QA pass rate.",
       "Implemented AI governance metrics (cycle time, defect-escape rates, token efficiency) and "
       "Human-in-the-Loop guardrails for production quality, security, and compliance."))

entry("Jan 2023 - Jan 2025",
      "<b>Brains Technology Solutions</b>, <i>Principal Architect \u2013 AI/ML, Agentic AI, GenAI</i>",
      "Michigan, USA",
      ("Designed multi-agent systems with LangGraph, CrewAI, MCP, and LangChain agents with LLM "
       "structured outputs for reasoning, tool use, and external interaction.",
       "Built Generative AI proof-of-concepts including regulatory text extraction (JPMC RCMA) on "
       "GCP/Vertex AI with GPT, Claude, Llama, and Mistral models.",
       "Established LLM fine-tuning and MLOps workflows (Llama 2/3.1, Mistral, Cohere, GPT-4) and "
       "transformer NLP (RoBERTa, DistilBERT) for text analytics and automation."))

entry("Jan 2016 - Jan 2023",
      "<b>Western Digital</b>, <i>Senior Principal / Technologist \u2013 AI/ML, Big Data</i>",
      "California, USA",
      ("Designed an AI/ML data platform on composable infrastructure and Kubernetes, delivered as "
       "on-demand SaaS for edge-to-cloud AI use cases (video analytics, threat intelligence).",
       "Delivered data-lakehouse components (MongoDB, Cassandra, Delta Lake), zoned-storage MySQL "
       "solutions, and smart archiving/analytics prototypes on OpenStack.",
       "Drove inference and data-pipeline performance optimization across GPUs, RDMA/RoCE, NVMe-oF, "
       "computational storage, and object storage."))

entry("Oct 2014 - Dec 2015",
      "<b>Cisco Systems, Inc.</b>, <i>Principal Architect \u2013 Big Data, AI/ML, NLP (Contract)</i>",
      "California, USA",
      ("Built deep-learning anomaly detection over network-device telemetry using pre-trained "
       "embeddings and clustering over log semantics and context.",
       "Integrated live devices for real-time detection with an operator dashboard and a human "
       "feedback loop for continuous model refinement."))

entry("Oct 2010 - Oct 2014",
      "<b>Franklin Templeton</b>, <i>Sr. Java Developer</i>",
      "California, USA",
      ("Built Hadoop/HBase ETL and MapReduce analytics; Hive/Pig reporting and Oracle integration "
       "via Sqoop; Twitter sentiment analysis served through the HBase REST API.",))

entry("Jun 2003 - Oct 2010",
      "<b>IBM, Wipro &amp; CF India</b>, <i>Java Engineer</i>",
      "Dublin, CA, USA",
      ("Enterprise application integration (Java/Spring, TIBCO); proof-of-concept design and "
       "development.",))

# ---------- Patents ----------
section("Patents")
draw_para(Paragraph(
    "<b>Method and Apparatus for Smart Archiving and Analytics</b> \u2014 US 10,360,193, "
    "issued July 23, 2019.", st_body), MAIN_X, RIGHT_X - MAIN_X - 8)
spacer(3)
draw_para(Paragraph(
    "<b>Intelligent Data Access Across Tiered Storage Systems</b> \u2014 US 11,544,216, "
    "issued January 3, 2023.", st_body), MAIN_X, RIGHT_X - MAIN_X - 8)
spacer(2)

# ---------- Publications & Conference Talks ----------
section("Publications &amp; Conference Talks")
pubs = [
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
]
for title, venue in pubs:
    draw_para(Paragraph(f"<b>{title}.</b> <i>{venue}.</i>", st_body),
              MAIN_X, RIGHT_X - MAIN_X - 8)
    spacer(3)

# ---------- Certifications ----------
section("Certifications")
draw_para(Paragraph(
    "AWS Certified Machine Learning \u2014 Specialty; Microsoft Azure AI Engineer (AZ-102); "
    "Generative AI with Large Language Models; Machine Learning, NLP, and Deep Learning "
    "specializations; Transformer Models and BERT; LLMs: Application through Production; Building "
    "Conversational AI Applications (NVIDIA); Responsible AI; AI in the Data Center (NVIDIA); "
    "Apache Cassandra Certified Developer; MongoDB Certified Developer; Spark ML; Big Data XSeries "
    "(UC BerkeleyX); Advanced Predictive Analytics using R (IIT Hyderabad); PMP Training.",
    st_body), MAIN_X, RIGHT_X - MAIN_X - 8)
spacer(4)

# ---------- Awards ----------
section("Awards")
draw_para(Paragraph("<b>IBM Bravo Award.</b>", st_body), MAIN_X, RIGHT_X - MAIN_X - 8)
spacer(3)
draw_para(Paragraph("<b>Best Employee Award.</b>", st_body), MAIN_X, RIGHT_X - MAIN_X - 8)

c.showPage()
c.save()
print("cv.pdf written")
