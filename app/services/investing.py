from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def investing(
        obj,
        model,
        session: AsyncSession,
):
    obj_diff = obj.full_amount - obj.invested_amount

    collections = await session.execute(
        select(model).where(model.close_date.is_(None)))
    collections = collections.scalars().all()

    new_obj = {}
    new_elem = {}
    for elem in collections:

        if not obj_diff:
            break

        elem_amount = elem.full_amount
        elem_invested = elem.invested_amount
        elem_diff = elem_amount - elem_invested

        if elem_diff >= obj_diff:
            new_elem['invested_amount'] = elem_invested + obj_diff
            if elem_diff == obj_diff:
                new_elem['fully_invested'] = True
                new_elem['close_date'] = datetime.now()
            obj_diff = 0

        else:
            new_elem['invested_amount'] = elem_amount
            new_elem['fully_invested'] = True
            new_elem['close_date'] = datetime.now()
            obj_diff -= elem_diff

        for key, value in new_elem.items():
            setattr(elem, key, value)
        session.add(elem)

    new_obj['invested_amount'] = obj.full_amount - obj_diff
    if not obj_diff:
        new_obj['fully_invested'] = True
        new_obj['close_date'] = datetime.now()

    for key, value in new_obj.items():
        setattr(obj, key, value)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj
