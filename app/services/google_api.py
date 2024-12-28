from datetime import datetime
from copy import deepcopy

from aiogoogle import Aiogoogle

from app.constants.constants import MAX_ROWS, MAX_COLS
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'


TABLE_VALUES_TEMPLATE = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

SPREADSHEET_TEMPLATE: dict = dict(
    properties=dict(
        title='',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=MAX_ROWS,
            columnCount=MAX_COLS,
        )
    ))]
)

ERROR_MESSAGE = (
    'Данные не помещаются в таблицу. '
    'Габариты вставляемой таблицы: {} строк, {} колонок. '
    'Максимальное число строк: {}, максимальное число колонок: {}.'
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = deepcopy(SPREADSHEET_TEMPLATE)
    spreadsheet_body['properties']['title'] = f'Отчёт от {now_date_time}'
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    TABLE_VALUES_TEMPLATE[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *TABLE_VALUES_TEMPLATE,
        *[list(map(
            str,
            [project['name'], project['duration'], project['description']])
        ) for project in projects],
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    range_rows = len(table_values)
    range_cols = len(table_values[2])
    row_count = (
        SPREADSHEET_TEMPLATE['sheets'][0][
            'properties'
        ]['gridProperties']['rowCount']
    )
    column_count = (
        SPREADSHEET_TEMPLATE['sheets'][0][
            'properties'
        ]['gridProperties']['columnCount']
    )

    if range_rows * range_cols > row_count * column_count:
        raise ValueError(ERROR_MESSAGE.format(
            range_rows, range_cols,
            row_count, column_count
        ))

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{range_rows}C{range_cols}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def get_projects_by_duration(projects):
    return sorted(
        [{
            'name': project.name,
            'duration': project.close_date - project.create_date,
            'description': project.description
        } for project in projects], key=lambda x: x['duration'])
