from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import AsyncSessionLocal, init_db
from .models import Note
from .schemas import NoteCreate, NoteOut

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/notes", response_model=NoteOut)
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    new_note = Note(text=note.text)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

@app.get("/notes", response_model=list[NoteOut])
async def get_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(Note.__table__.select())
    return result.scalars().all()
