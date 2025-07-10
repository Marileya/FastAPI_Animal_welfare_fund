from datetime import datetime
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_ability_to_delete, check_close_date,
                                check_full_amount, check_name_duplicate,
                                check_project_exists)

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.models import Donation
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)
from app.services.investing import investing


router = APIRouter()


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post('/',
             response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)],
             response_model_exclude_none=True,)
async def create_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    new_project = await investing(
        obj=new_project,
        model=Donation,
        session=session)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_ability_to_delete(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(project_id, session)
    await check_close_date(project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount(project_id, obj_in.full_amount, session)
        if obj_in.full_amount == project.invested_amount:
            project.fully_invested = True
            project.close_date = datetime.now()

    project = await charity_project_crud.update(project, obj_in, session)
    return project
