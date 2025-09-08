#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор блок-схемы процесса утверждения документов на открытие проекта
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.font_manager as fm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import os

def create_flowchart():
    """Создание блок-схемы процесса утверждения документов"""
    
    # Настройка размера и разрешения
    fig, ax = plt.subplots(1, 1, figsize=(16, 20))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Цвета для разных типов блоков
    colors_dict = {
        'start_end': '#4CAF50',
        'process': '#2196F3', 
        'decision': '#FF9800',
        'document': '#9C27B0'
    }
    
    # Функция для создания блока
    def create_box(x, y, width, height, text, box_type='process', fontsize=9):
        if box_type == 'decision':
            # Ромб для решения
            diamond = mpatches.FancyBboxPatch(
                (x-width/2, y-height/2), width, height,
                boxstyle="round,pad=0.02",
                facecolor=colors_dict[box_type],
                edgecolor='black',
                linewidth=1.5
            )
        else:
            # Прямоугольник для процесса
            diamond = mpatches.FancyBboxPatch(
                (x-width/2, y-height/2), width, height,
                boxstyle="round,pad=0.02",
                facecolor=colors_dict[box_type],
                edgecolor='black',
                linewidth=1.5
            )
        
        ax.add_patch(diamond)
        
        # Добавление текста
        ax.text(x, y, text, ha='center', va='center', 
               fontsize=fontsize, weight='bold', color='white',
               wrap=True, bbox=dict(boxstyle="round,pad=0", 
                                   facecolor='none', edgecolor='none'))
    
    # Функция для создания стрелки
    def create_arrow(x1, y1, x2, y2, text=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        if text:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.2, mid_y, text, fontsize=8, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Заголовок
    ax.text(5, 11.5, 'Блок-схема процесса А1.5\n«Утверждение документов на открытие проекта»', 
           ha='center', va='center', fontsize=16, weight='bold')
    
    # Блоки процесса
    
    # 1. Начало
    create_box(5, 10.5, 2, 0.4, 'НАЧАЛО', 'start_end', 10)
    
    # 2. Подготовка документов
    create_box(5, 9.5, 3, 0.6, 'Подготовка необходимых\nдокументов на открытие проекта\n(РП)', 'process')
    create_arrow(5, 10.3, 5, 9.8)
    
    # 3. Отправка на согласование  
    create_box(5, 8.5, 3, 0.6, 'Отправка документов\nна согласование в СЭД\n(РП)', 'process')
    create_arrow(5, 9.2, 5, 8.8)
    
    # 4. Согласование
    create_box(5, 7.3, 3.5, 0.8, 'Согласование документов\n(Руководители подразделений,\nДЭФ, ДАД)\n2 рабочих дня на этап', 'process')
    create_arrow(5, 8.2, 5, 7.7)
    
    # 5. Решение о согласовании
    create_box(5, 6, 2.5, 0.6, 'Документы\nсогласованы?', 'decision')
    create_arrow(5, 6.9, 5, 6.3)
    
    # 6а. Доработка (НЕТ)
    create_box(2, 6, 2, 0.6, 'Доработка\nдокументов\n(РП)', 'process')
    create_arrow(3.75, 6, 3, 6, 'НЕТ')
    create_arrow(2, 6.3, 2, 8.5)
    create_arrow(2, 8.5, 3.5, 8.5)
    
    # 6б. Передача на утверждение (ДА)
    create_box(5, 4.8, 3, 0.6, 'Передача на утверждение\nкуратору проекта\n(РП)', 'process')
    create_arrow(5, 5.7, 5, 5.1, 'ДА')
    
    # 7. Утверждение
    create_box(5, 3.6, 3, 0.6, 'Утверждение документов\n(Куратор проекта)', 'process')
    create_arrow(5, 4.5, 5, 3.9)
    
    # 8. Решение об утверждении
    create_box(5, 2.4, 2.5, 0.6, 'Документы\nутверждены?', 'decision')
    create_arrow(5, 3.3, 5, 2.7)
    
    # 8а. Доработка (НЕТ)
    create_box(8, 2.4, 2, 0.6, 'Направление\nна доработку', 'process')
    create_arrow(6.25, 2.4, 7, 2.4, 'НЕТ')
    create_arrow(8, 2.7, 8, 4.8)
    create_arrow(8, 4.8, 6.5, 4.8)
    
    # 9. Размещение документов (ДА)
    create_box(5, 1.2, 3.5, 0.6, 'Размещение электронных\nобразов утвержденных\nдокументов в узле проекта\n(РП, Куратор)', 'document')
    create_arrow(5, 2.1, 5, 1.5, 'ДА')
    
    # 10. Конец
    create_box(5, 0.3, 2, 0.4, 'КОНЕЦ', 'start_end', 10)
    create_arrow(5, 0.9, 5, 0.5)
    
    # Легенда
    legend_elements = [
        mpatches.Patch(color=colors_dict['start_end'], label='Начало/Конец'),
        mpatches.Patch(color=colors_dict['process'], label='Процесс'),
        mpatches.Patch(color=colors_dict['decision'], label='Решение'),
        mpatches.Patch(color=colors_dict['document'], label='Документооборот')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    # Добавление информации об ответственных
    ax.text(0.2, 11, 'Условные обозначения:\nРП - Руководитель проекта\nДЭФ - Директор по экономике и финансам\nДАД - Директор по административной деятельности\nСЭД - Система электронного документооборота', 
           fontsize=8, va='top',
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    return fig

def save_as_pdf(fig, filename):
    """Сохранение блок-схемы в PDF"""
    # Сохранение как изображение в памяти
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    
    # Создание PDF
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    story = []
    
    # Добавление заголовка
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Центрирование
    )
    
    title = Paragraph("Блок-схема процесса А1.5<br/>«Утверждение документов на открытие проекта»", title_style)
    story.append(title)
    
    # Сохранение изображения во временный файл
    temp_img_path = '/tmp/flowchart_temp.png'
    fig.savefig(temp_img_path, format='png', dpi=300, bbox_inches='tight')
    
    # Добавление изображения с подходящим размером
    img = Image(temp_img_path, width=9*inch, height=6*inch)
    story.append(img)
    
    # Добавление описания процесса
    story.append(Spacer(1, 20))
    
    description_style = ParagraphStyle(
        'Description',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12
    )
    
    description_text = """
    <b>Описание процесса:</b><br/>
    1. РП подготавливает необходимые документы на основе шаблонов<br/>
    2. Документы размещаются на согласование в СЭД<br/>
    3. Согласование проходит в течение 2 рабочих дней на каждый этап<br/>
    4. При необходимости документы дорабатываются<br/>
    5. Согласованные документы передаются куратору на утверждение<br/>
    6. Утвержденные документы размещаются в узле проекта в PDF-формате<br/>
    """
    
    description = Paragraph(description_text, description_style)
    story.append(description)
    
    # Генерация PDF
    doc.build(story)
    
    # Удаление временного файла
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

if __name__ == "__main__":
    # Создание блок-схемы
    fig = create_flowchart()
    
    # Сохранение в PDF
    pdf_filename = "/workspace/flowchart_approval_process.pdf"
    save_as_pdf(fig, pdf_filename)
    
    print(f"Блок-схема сохранена в файл: {pdf_filename}")
    
    # Также сохранение как PNG для предварительного просмотра
    png_filename = "/workspace/flowchart_approval_process.png"
    fig.savefig(png_filename, dpi=300, bbox_inches='tight')
    print(f"Изображение сохранено в файл: {png_filename}")
    
    plt.close()