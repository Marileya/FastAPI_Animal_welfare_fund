from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import (DonationCreate, DonationDBfull,
                                  DonationDBpart)
from app.services.investing import investing


router = APIRouter()


@router.get('/',
            response_model=list[DonationDBfull],
            dependencies=[Depends(current_superuser)]
            )
async def get_all_donats(
    session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.post('/',
             response_model=DonationDBpart,
             response_model_exclude_none=True,)
async def create_donat(
        donat: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    new_donat = await donation_crud.create(donat, session, user)
    new_donat = await investing(
        obj=new_donat,
        model=CharityProject,
        session=session)

    return new_donat


@router.get('/my',
            response_model=list[DonationDBpart])
async def get_donat_for_user(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    donats = await donation_crud.get_by_user(user, session)
    return donats
