import os
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime, timezone


def column_letter(col_index: int) -> str:
    letters = ""
    dividend = col_index + 1
    while dividend > 0:
        modulo = (dividend - 1) % 26
        letters = chr(65 + modulo) + letters
        dividend = (dividend - modulo - 1) // 26
    return letters


def cell_ref(row_index: int, col_index: int) -> str:
    return f"{column_letter(col_index)}{row_index + 1}"


def xml_header() -> str:
    return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"


def build_checklist(output_path: str) -> None:
    headers = [" ", "Что нужно сделать", "Кто отвечает", "Обязательно"]
    rows = [
        (
            "Направить запрос/описание инициативы директору Дирекции развития по эл. почте",
            "Инициатор",
            "Обязательно",
        ),
        ("Внести инициативу в реестр (КСУПД)", "Директор Дирекции развития / Администратор инициатив", "Обязательно"),
        ("Присвоить уникальный ID инициативы", "Директор Дирекции развития / Администратор инициатив", "Обязательно"),
        ("Назначить куратора инициативы", "Директор Дирекции развития", "Обязательно"),
        ("Назначить администратора инициативы", "Директор Дирекции развития", "Обязательно"),
        ("Провести установочное совещание при необходимости и зафиксировать итоги", "Директор Дирекции развития / Куратор", "Опционально"),
        ("Выполнить предварительную проработку (справки, презентации) для принятия решения", "Дирекция развития / Куратор", "Опционально"),
        ("Согласовать привлечение других подразделений (особые случаи)", "Курирующий зам. гендиректора / Директор Дирекции", "Опционально"),
        ("Сформировать команду инициативы", "Куратор", "Обязательно"),
        ("Определить роли и зоны ответственности участников", "Куратор", "Обязательно"),
        ("Подготовить Карточку инициативы (ID, цель, результаты, стороны, риски, сроки, ресурсы)", "Куратор / Администратор инициатив", "Обязательно"),
        ("Подготовить План расходов инициативы (статьи затрат, этапы, лимиты)", "Куратор / Финансовое подразделение", "Обязательно"),
        ("Составить Дорожную карту инициативы (этапы, вехи, зависимости, критерии выхода)", "Куратор / Команда инициативы", "Обязательно"),
        ("Направить комплект документов на согласование", "Куратор / Администратор инициатив", "Обязательно"),
        ("Получить визирования, учесть замечания, обновить версии документов", "Куратор / Администратор инициатив", "Обязательно"),
        ("Зафиксировать решение об открытии инициативы", "Директор Дирекции развития", "Обязательно"),
        ("Завести карточку инициативы в КСУПД и прикрепить документы", "Администратор инициатив", "Обязательно"),
        ("Назначить права доступа участникам и ответственным", "Администратор инициатив", "Обязательно"),
        ("Обеспечить хранение документации в Дирекции развития не менее 1 года", "Дирекция развития / Администратор инициатив", "Обязательно"),
        ("Определить дальнейшие шаги (статус-отчётность, закупка/договор, инициация проекта)", "Куратор", "Обязательно"),
    ]

    # Build worksheet XML with inline strings and data validation list for checkboxes
    sheet_rows_xml = []

    def inline_str_cell(r: int, c: int, value: str) -> str:
        ref = cell_ref(r, c)
        # Escape XML special chars
        esc = (
            value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        return f"<c r=\"{ref}\" t=\"inlineStr\"><is><t>{esc}</t></is></c>"

    # Header row (row index 0)
    header_cells = "".join(inline_str_cell(0, i, h) for i, h in enumerate(headers))
    sheet_rows_xml.append(f"<row r=\"1\">{header_cells}</row>")

    # Data rows start at row 2 (index 1)
    for idx, (task, responsible, mandatory) in enumerate(rows, start=2):
        # A column preset to unchecked box
        c0 = inline_str_cell(idx - 1, 0, "☐")
        c1 = inline_str_cell(idx - 1, 1, task)
        c2 = inline_str_cell(idx - 1, 2, responsible)
        c3 = inline_str_cell(idx - 1, 3, mandatory)
        sheet_rows_xml.append(f"<row r=\"{idx}\">{c0}{c1}{c2}{c3}</row>")

    last_row = 1 + len(rows) + 1 - 1  # zero-based math simplified below by direct use
    total_rows = 1 + len(rows)

    # Data validation for each A cell from A2..A{total_rows}
    validations = []
    for r in range(2, total_rows + 1):
        validations.append(
            f"<dataValidation type=\"list\" allowBlank=\"1\" showInputMessage=\"1\" sqref=\"A{r}\"><formula1>\"☐,☑\"</formula1></dataValidation>"
        )
    data_validations_xml = (
        f"<dataValidations count=\"{len(validations)}\">" + "".join(validations) + "</dataValidations>"
        if validations
        else ""
    )

    # Column widths
    cols_xml = (
        "<cols>"
        "<col min=\"1\" max=\"1\" width=\"5\" customWidth=\"1\"/>"
        "<col min=\"2\" max=\"2\" width=\"70\" customWidth=\"1\"/>"
        "<col min=\"3\" max=\"3\" width=\"32\" customWidth=\"1\"/>"
        "<col min=\"4\" max=\"4\" width=\"14\" customWidth=\"1\"/>"
        "</cols>"
    )

    sheet_xml = (
        xml_header()
        + "<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">"
        + "<sheetViews><sheetView workbookViewId=\"0\"><pane ySplit=\"1\" topLeftCell=\"A2\" activePane=\"bottomLeft\" state=\"frozen\"/></sheetView></sheetViews>"
        + cols_xml
        + "<sheetData>"
        + "".join(sheet_rows_xml)
        + "</sheetData>"
        + f"<autoFilter ref=\"A1:D{total_rows}\"/>"
        + data_validations_xml
        + "</worksheet>"
    )

    workbook_xml = (
        xml_header()
        + "<workbook xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">"
        + "<sheets>"
        + "<sheet name=\"Чек-лист\" sheetId=\"1\" r:id=\"rId1\"/>"
        + "</sheets>"
        + "</workbook>"
    )

    workbook_rels_xml = (
        xml_header()
        + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
        + "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet\" Target=\"worksheets/sheet1.xml\"/>"
        + "</Relationships>"
    )

    root_rels_xml = (
        xml_header()
        + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
        + "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"xl/workbook.xml\"/>"
        + "<Relationship Id=\"rId2\" Type=\"http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties\" Target=\"docProps/core.xml\"/>"
        + "<Relationship Id=\"rId3\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties\" Target=\"docProps/app.xml\"/>"
        + "</Relationships>"
    )

    # Minimal app and core properties
    app_xml = (
        xml_header()
        + "<Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/extended-properties\" xmlns:vt=\"http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes\">"
        + "<Application>Python</Application>"
        + "</Properties>"
    )

    now = datetime.now(timezone.utc).isoformat()
    core_xml = (
        xml_header()
        + "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:dcterms=\"http://purl.org/dc/terms/\" xmlns:dcmitype=\"http://purl.org/dc/dcmitype/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        + "<dc:title>Чек-лист предпроектной деятельности</dc:title>"
        + "<dc:creator>Generator</dc:creator>"
        + f"<dcterms:created xsi:type=\"dcterms:W3CDTF\">{now}</dcterms:created>"
        + f"<dcterms:modified xsi:type=\"dcterms:W3CDTF\">{now}</dcterms:modified>"
        + "</cp:coreProperties>"
    )

    content_types_xml = (
        xml_header()
        + "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
        + "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>"
        + "<Default Extension=\"xml\" ContentType=\"application/xml\"/>"
        + "<Override PartName=\"/xl/workbook.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml\"/>"
        + "<Override PartName=\"/xl/worksheets/sheet1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml\"/>"
        + "<Override PartName=\"/docProps/core.xml\" ContentType=\"application/vnd.openxmlformats-package.core-properties+xml\"/>"
        + "<Override PartName=\"/docProps/app.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.extended-properties+xml\"/>"
        + "</Types>"
    )

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml)
        z.writestr("_rels/.rels", root_rels_xml)
        z.writestr("xl/workbook.xml", workbook_xml)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)
        z.writestr("docProps/app.xml", app_xml)
        z.writestr("docProps/core.xml", core_xml)


if __name__ == "__main__":
    output_file = os.path.join("/workspace", "predproekt_checklist.xlsx")
    build_checklist(output_file)
    print(f"Created: {output_file}")

