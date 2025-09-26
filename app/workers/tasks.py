import os
from pathlib import Path
from pydub import AudioSegment, silence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.workers.celery_app import celery
from app.models import Recording, Call, CallStatus


SYNC_DB_URL = os.getenv('SYNC_DATABASE_URL')
MEDIA_ROOT = os.getenv('MEDIA_ROOT')

engine = create_engine(SYNC_DB_URL, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


@celery.task(name='process_recording_task')
def process_recording_task(recording_id: int):
    ''' Считает длительность, делает псевдотранскрипт и детект тишины '''
    with SessionLocal() as session:
        rec: Recording | None = session.get(Recording, recording_id)
        if not rec:
            return

        file_path = Path(MEDIA_ROOT) / rec.filename
        audio = AudioSegment.from_file(file_path)

        duration_sec = int(len(audio) // 1000)
        transcription = f'Detected speech fragment: ... ({min(20, duration_sec)}s)'
        silences = silence.detect_silence(
            audio, min_silence_len=300, silence_thresh=audio.dBFS - 5
        )

        rec.duration_sec = duration_sec
        rec.transcription = transcription
        rec.silence_ranges = silences or []

        call = session.get(Call, rec.call_id)
        if call:
            call.status = CallStatus.ready

        session.commit()