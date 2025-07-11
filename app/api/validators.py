from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект с таким id не найден!'
        )
    return project


async def check_ability_to_delete(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка наличия внесенной суммы в проект при удалении."""
    project = await check_project_exists(project_id, session)
    if project.invested_amount or project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_full_amount(
        project_id: int,
        new_full_amount: int,
        session: AsyncSession
) -> None:
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Нелья установить значение full_amount меньше уже '
                    'вложенной суммы.')
        )


async def check_close_date(
        project_id: int,
        session: AsyncSession
) -> None:
    project = await charity_project_crud.get(project_id, session)
    if project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
