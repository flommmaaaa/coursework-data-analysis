import os
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from common_styles import (
    style_toc_title, TOCLineFlowable, style_body, style_title
)
from reportlab.lib.styles import ParagraphStyle

def build_front_matter(story, toc_pages):
    # =========================================================================
    # 1. ТИТУЛЬНЫЙ ЛИСТ (Стр. 1)
    # =========================================================================
    p_header = ParagraphStyle('THeader', fontName='TimesNewRoman', fontSize=10.5, leading=14, alignment=1)
    p_header_b = ParagraphStyle('THeaderB', fontName='TimesNewRoman-Bold', fontSize=11, leading=15, alignment=1)
    p_doc_title = ParagraphStyle('TDocTitle', fontName='TimesNewRoman-Bold', fontSize=16, leading=21, alignment=1)
    p_doc_sub = ParagraphStyle('TDocSub', fontName='TimesNewRoman', fontSize=12, leading=16, alignment=1)
    p_cipher = ParagraphStyle('TCipher', fontName='TimesNewRoman-Bold', fontSize=13, leading=17, alignment=1)
    p_sign_left = ParagraphStyle('TSignL', fontName='TimesNewRoman', fontSize=11, leading=15, alignment=0)
    p_city = ParagraphStyle('TCity', fontName='TimesNewRoman', fontSize=11, leading=14, alignment=1)

    story.append(Paragraph("МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ", p_header))
    story.append(Paragraph("Федеральное государственное автономное образовательное учреждение высшего образования", p_header))
    story.append(Paragraph("«Южно-Уральский государственный университет (национальный исследовательский университет)»", p_header_b))
    story.append(Paragraph("Центр «ВиртУм»", p_header_b))
    story.append(Paragraph("Кафедра прикладной математики и программирования", p_header))
    story.append(Spacer(1, 25 * mm))

    story.append(Paragraph("КУРСОВОЙ ПРОЕКТ", p_doc_title))
    story.append(Paragraph("по дисциплине «Введение в проектную деятельность»", p_doc_sub))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("ЮУрГУ – 09.03.04.2026.306-328.КП", p_cipher))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("на тему: <b>«Поиск и первичный анализ наборов данных по различным областям применения»</b>", p_doc_sub))
    story.append(Spacer(1, 25 * mm))

    sign_data = [
        [
            Paragraph("<b>Руководитель проекта:</b><br/>д.ф.-м.н., профессор<br/>____________ М.Л. Цымблер<br/>«___» ____________ 2026 г.", p_sign_left),
            Paragraph("<b>Выполнил:</b><br/>студент группы ЕТ-242<br/>направление 09.03.04<br/>«Программная инженерия»<br/>____________ < И.О. Фамилия ><br/>«___» ____________ 2026 г.", p_sign_left)
        ]
    ]
    t_sign = Table(sign_data, colWidths=[90 * mm, 90 * mm])
    t_sign.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_sign)

    story.append(Spacer(1, 32 * mm))
    story.append(Paragraph("Челябинск, 2026 г.", p_city))
    story.append(PageBreak())

    # =========================================================================
    # 2. ЗАДАНИЕ НА КУРСОВОЙ ПРОЕКТ (Стр. 2)
    # =========================================================================
    p_task_inst = ParagraphStyle('TaskInst', fontName='TimesNewRoman', fontSize=9, leading=12, alignment=1)
    p_task_inst_b = ParagraphStyle('TaskInstB', fontName='TimesNewRoman-Bold', fontSize=9.5, leading=12.5, alignment=1)
    p_task_title = ParagraphStyle('TaskT', fontName='TimesNewRoman-Bold', fontSize=12.5, leading=16, alignment=1)
    p_task_sub = ParagraphStyle('TaskS', fontName='TimesNewRoman', fontSize=10, leading=13.5, alignment=0)
    p_task_body = ParagraphStyle('TaskB', fontName='TimesNewRoman', fontSize=9.5, leading=13, alignment=4, firstLineIndent=6 * mm)

    story.append(Paragraph("МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ", p_task_inst))
    story.append(Paragraph("Федеральное государственное автономное образовательное учреждение высшего образования", p_task_inst))
    story.append(Paragraph("«Южно-Уральский государственный университет (национальный исследовательский университет)»", p_task_inst_b))
    story.append(Paragraph("Центр «ВиртУм»", p_task_inst_b))
    story.append(Spacer(1, 3 * mm))

    task_header_data = [
        [
            Paragraph("", p_task_sub),
            Paragraph("<b>УТВЕРЖДАЮ</b><br/>Директор ИЕТН ЮУрГУ<br/>д.ф.-м.н., профессор<br/>__________ А.А. Замышляева<br/>«___»._____________.2026 г.", p_task_sub)
        ]
    ]
    t_th = Table(task_header_data, colWidths=[95 * mm, 85 * mm])
    t_th.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_th)
    story.append(Spacer(1, 2 * mm))

    story.append(Paragraph("ЗАДАНИЕ<br/>на выполнение курсового проекта по дисциплине «Введение в проектную деятельность»", p_task_title))
    story.append(Spacer(1, 2 * mm))

    story.append(Paragraph("<b>Студенту группы:</b> ЕТ-242 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Направление:</b> 09.03.04 «Программная инженерия»", p_task_sub))
    story.append(Paragraph("<b>Тема проекта:</b> Поиск и первичный анализ наборов данных по различным областям применения", p_task_sub))
    story.append(Paragraph("<b>Срок сдачи студентом законченной работы:</b> 21.09.2026 г.", p_task_sub))
    story.append(Spacer(1, 1.5 * mm))

    story.append(Paragraph("<b>Исходные данные к работе:</b>", p_task_sub))
    story.append(Paragraph("1. Источник набора табличных данных: https://github.com/stedy/Machine-Learning-with-R-datasets/blob/master/insurance.csv", p_task_sub))
    story.append(Paragraph("2. Источник набора данных с временными рядами: https://www.kaggle.com/datasets/harishkumardatalab/medical-insurance-price-prediction", p_task_sub))
    story.append(Paragraph("3. Источник набора данных с изображениями: https://github.com/aashwika25/PPE_Detection_YOLO/tree/main", p_task_sub))
    story.append(Paragraph("4. Источник набора текстовых данных: https://github.com/Koziev/NLP_Datasets", p_task_sub))
    story.append(Spacer(1, 1.5 * mm))

    story.append(Paragraph("<b>Перечень подлежащих разработке вопросов:</b>", p_task_sub))
    story.append(Paragraph("1. Подготовить для каждого типа данных (табличные данные, временные ряды, изображения, тексты, аудио) краткое описание выбранной задачи, решение которой связано с применением технологий искусственного интеллекта.", p_task_body))
    story.append(Paragraph("2. Подобрать для каждого типа данных набор данных из авторитетных открытых источников, необходимый для обучения ИИ-модели, решающей соответствующую выбранную задачу;", p_task_body))
    story.append(Paragraph("3. Разработать и реализовать комплекс программ на языке Python, каждая из которых для заданного типа данных должна выполнять следующие основные функции первичного анализа: загрузка и визуализация данных, статистический анализ, выявление специфических особенностей для определенного типа данных.", p_task_body))
    story.append(Paragraph("4. Сформулировать выводы по каждому этапу анализа, а также итоговое заключение о качестве данных и их пригодности для решения поставленной задачи.", p_task_body))
    story.append(Paragraph("5. Разместить исходный код в репозитории системы контроля версий Git.", p_task_body))
    story.append(Spacer(1, 2 * mm))

    task_sign_data = [
        [
            Paragraph("<b>Научный руководитель:</b><br/>профессор М.Л. Цымблер __________", p_task_sub),
            Paragraph("<b>Задание принял к исполнению:</b><br/>студент __________", p_task_sub)
        ]
    ]
    t_ts = Table(task_sign_data, colWidths=[90 * mm, 90 * mm])
    t_ts.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_ts)
    story.append(PageBreak())

    # =========================================================================
    # 3. ОГЛАВЛЕНИЕ (Стр. 3–4: 2 страницы)
    # =========================================================================
    story.append(Paragraph("ОГЛАВЛЕНИЕ", style_toc_title))

    def toc_line(title, page_key, is_h1=True, indent=0):
        pg = toc_pages.get(page_key, "...")
        return TOCLineFlowable(title, pg, is_h1=is_h1, indent=indent, width=180*mm, height=5.5*mm)

    # Page 3 of document: Introduction, Chapter 1, Chapter 2
    story.append(toc_line("ВВЕДЕНИЕ", "intro", True, 0))
    story.append(Spacer(1, 1.5 * mm))

    story.append(toc_line("1. ПЕРВИЧНЫЙ АНАЛИЗ НАБОРА ТАБЛИЧНЫХ ДАННЫХ", "ch1", True, 0))
    story.append(toc_line("1.1. Постановка задачи", "ch1_1", False, 6 * mm))
    story.append(toc_line("1.2. Описание выбранного набора данных", "ch1_2", False, 6 * mm))
    story.append(toc_line("1.3. Описание результатов первичного анализа", "ch1_3", False, 6 * mm))
    story.append(toc_line("Визуализация распределения признаков", "ch1_dist", False, 12 * mm))
    story.append(toc_line("Анализ на наличие пропусков в данных", "ch1_miss", False, 12 * mm))
    story.append(toc_line("Выявление и устранение дубликатов", "ch1_dup", False, 12 * mm))
    story.append(toc_line("Анализ и обработка аномальных значений (выбросов)", "ch1_outl", False, 12 * mm))
    story.append(toc_line("Фильтрация данных по заданным условиям", "ch1_filt", False, 12 * mm))
    story.append(toc_line("Моделирование устойчивости путем добавления случайного шума", "ch1_noise", False, 12 * mm))
    story.append(toc_line("Выводы по первому разделу", "ch1_concl", False, 6 * mm))
    story.append(Spacer(1, 1.5 * mm))

    story.append(toc_line("2. ПЕРВИЧНЫЙ АНАЛИЗ НАБОРА ДАННЫХ С ВРЕМЕННЫМИ РЯДАМИ", "ch2", True, 0))
    story.append(toc_line("2.1. Постановка задачи", "ch2_1", False, 6 * mm))
    story.append(toc_line("2.2. Описание выбранного набора данных", "ch2_2", False, 6 * mm))
    story.append(toc_line("2.3. Описание результатов первичного анализа", "ch2_3", False, 6 * mm))
    story.append(toc_line("Визуализация исходных данных", "ch2_vis", False, 12 * mm))
    story.append(toc_line("Анализ на наличие пропусков", "ch2_miss", False, 12 * mm))
    story.append(toc_line("Анализ диапазонов значений", "ch2_range", False, 12 * mm))
    story.append(toc_line("Поиск шумов", "ch2_noise", False, 12 * mm))
    story.append(toc_line("Выводы по второму разделу", "ch2_concl", False, 6 * mm))

    story.append(PageBreak())

    # Page 4 of document: Chapter 3, Chapter 4, Conclusion, Literature, Appendix
    story.append(Paragraph("ОГЛАВЛЕНИЕ (продолжение)", ParagraphStyle('TOCCtr', fontName='TimesNewRoman-Italic', fontSize=10.5, leading=14, alignment=2, spaceAfter=8)))

    story.append(toc_line("3. ПЕРВИЧНЫЙ АНАЛИЗ НАБОРА ДАННЫХ С ИЗОБРАЖЕНИЯМИ", "ch3", True, 0))
    story.append(toc_line("3.1. Постановка задачи", "ch3_1", False, 6 * mm))
    story.append(toc_line("3.2. Описание выбранного набора данных", "ch3_2", False, 6 * mm))
    story.append(toc_line("3.3. Описание результатов первичного анализа", "ch3_3", False, 6 * mm))
    story.append(toc_line("Анализ количества и баланса классов", "ch3_cls", False, 12 * mm))
    story.append(toc_line("Примеры типичных изображений", "ch3_sample", False, 12 * mm))
    story.append(toc_line("Анализ качества разметки и аннотаций", "ch3_bbox", False, 12 * mm))
    story.append(toc_line("Выводы по третьему разделу", "ch3_concl", False, 6 * mm))
    story.append(Spacer(1, 1.5 * mm))

    story.append(toc_line("4. ПЕРВИЧНЫЙ АНАЛИЗ НАБОРА ТЕКСТОВЫХ ДАННЫХ", "ch4", True, 0))
    story.append(toc_line("4.1. Постановка задачи", "ch4_1", False, 6 * mm))
    story.append(toc_line("4.2. Описание выбранного набора данных", "ch4_2", False, 6 * mm))
    story.append(toc_line("4.3. Описание результатов первичного анализа", "ch4_3", False, 6 * mm))
    story.append(toc_line("Очистка текста и лемматизация", "ch4_clean", False, 12 * mm))
    story.append(toc_line("Подсчет частоты слов и удаление стоп-слов", "ch4_freq", False, 12 * mm))
    story.append(toc_line("TF-IDF векторизация и информационный поиск", "ch4_tfidf", False, 12 * mm))
    story.append(toc_line("Выводы по четвертому разделу", "ch4_concl", False, 6 * mm))
    story.append(Spacer(1, 1.5 * mm))

    story.append(toc_line("ЗАКЛЮЧЕНИЕ", "conclusion", True, 0))
    story.append(Spacer(1, 1.5 * mm))
    story.append(toc_line("ЛИТЕРАТУРА", "biblio", True, 0))
    story.append(Spacer(1, 1.5 * mm))
    story.append(toc_line("ПРИЛОЖЕНИЕ А. Архитектура репозитория и программный код", "app_a", True, 0))

    story.append(PageBreak())
