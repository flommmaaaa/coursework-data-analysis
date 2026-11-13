import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate

from common_styles import (
    SECTION_PAGES, NumberedCanvas, OUT_DIR
)
from front_matter import build_front_matter
from intro_builder import build_intro
from ch1_builder import build_ch1
from ch2_builder import build_ch2
from ch3_builder import build_ch3
from ch4_builder import build_ch4
from back_matter import build_back_matter

def build_full_story(toc_pages):
    story = []
    build_front_matter(story, toc_pages)
    build_intro(story)
    build_ch1(story)
    build_ch2(story)
    build_ch3(story)
    build_ch4(story)
    build_back_matter(story)
    return story

def compile_50pages_pdf():
    pdf_filename = os.path.join(OUT_DIR, "Курсовой_проект_Итоговый_50стр.pdf")
    pdf_standard_name = os.path.join(OUT_DIR, "Курсовой_проект_Итоговый.pdf")

    print("=== Starting Pass 1 (Dry run for page detection) ===")
    dummy_pages = {k: "..." for k in [
        "intro",
        "ch1", "ch1_1", "ch1_2", "ch1_3", "ch1_dist", "ch1_miss", "ch1_dup", "ch1_outl", "ch1_filt", "ch1_noise", "ch1_concl",
        "ch2", "ch2_1", "ch2_2", "ch2_3", "ch2_vis", "ch2_miss", "ch2_range", "ch2_noise", "ch2_concl",
        "ch3", "ch3_1", "ch3_2", "ch3_3", "ch3_cls", "ch3_sample", "ch3_bbox", "ch3_concl",
        "ch4", "ch4_1", "ch4_2", "ch4_3", "ch4_clean", "ch4_freq", "ch4_tfidf", "ch4_concl",
        "conclusion", "biblio", "app_a"
    ]}

    doc_pass1 = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=30 * mm,
        rightMargin=15 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )
    story1 = build_full_story(dummy_pages)
    doc_pass1.build(story1, canvasmaker=NumberedCanvas)

    print("Pass 1 completed. Detected page numbers:")
    for k, v in SECTION_PAGES.items():
        print(f"  {k} -> Page {v}")

    print("\n=== Starting Pass 2 (Final build with exact TOC pages) ===")
    doc_pass2 = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=30 * mm,
        rightMargin=15 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )
    story2 = build_full_story(SECTION_PAGES)
    doc_pass2.build(story2, canvasmaker=NumberedCanvas)

    shutil.copyfile(pdf_filename, pdf_standard_name)
    print(f"\nFinal unified 50-page coursework successfully generated at:")
    print(f"  -> {pdf_filename}")
    print(f"  -> {pdf_standard_name}")

if __name__ == '__main__':
    compile_50pages_pdf()
