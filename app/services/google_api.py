from typing import Optional
from aiogoogle import Aiogoogle
from datetime import datetime
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(
        wrapper_services: Aiogoogle
) -> Optional[str]:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт на {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {'properties':{'sheetType': 'GRID',
                           'sheetId': 0,
                           'title':'Лист1',
                           'gridProperties': {'rowCount': 100, 
                                              'columnCount': 11}
                           }
            }
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(fileId=spreadsheet_id, json=permissions_body, fields="id")
    )


async def spreadsheets_update_value(
        spreadsheet_id: str, reservations: list, wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for res in reservations:
        new_row = [
            str(res.name),
            str(res.close_date - res.create_date),
            str(res.description)
        ]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )

