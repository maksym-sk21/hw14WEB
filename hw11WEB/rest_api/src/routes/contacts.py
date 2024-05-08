from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..repository.contacts import create_contact, get_contact, get_contacts, update_contact, delete_contact
from ..schemas import Contact, ContactCreate, ContactUpdate
from ..database.db import SessionLocal
from sqlalchemy.orm import Session
from ..services.auth import Auth
from ..database.models import User
from fastapi_limiter.depends import RateLimiter

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/contacts/", response_model=Contact)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db),
                       current_user: User = Depends(Auth.get_current_user)):
    return create_contact(db, contact, current_user)


@router.get("/contacts/", response_model=List[Contact])
def get_all_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                     current_user: User = Depends(Auth.get_current_user)):
    return get_contacts(db, current_user, skip=skip, limit=limit)


@router.get("/contacts/{contact_id}", response_model=Contact)
def get_single_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(Auth.get_current_user)):
    contact = get_contact(db, current_user, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=Contact)
def update_single_contact(
    contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db),
        current_user: User = Depends(Auth.get_current_user)
):
    updated_contact = update_contact(db, contact_id, current_user, contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/contacts/{contacts_id}")
def delete_single_contact(contact_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(Auth.get_current_user)):
    success = delete_contact(db, current_user, contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}


@router.get("/", response_model=List[Contact], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        current_user: User = Depends(Auth.get_current_user)):
    contacts = get_contacts(db, current_user, skip, limit)
    return contacts
