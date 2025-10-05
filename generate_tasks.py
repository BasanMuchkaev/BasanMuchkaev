# -*- coding: utf-8 -*-
import re
import sys
import subprocess
import site


def ensure_openpyxl_workbook():
    try:
        from openpyxl import Workbook as _Workbook
        return _Workbook
    except Exception:
        try:
            user_site = site.getusersitepackages()
            if user_site and user_site not in sys.path:
                sys.path.append(user_site)
        except Exception:
            pass
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "openpyxl"])  # noqa: E402
        except Exception:
            raise
        try:
            user_site = site.getusersitepackages()
            if user_site and user_site not in sys.path:
                sys.path.append(user_site)
        except Exception:
            pass
        from openpyxl import Workbook as _Workbook
        return _Workbook

TEXT = '''
- ASISPEVO-100 SQL. ПМУ / ПФУ. Дашборд. Номер машины сделать кликабельным. 
- ASISPEVO-31 SQL. Исправление и доработки хранимых п р о ц е д у р
- ASISPEVO-102 SQL. Исправление и доработки хранимых п р о ц е д у р
- ASISPEVO-111 ПРОД. ПМУ. Дашборд. Увеличить количество п а р к о в о ч н ы х мест.
- ASISPEVO-113 БЭ. ПМУ. [ ТехЗакр ] Доработка механизма закрытия после изменения 
- ASISPEVO-114 БЭ. ПМУ / ПФУ. Дашборд. Номер машины сделать кликабельным. 
- ASISPEVO-115 SQL. ПМУ. МФАПП . Прод. Обновить команды для камер.
- ASISPEVO-118 SQL. ПМУ. [ ТехЗакр ] Доработать функцию и иерархию по 
- ASISPEVO-120 SQL. ПМУ. [ ТехЗакр ] Доработки функциизакрытия зон
- ASISPEVO-136 ZONE. ПМУ. Техкарта ТС. Перепутаны местами поля Время старта 
- ASISPEVO-138 ZONE. ПМУ. Механизм тех закрытия. При повторном прохождении 
- ASISPEVO-139 ZONE. ПМУ. Механизм тех закрытия. Зона ВГК не открылась при 
- ASISPEVO-143 ZONE. ПМУ. Механизм тех закрытия. Повторное открытие Зоны 
- ASISPEVO-146 ZONE. ПМУ. Механизм тех закрытия. Рад контроль некорректно 
- ASISPEVO-15 SQL. ПМУ / ПФУ. МФАПП . Группировка измерений по событию в н е ш 
- ASISPEVO-155 ПРОД. ПМУ. Техкарта ТС. Таможенное оформление было несколько 
- ASISPEVO - 165 ZONE. ПМУ. Механизм закрытия техническим временем. 
- ASISPEVO-167 ZONE. ПМУ. Реестр ТС. Приходят неправильные статусы 
- ASISPEVO - 235 SQL. ПРОД. ПФУ. Внести в таблицу Comments (Комментарии)
- ASISPEVO-277 SQL. ПМУ / ПФУ. МФАПП . Закрыть зоны для
- ASISPEVO-37 SQL. ПМУ. [Тех3акр] Разработка представления и функций по 
- ASISPEVO-40 SQL. ПМУ. МФАПП . Добавление информации в БД п о к а м е р а м
- ASISPEVO-46 SQL. ПМУ / ПФУ. МФАПП . Закрыть зоны для всех проехавших ТС до 
- ASISPEVO-48 Аналитика . ПМУ. [ ТехЗакр ] Изменение п о с л е д о в а т е л ь н о с т и
- ASISPEVO-59 Zone. ПМУ. Некорректная работа технического
- ASISPEVO-60 SQL. ПМУ. [Тех 3акр ] Подготовить скрипт
- ASISPEVO-65 SQL. ПМУ. МФАПП . Подготовить скрипт обновления информации в БД 
- ASISPEVO-68 ПМУ. Протестировать черные списки от ФТС
- ASISPEVO-74 ПРОД. SQL. ПМУ. Обновить данные по камерам
- ASISPEVO-91 SQL. ПМУ / ПФУ. МФАПП . [ ТехЗакр ] Переименовать статус получения 
- ASISPEVO-92 БЭ. ПМУ. МФАПП . Получение событий из ВА / СВА с типом TC 
- ASISPEVO-97 SQL. ПМУ / ПФУ. Добавить не определённый тип ТС в справочник
- ASISPEVO-99 SQL. ПМУ. [Тех3акр] Добавить значения в справочники по ручному и 
- GIS24EXP-1226 Создание секций [Ноябрь 2024]
- GIS24EXP-1600 Написание инструкции и доработки скрипта
- GIS24EXP - 1716 Написать инструкцию для поддержки по ч и с т к е
- GIS24EXP-2096 [ Прод ] ГИС ЭПД : 500 ошибка при попытке скачать документы
- GIS24EXP - 2125 Удаление пользователей с дева
- GIS24EXP-2180 Привести ИНН пользователей и организаций к нижнему регистру
- GIS24EXP-2251 Корректировка констрейнта на тестовом с т е н д е
- GIS24EXP-2280 ЭОПП : Prod Исправление дублей организаций
- GIS24EXP - 2288 [ Прод ] СберКорус. Нужен список неиспользованных УИДов 
- GIS24EXP-2317 Разработка руководства для 2 ЛТП по выгрузке пула uuid для 
- GIS24EXP-2324 ЭОПП Prod: Правка проблем в части блокировок
- GIS24EXP-2415 Корректировка параметров админки
- GIS24EXP-2444 Написание запроса для проблемных заявок
- G IS24EXP - 2527 Авторизация КЛУ (REST) Изменения в БД
- GIS24EXP-2573 Переезд БД дева
- GIS24EXP-738 Прод. ЭПД. Формирование отчетов на
- SUPASISP-231 SQL. ПФУ. Сгенерировать ТС до актуальной
- SUPASISP-261 Test. ПМУ ПФУ. Реестр. ТехКарта
- SUPASISP-281 SQL. ПМУ / ПФУ. Портал. Реестр. Оптимизировать SQL выгрузки 
- SUPASISP-350 ДЕВ. ПМУ / ПФУ. Реестр ТС. Выгрузка реестра тс, некорректные 
- SUPASISP-405 SQL. ПМУ / ПФУ. Исправить справочники
- SUPASISP-440 SQL. ПМУ / ПФУ. Убрать округление времени из всех функций
- SUPASISP-66 ПФУ. Портал. Главная . Виджеты. Виджет " въезд ) выезд" + Виджет 
'''


def parse_tasks(text):
    pattern = re.compile(r'^(?:-)?\s*(?P<prefix>(?:[A-Z0-9]+(?:\s+[A-Z0-9]+)*))\s*-\s*(?P<num>\d+)\s*(?P<topic>.*)$')
    tasks = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or not line.startswith('-'):
            continue
        content = line.lstrip('-').strip()
        match = pattern.match(content)
        if not match:
            continue
        raw_prefix = match.group('prefix')
        number = match.group('num')
        topic = match.group('topic').strip()
        prefix = re.sub(r'\s+', '', raw_prefix)
        key = f"{prefix}-{number}"
        tasks.append((key, topic))
    return tasks


def write_excel(records, out_path):
    Workbook = ensure_openpyxl_workbook()
    wb = Workbook()
    ws = wb.active
    ws.title = "Tasks"
    ws.append(["Key", "Topic", "Date"])  # header
    for key, topic in records:
        ws.append([key, topic, "10.03.2025"])  # fixed date for all
    wb.save(out_path)


def main():
    records = parse_tasks(TEXT)
    out_path = "/workspace/tasks.xlsx"
    write_excel(records, out_path)
    print(f"Wrote {out_path} with {len(records)} rows")


if __name__ == "__main__":
    main()
