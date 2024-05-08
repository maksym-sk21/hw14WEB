from typing import List, Type
from sqlalchemy.orm import Session
from ..database.models import Contact
from ..schemas import ContactCreate, ContactUpdate
from ..database.models import User
from sqlalchemy import and_


def create_contact(db: Session, contact: ContactCreate, current_user: User) -> Contact:
    """
    Create a new contact in the database for the current user.

    :param db: SQLAlchemy database session.
    :type db: Session
    :param contact: Data schema for creating the contact.
    :type contact: ContactCreate
    :param current_user: The current user on behalf of whom the contact is created.
    :type current_user: User
    :return: The created contact object.
    :rtype: Contact
    """
    db_contact = Contact(**contact.dict(), user_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, user: User, skip: int = 0, limit: int = 10) -> List[Type[Contact]]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id)).offset(skip).limit(limit).all()


def get_contact(db: Session, user: User, contact_id: int) -> Type[Contact]:
    """
    Retrieves a single note with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


def update_contact(db: Session, contact_id: int, user: User, contact: ContactUpdate) -> Type[Contact]:
    """
    Update an existing contact in the database.

    :param db: SQLAlchemy database session.
    :type db: Session
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param user: The user who owns the contact.
    :type user: User
    :param contact: Data schema containing updated contact information.
    :type contact: ContactUpdate
    :return: The updated contact object if found, otherwise None.
    :rtype: Contact | None
    """
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        for attr, value in contact.dict().items():
            setattr(db_contact, attr, value) if value else None
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, user: User, contact_id: int) -> bool:
    """
    Delete a contact from the database.

    :param db: SQLAlchemy database session.
    :type db: Session
    :param user: The user who owns the contact to be deleted.
    :type user: User
    :param contact_id: The ID of the contact to be deleted.
    :type contact_id: int
    :return: True if the contact was successfully deleted, False otherwise.
    :rtype: bool
    """
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False
