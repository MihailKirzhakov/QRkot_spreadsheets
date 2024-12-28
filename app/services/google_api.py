from datetime import datetime
from copy import deepcopy

from aiogoogle import Aiogoogle

from app.constants.constants import MAX_ROWS
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'


TABLE_VALUES_TEMPLATE = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

range_cols = len(TABLE_VALUES_TEMPLATE[2])

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
            columnCount=range_cols,
        )
    ))]
)

ERROR_MESSAGE = (
    'Данные не помещаются в таблицу. '
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
        TABLE_VALUES_TEMPLATE[0],
        *[list(map(
            str,
            [project['name'], project['duration'], project['description']])
        ) for project in projects],
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    range_rows = (len(TABLE_VALUES_TEMPLATE) + len(projects))

    if range_rows * range_cols > MAX_ROWS * range_cols:
        raise ValueError(ERROR_MESSAGE.format(MAX_ROWS, range_cols))

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
