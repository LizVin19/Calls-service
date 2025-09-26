from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from pathlib import Path

from app.db import get_session
from app import models
from app.config import settings

router = APIRouter(prefix='/calls', tags=['recordings'])


@router.post('/{call_id}/recording')
async def upload_recording(call_id: int, file: UploadFile = File(...),
                           session: AsyncSession = Depends(get_session)):
    call = await session.get(models.Call, call_id)
    if not call:
        raise HTTPException(status_code=404, detail='Call not found')

    allowed = {'audio/wav', 'audio/x-wav', 'audio/mpeg', 'audio/mp3'}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail='Unsupported file type')

    Path(settings.media_root).mkdir(parents=True, exist_ok=True)
    if 'wav' in file.content_type or (file.filename and file.filename.lower().endswith('.wav')):
        ext = '.wav'
    else:
        ext = '.mp3'
    filename = f'{uuid4().hex}{ext}'
    full_path = Path(settings.media_root) / filename

    data = await file.read()
    with open(full_path, 'wb') as f:
        f.write(data)

    rec = models.Recording(call_id=call_id, filename=filename)
    session.add(rec)
    call.status = models.CallStatus.processing
    await session.commit()
    await session.refresh(rec)

    from app.workers.tasks import process_recording_task
    process_recording_task(rec.id)

    return {'recording_id': rec.id, 'filename': filename}

