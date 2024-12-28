from datetime import datetime
from copy import deepcopy

from aiogoogle import Aiogoogle

from app.constants.constants import ConstantNumbers
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'

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
            rowCount=ConstantNumbers.MAX_ROWS,
            columnCount=ConstantNumbers.MAX_COLS,
        )
    ))]
)

TABLE_VALUES_TEMPLATE = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = deepcopy(SPREADSHEET_TEMPLATE)
    spreadsheet_body['properties']['title'] = f'Отчёт от {now_date_time}'
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    report_url = response['spreadsheetUrl']
    return spreadsheet_id, report_url


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
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        TABLE_VALUES_TEMPLATE[0][1] + now_date_time,
        *[list(map(
            str,
            [project['name'], project['duration'], project['description']])
        ) for project in projects],
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    if len(projects) > ConstantNumbers.MAX_ROWS:
        raise ValueError(
            'Данные не помещаются в таблицу. '
            f'Максимальное число строк {ConstantNumbers.MAX_ROWS}.'
        )

    range_end_row = len(table_values)
    range_end_col = ConstantNumbers.MAX_COLS

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{range_end_row}C{range_end_col}',
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
