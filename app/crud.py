import string, random
from sqlalchemy.orm import Session
from . import models

def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_url(db: Session, original_url: str):
    short_id = generate_short_id()
    while db.query(models.URL).filter(models.URL.short_id == short_id).first():
        short_id = generate_short_id()
    db_url = models.URL(original_url=original_url, short_id=short_id)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url_by_short_id(db: Session, short_id: str):
    return db.query(models.URL).filter(models.URL.short_id == short_id).first()

def create_click(db: Session, url_id: int, ip: str, user_agent: str):
    click = models.Click(url_id=url_id, ip=ip, user_agent=user_agent)
    db.add(click)
    db.commit()
    db.refresh(click)
    return click

def get_clicks(db: Session, url_id: int):
    return db.query(models.Click).filter(models.Click.url_id == url_id).all()
