"""
OWLET-AI Performance Evaluation Report
RCEL 506 — Mohammed Farran — April 2026
Generated using Python + ReportLab
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import io

W, H = letter  # 612 x 792

# ── Color palette ─────────────────────────────────────────────────────────────
BG       = colors.HexColor('#0D0D0D')
CARD     = colors.HexColor('#1C1C1C')
ACCENT   = colors.HexColor('#C8F542')
ACCENT2  = colors.HexColor('#4A9FD5')
RED      = colors.HexColor('#E05252')
WHITE    = colors.white
MUTED    = colors.HexColor('#9E9E9E')
DARK2    = colors.HexColor('#141414')

# ── Data ──────────────────────────────────────────────────────────────────────
G_AVG = 42
A_AVG = 33
C_AVG = 25

incidents = [
    ("1", "Primary data source returned empty values. Switched to UN Comtrade mirror data approach.", 70, 10, 20),
    ("2", "Rebuilt pipeline after original data source failed. Confirmed correct HS Chapter and coverage.", 50, 20, 30),
    ("3", "Data only captured part of the picture. Reframed scope to address coverage limitations.", 30, 60, 10),
    ("4", "Fixed output error in monthly data calculation producing unrealistic values.", 10, 80, 10),
    ("5", "Identified and corrected wrong value in one period that did not match historical data.", 60, 30, 10),
    ("6", "Dataset was mixing value types across periods. Standardized everything before modeling.", 40, 20, 40),
    ("7", "Data frequency insufficient for model requirements. Switched to higher frequency source.", 50, 40, 10),
    ("8", "Data too noisy to model directly. Applied smoothing and justified the choice.", 80, 10, 10),
    ("9", "Conclusions exceeded what data could support. Pulled back scope to match actual findings.", 10, 10, 80),
    ("10","OWLET drifted from project objective in later sessions. Re-explained real goal.", 20, 50, 30),
]

# ── Generate ternary plot ─────────────────────────────────────────────────────
def make_ternary_plot():
    fig, ax = plt.subplots(figsize=(3.2, 2.8), facecolor='#0D0D0D')
    ax.set_facecolor('#141414')
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw triangle
    verts = np.array([[0,0],[1,0],[0.5, np.sqrt(3)/2]])
    triangle = plt.Polygon(verts, fill=True, facecolor='#1A2A3A', edgecolor='#4A9FD5', linewidth=1.5)
    ax.add_patch(triangle)

    # Grid lines
    for i in [0.2, 0.4, 0.6, 0.8]:
        for j in range(3):
            p1 = (1-i)*verts[j] + i*verts[(j+1)%3]
            p2 = (1-i)*verts[j] + i*verts[(j+2)%3]
            ax.plot([p1[0],p2[0]],[p1[1],p2[1]], color='#2A3A4A', linewidth=0.5, alpha=0.6)

    # Convert GAC to cartesian
    g, a, c = G_AVG/100, A_AVG/100, C_AVG/100
    x = a * verts[1][0] + c * verts[2][0] + g * verts[0][0]
    y = a * verts[1][1] + c * verts[2][1] + g * verts[0][1]

    # Plot dot
    ax.plot(x, y, 'o', color='#E05252', markersize=10, zorder=5)
    ax.plot(x, y, 'o', color='#FF8888', markersize=5, zorder=6)

    # Labels
    ax.text(verts[0][0]-0.12, verts[0][1]-0.04, f'Governance\n(G={G_AVG}%)',
            color='#C8F542', fontsize=7, ha='center', fontweight='bold')
    ax.text(verts[1][0]+0.05, verts[1][1]-0.04, f'Audit\n(A={A_AVG}%)',
            color='#4A9FD5', fontsize=7, ha='center', fontweight='bold')
    ax.text(verts[2][0], verts[2][1]+0.04, f'Context\n(C={C_AVG}%)',
            color='#9E9E9E', fontsize=7, ha='center', fontweight='bold')

    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-0.1, 1.0)
    plt.tight_layout(pad=0.1)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor='#0D0D0D', edgecolor='none')
    plt.close()
    buf.seek(0)
    return buf

# ── Generate bar chart ────────────────────────────────────────────────────────
def make_bar_chart():
    fig, ax = plt.subplots(figsize=(3.2, 2.4), facecolor='#0D0D0D')
    ax.set_facecolor('#141414')

    categories = ['Governance\n(Domain Fix)', 'Audit\n(Hallucination)', 'Context\n(Decay Fix)']
    values = [G_AVG, A_AVG, C_AVG]
    bar_colors = ['#C8F542', '#4A9FD5', '#9E9E9E']

    bars = ax.bar(categories, values, color=bar_colors, alpha=0.85,
                  edgecolor='#2A2A2A', linewidth=0.5, width=0.55)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val}%', ha='center', va='bottom', color='white',
                fontsize=9, fontweight='bold')

    ax.set_ylim(0, 55)
    ax.set_ylabel('Energy Allocation (%)', color='#9E9E9E', fontsize=8)
    ax.tick_params(colors='#9E9E9E', labelsize=8)
    ax.spines['bottom'].set_color('#333333')
    ax.spines['left'].set_color('#333333')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_facecolor('#141414')
    ax.yaxis.label.set_color('#9E9E9E')
    for label in ax.get_xticklabels():
        label.set_color('#9E9E9E')

    plt.tight_layout(pad=0.3)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor='#0D0D0D', edgecolor='none')
    plt.close()
    buf.seek(0)
    return buf

# ── Build PDF ─────────────────────────────────────────────────────────────────
c = canvas.Canvas("/home/claude/OWLET_Performance_Report.pdf", pagesize=letter)
c.setTitle("OWLET-AI Performance Evaluation — Mohammed Farran")

# Background
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Top accent bar
c.setFillColor(ACCENT)
c.rect(0, H-4, W, 4, fill=1, stroke=0)

# Left accent bar
c.setFillColor(ACCENT)
c.rect(0, 0, 4, H, fill=1, stroke=0)

# ── HEADER ────────────────────────────────────────────────────────────────────
c.setFillColor(DARK2)
c.rect(4, H-70, W-4, 66, fill=1, stroke=0)

c.setFont("Helvetica-Bold", 16)
c.setFillColor(WHITE)
c.drawString(20, H-32, "O.W.L.E.T.-AI  |  Job Performance Evaluation")

c.setFont("Helvetica", 9)
c.setFillColor(ACCENT)
c.drawString(20, H-48, "AI Junior Assistant Audit  —  RCEL 506 Final Project  —  Saudi Arabia Defense Localization")

c.setFont("Helvetica", 8)
c.setFillColor(MUTED)
c.drawString(20, H-62, "Mohammed Farran  |  Rice University  |  April 2026")

# Hiring decision badge
c.setFillColor(RED)
c.roundRect(W-140, H-60, 120, 24, 4, fill=1, stroke=0)
c.setFont("Helvetica-Bold", 9)
c.setFillColor(WHITE)
c.drawCentredString(W-80, H-44, "DECISION: TERMINATE")

# ── SECTION 1: METRICS ROW ────────────────────────────────────────────────────
y_metrics = H - 100
metric_data = [
    ("42%", "Governance", "Domain & SOP corrections", ACCENT),
    ("33%", "Audit", "Hallucination catches", ACCENT2),
    ("25%", "Context", "Context decay fixes", MUTED),
    ("10", "Incidents", "Critical interventions", colors.HexColor('#E08020')),
]

box_w = (W - 24) / 4
for i, (val, label, sub, col) in enumerate(metric_data):
    bx = 4 + i * box_w
    c.setFillColor(CARD)
    c.rect(bx + 2, y_metrics - 52, box_w - 4, 50, fill=1, stroke=0)
    c.setFillColor(col)
    c.rect(bx + 2, y_metrics - 4, box_w - 4, 4, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(col)
    c.drawCentredString(bx + box_w/2, y_metrics - 28, val)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(WHITE)
    c.drawCentredString(bx + box_w/2, y_metrics - 40, label)
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawCentredString(bx + box_w/2, y_metrics - 50, sub)

# ── SECTION 2: CHARTS + INCIDENT TABLE ────────────────────────────────────────
y_section = y_metrics - 58

# Left: Ternary plot
c.setFillColor(CARD)
c.rect(4, y_section - 155, 185, 152, fill=1, stroke=0)
c.setFillColor(ACCENT2)
c.rect(4, y_section - 5, 185, 4, fill=1, stroke=0)
c.setFont("Helvetica-Bold", 8)
c.setFillColor(WHITE)
c.drawString(10, y_section - 16, "MANAGERIAL ENERGY MAP")
c.setFont("Helvetica", 7)
c.setFillColor(MUTED)
c.drawString(10, y_section - 26, "G-A-C Ternary Plot — Semester Average")

ternary_buf = make_ternary_plot()
from reportlab.lib.utils import ImageReader
c.drawImage(ImageReader(ternary_buf), 8, y_section - 148, width=177, height=118)

# Middle: Bar chart
c.setFillColor(CARD)
c.rect(193, y_section - 155, 185, 152, fill=1, stroke=0)
c.setFillColor(ACCENT)
c.rect(193, y_section - 5, 185, 4, fill=1, stroke=0)
c.setFont("Helvetica-Bold", 8)
c.setFillColor(WHITE)
c.drawString(199, y_section - 16, "ENERGY DISTRIBUTION")
c.setFont("Helvetica", 7)
c.setFillColor(MUTED)
c.drawString(199, y_section - 26, "Average across 10 critical incidents")

bar_buf = make_bar_chart()
c.drawImage(ImageReader(bar_buf), 196, y_section - 148, width=179, height=118)

# Right: Strategic Redirection box
c.setFillColor(CARD)
c.rect(382, y_section - 155, W - 386, 152, fill=1, stroke=0)
c.setFillColor(RED)
c.rect(382, y_section - 5, W - 386, 4, fill=1, stroke=0)

c.setFont("Helvetica-Bold", 8)
c.setFillColor(RED)
c.drawString(388, y_section - 16, "STRATEGIC REDIRECTION")
c.setFont("Helvetica-Bold", 7)
c.setFillColor(ACCENT)
c.drawString(388, y_section - 28, "Incident #3: HS Chapter 93 Proxy Problem")

redirect_text = [
    "OWLET confidently proposed using",
    "SIPRI TIV data combined with USD",
    "military spending to build the proxy.",
    "The resulting ratio produced values",
    "close to 1.0 — fundamentally wrong.",
    "",
    "Intervention: Identified the unit",
    "mismatch (TIV vs USD) and redirected",
    "to UN Comtrade mirror data in USD",
    "for both variables. Fixed the proxy.",
    "",
    "Impact: Without this redirection,",
    "the entire model would have been",
    "built on a meaningless ratio.",
]
c.setFont("Helvetica", 7)
c.setFillColor(WHITE)
for i, line in enumerate(redirect_text):
    if line == "":
        continue
    col = ACCENT if line.startswith("Intervention") or line.startswith("Impact") else WHITE
    c.setFillColor(col if line else WHITE)
    c.drawString(388, y_section - 40 - i*8.5, line)

# ── SECTION 3: INCIDENT LOG TABLE ─────────────────────────────────────────────
y_table = y_section - 160

c.setFillColor(CARD)
c.rect(4, y_table - 195, W-8, 190, fill=1, stroke=0)
c.setFillColor(ACCENT)
c.rect(4, y_table - 5, W-8, 4, fill=1, stroke=0)

c.setFont("Helvetica-Bold", 8)
c.setFillColor(WHITE)
c.drawString(10, y_table - 16, "CRITICAL INCIDENT LOG  —  10 Managerial Interventions")

# Table headers
headers = ["#", "Incident Summary", "G%", "A%", "C%"]
col_widths = [18, 450, 32, 32, 32]
col_x = [8]
for w in col_widths[:-1]:
    col_x.append(col_x[-1] + w)

header_y = y_table - 30
c.setFillColor(colors.HexColor('#1A2A0A'))
c.rect(8, header_y - 2, W-16, 13, fill=1, stroke=0)
c.setFont("Helvetica-Bold", 7)
for i, (hdr, cx) in enumerate(zip(headers, col_x)):
    color = ACCENT if i == 0 else (ACCENT if i == 1 else ACCENT2)
    c.setFillColor(color)
    c.drawString(cx + 2, header_y + 2, hdr)

# Incident rows
for ri, (num, desc, g, a, ctx) in enumerate(incidents):
    row_y = header_y - 16 - ri * 15
    bg = colors.HexColor('#181818') if ri % 2 == 0 else colors.HexColor('#1F1F1F')
    c.setFillColor(bg)
    c.rect(8, row_y - 3, W-16, 13, fill=1, stroke=0)

    # Truncate description
    max_desc = 90
    short_desc = desc[:max_desc] + '...' if len(desc) > max_desc else desc

    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(ACCENT)
    c.drawString(col_x[0] + 2, row_y + 2, num)

    c.setFont("Helvetica", 6.5)
    c.setFillColor(WHITE)
    c.drawString(col_x[1] + 2, row_y + 2, short_desc)

    # G A C values with color coding
    for val, cx, col in [(g, col_x[2], ACCENT), (a, col_x[3], ACCENT2), (ctx, col_x[4], MUTED)]:
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(col)
        c.drawCentredString(cx + 16, row_y + 2, str(val))

# ── SECTION 4: CONCLUSION ─────────────────────────────────────────────────────
y_conclusion = y_table - 200

c.setFillColor(colors.HexColor('#0D1A0D'))
c.rect(4, 28, W-8, y_conclusion - 30, fill=1, stroke=0)
c.setFillColor(ACCENT)
c.rect(4, 28, 4, y_conclusion - 30, fill=1, stroke=0)

c.setFont("Helvetica-Bold", 8)
c.setFillColor(ACCENT)
c.drawString(14, y_conclusion - 14, "HIRING DECISION: TERMINATE  —  Managerial Conclusion")

conclusion_lines = [
    "After a full semester of working with OWLET, my decision is to terminate. Not out of frustration, but because the numbers do not",
    "support keeping it at current capability. 75% of managerial energy went toward correcting and verifying outputs — not an assistant.",
    "",
    "The ternary plot lands squarely in Governance/Audit. Two incidents pushed the decision: the data source failure (Incident #1) and the",
    "HS Chapter 93 proxy problem (Incident #3). Both times OWLET delivered confident, structured analysis that was fundamentally misleading.",
    "In a real engineering environment, those outputs reach a client before you catch them. That is not a risk worth carrying on a team.",
    "",
    "GenAI is a tool, not a trainee. Trainees grow and internalize feedback — OWLET does not. Every session started from zero. What GenAI",
    "actually is: a fast first-draft machine requiring a domain expert behind it at all times. The speed gain is real, but so is the cognitive",
    "load. You are not delegating work — you are splitting it differently. You still own every judgment call.",
    "",
    "My honest takeaway: GenAI raises the floor for those who already know what they are doing, and raises the risk ceiling for those who do",
    "not. The tool is only as safe as the person reviewing its output. This semester taught me: the review is the job, not the prompt.",
]

c.setFont("Helvetica", 7)
c.setFillColor(WHITE)
for i, line in enumerate(conclusion_lines):
    c.drawString(14, y_conclusion - 26 - i * 9, line)

# ── FOOTER ────────────────────────────────────────────────────────────────────
c.setFillColor(DARK2)
c.rect(0, 0, W, 22, fill=1, stroke=0)
c.setFillColor(ACCENT)
c.rect(0, 22, W, 1, fill=1, stroke=0)
c.setFont("Helvetica", 7)
c.setFillColor(MUTED)
c.drawString(20, 8, "OWLET-AI Performance Evaluation  |  RCEL 506  |  Rice University  |  Mohammed Farran  |  April 2026")
c.drawRightString(W-20, 8, "Generated using Python + ReportLab + Matplotlib")

c.save()
print("PDF saved: OWLET_Performance_Report.pdf")
