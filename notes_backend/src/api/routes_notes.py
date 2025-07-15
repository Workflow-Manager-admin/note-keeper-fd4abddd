from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models, auth
from .database import get_db

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

# PUBLIC_INTERFACE
@router.get("/", response_model=list[schemas.NoteOut])
def list_notes(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    List all notes belonging to the current user.
    """
    notes = db.query(models.Note).filter(models.Note.owner_id == current_user.id).order_by(models.Note.updated_at.desc()).all()
    return notes

# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.NoteOut, status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Create a new note for user.
    """
    db_note = models.Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# PUBLIC_INTERFACE
@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Get a single note by ID, must be owned by current user.
    """
    note = db.query(models.Note).filter_by(id=note_id, owner_id=current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: int, patch: schemas.NoteUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Update note (title/content).
    """
    note = db.query(models.Note).filter_by(id=note_id, owner_id=current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if patch.title is not None:
        note.title = patch.title
    if patch.content is not None:
        note.content = patch.content
    db.commit()
    db.refresh(note)
    return note

# PUBLIC_INTERFACE
@router.delete("/{note_id}", response_model=schemas.NoteOut)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Delete a note (must be owned by user).
    """
    note = db.query(models.Note).filter_by(id=note_id, owner_id=current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return note
