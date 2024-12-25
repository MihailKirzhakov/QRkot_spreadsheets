from datetime import datetime

from aiogoogle import Aiogoogle

from app.api.validators import validate_data_size
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
            rowCount=100,
            columnCount=11,
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
    spreadsheet_body = SPREADSHEET_TEMPLATE.copy()
    spreadsheet_body['properties']['title'] = f'Отчёт от {now_date_time}'
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    report_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
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


def create_range_r1c1(start_row, start_col, num_rows, num_cols):
    end_row = start_row + num_rows - 1
    end_col = start_col + num_cols - 1
    return f"R{start_row}C{start_col}:R{end_row}C{end_col}"


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        TABLE_VALUES_TEMPLATE[0][:1] + [now_date_time],
        *[list(map(
            str,
            [project['name'], project['duration'], project['description']])
        ) for project in projects],
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    validate_data_size(
        table_values,
        ConstantNumbers.MAX_ROWS,
        ConstantNumbers.MAX_COLS
    )
    num_rows = len(table_values)
    num_cols = len(table_values[0]) if num_rows > 0 else 0
    range = create_range_r1c1(
        ConstantNumbers.START_ROW,
        ConstantNumbers.START_COL,
        num_rows,
        num_cols
    )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def get_projects_by_duration(projects):
    project_list = []
    for project in projects:
        project_list.append({
            'name': project.name,
            'duration': project.close_date - project.create_date,
            'description': project.description
        })
    project_list = sorted(project_list, key=lambda x: x['duration'])
    return project_list
