from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app import models, schemas

from typing import List
from fastapi import Query
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

router = APIRouter(prefix='/calls', tags=['calls'])


@router.post('/', response_model=dict)
async def create_call(payload: schemas.CallCreate, session: AsyncSession = Depends(get_session)):
    call = models.Call(
        caller=payload.caller,
        receiver=payload.receiver,
        started_at=payload.started_at,
        status=models.CallStatus.created
    )
    session.add(call)
    await session.commit()
    await session.refresh(call)
    return {'id': call.id}


@router.get('/', response_model=List[schemas.CallOut])
async def list_calls(
        q: str | None = Query(None, description='Поиск по номеру (caller/receiver)'),
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0),
        session: AsyncSession = Depends(get_session)
):
    stmt = (
        select(models.Call)
        .options(selectinload(models.Call.recording))
        .order_by(models.Call.id.desc())
        .limit(limit)
        .offset(offset)
    )

    if q:
        like = f'%{q}%'
        stmt = (
            select(models.Call)
            .where(or_(models.Call.caller.ilike(like), models.Call.receiver.ilike(like)))
            .options(selectinload(models.Call.recording))
            .order_by(models.Call.id.desc())
            .limit(limit)
            .offset(offset)
        )

    res = await session.execute(stmt)
    return res.scalars().all()


@router.get('/{call_id}/', response_model=schemas.CallOut)
async def get_call(call_id: int, session: AsyncSession = Depends(get_session)):
    stmt = (
        select(models.Call)
        .options(selectinload(models.Call.recording))
        .where(models.Call.id == call_id)
    )
    result = await session.execute(stmt)
    call = result.scalars().first()
    if not call:
        raise HTTPException(status_code=404, detail='Call not found')
    return call
