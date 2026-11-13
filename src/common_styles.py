import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Register Times New Roman and Courier New fonts
FONT_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont('TimesNewRoman', os.path.join(FONT_DIR, 'times.ttf')))
pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', os.path.join(FONT_DIR, 'timesbd.ttf')))
pdfmetrics.registerFont(TTFont('TimesNewRoman-Italic', os.path.join(FONT_DIR, 'timesi.ttf')))
pdfmetrics.registerFont(TTFont('TimesNewRoman-BoldItalic', os.path.join(FONT_DIR, 'timesbi.ttf')))
pdfmetrics.registerFont(TTFont('CourierNew', os.path.join(FONT_DIR, 'cour.ttf')))
pdfmetrics.registerFont(TTFont('CourierNew-Bold', os.path.join(FONT_DIR, 'courbd.ttf')))

WORKDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIG_DIR = os.path.join(WORKDIR, "figures_exact")
OUT_DIR = os.path.join(WORKDIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

# Global dictionary to store detected page numbers for TOC
SECTION_PAGES = {}

class BookmarkFlowable(Flowable):
    def __init__(self, key):
        super(BookmarkFlowable, self).__init__()
        self.key = key
        self.width = 0
        self.height = 0

    def draw(self):
        SECTION_PAGES[self.key] = self.canv._pageNumber

class TOCLineFlowable(Flowable):
    def __init__(self, title, page_str, is_h1=True, indent=0, width=165*mm, height=5.5*mm):
        super(TOCLineFlowable, self).__init__()
        self.title = title
        self.page_str = str(page_str)
        self.is_h1 = is_h1
        self.indent = indent
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        canv = self.canv
        canv.saveState()
        
        font_name = 'TimesNewRoman-Bold' if self.is_h1 else 'TimesNewRoman'
        font_size = 11 if self.is_h1 else 10.5
        canv.setFont(font_name, font_size)
        
        y = 1.2 * mm
        canv.drawString(self.indent, y, self.title)
        title_width = canv.stringWidth(self.title, font_name, font_size)
        
        pg_font = 'TimesNewRoman-Bold' if self.is_h1 else 'TimesNewRoman'
        pg_size = 11 if self.is_h1 else 10.5
        canv.setFont(pg_font, pg_size)
        canv.drawRightString(self.width, y, self.page_str)
        page_width = canv.stringWidth(self.page_str, pg_font, pg_size)
        
        # Leader dots
        dot = ". "
        canv.setFont('TimesNewRoman', 9)
        canv.setFillColor(colors.HexColor('#666666'))
        dot_width = canv.stringWidth(dot, 'TimesNewRoman', 9)
        
        start_x = self.indent + title_width + 2.5 * mm
        end_x = self.width - page_width - 2.5 * mm
        
        curr_x = start_x
        while curr_x + dot_width <= end_x:
            canv.drawString(curr_x, y, dot)
            curr_x += dot_width
            
        canv.restoreState()

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Pages 1 and 2 (Title and Task Assignment) do not have page numbers printed per GOST
        if self._pageNumber > 2:
            self.saveState()
            self.setFont("TimesNewRoman", 11)
            page_text = f"{self._pageNumber}"
            # Centered at 105 mm (middle of A4 page width 210 mm), 12 mm from bottom
            self.drawCentredString(105 * mm, 12 * mm, page_text)
            self.restoreState()

# Typography Styles strictly conforming to GOST 7.32-2017
style_title = ParagraphStyle(
    'ChapterTitle',
    fontName='TimesNewRoman-Bold',
    fontSize=14,
    leading=18,
    alignment=1, # Centered
    spaceAfter=12,
    keepWithNext=True
)

style_h1 = ParagraphStyle(
    'SectionH1',
    fontName='TimesNewRoman-Bold',
    fontSize=13,
    leading=16.5,
    alignment=0, # Left
    firstLineIndent=12.5 * mm,
    spaceBefore=9,
    spaceAfter=5,
    keepWithNext=True
)

style_h2 = ParagraphStyle(
    'SectionH2',
    fontName='TimesNewRoman-Bold',
    fontSize=12,
    leading=15.5,
    alignment=0,
    firstLineIndent=12.5 * mm,
    spaceBefore=7,
    spaceAfter=4,
    keepWithNext=True
)

style_h3 = ParagraphStyle(
    'SectionH3',
    fontName='TimesNewRoman-BoldItalic',
    fontSize=11.5,
    leading=14.5,
    alignment=0,
    firstLineIndent=12.5 * mm,
    spaceBefore=5,
    spaceAfter=3,
    keepWithNext=True
)

style_body = ParagraphStyle(
    'BodyTextCustom',
    fontName='TimesNewRoman',
    fontSize=12,
    leading=16.5, # 1.5 line spacing equivalent
    alignment=4, # Justified
    firstLineIndent=12.5 * mm,
    spaceAfter=0
)

style_bullet = ParagraphStyle(
    'BulletCustom',
    fontName='TimesNewRoman',
    fontSize=12,
    leading=16,
    alignment=4,
    leftIndent=17 * mm,
    firstLineIndent=-4.5 * mm,
    spaceAfter=2
)

style_caption = ParagraphStyle(
    'FigureCaption',
    fontName='TimesNewRoman',
    fontSize=11,
    leading=13,
    alignment=1, # Centered
    spaceBefore=4,
    spaceAfter=6,
    keepWithNext=False
)

style_table_caption = ParagraphStyle(
    'TableCaption',
    fontName='TimesNewRoman',
    fontSize=11,
    leading=13,
    alignment=0, # Left aligned
    spaceBefore=6,
    spaceAfter=3,
    keepWithNext=True
)

style_th = ParagraphStyle(
    'TableHeader',
    fontName='TimesNewRoman-Bold',
    fontSize=8.5,
    leading=10.5,
    alignment=1, # Center
)

style_td = ParagraphStyle(
    'TableCell',
    fontName='TimesNewRoman',
    fontSize=8,
    leading=10.5,
    alignment=1, # Center
)

style_td_left = ParagraphStyle(
    'TableCellLeft',
    fontName='TimesNewRoman',
    fontSize=8,
    leading=10.5,
    alignment=0, # Left
)

style_code = ParagraphStyle(
    'CodeStyle',
    fontName='CourierNew',
    fontSize=7.5,
    leading=9.5,
    alignment=0,
    leftIndent=6 * mm,
    spaceBefore=2,
    spaceAfter=2
)

style_toc_title = ParagraphStyle(
    'TOCTitle',
    fontName='TimesNewRoman-Bold',
    fontSize=14,
    leading=18,
    alignment=1,
    spaceAfter=10
)
