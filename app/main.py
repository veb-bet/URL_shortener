from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

BASE_URL = "http://127.0.0.1:8000"

@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(url_data: schemas.URLCreate, db: Session = Depends(get_db)):
    db_url = crud.create_url(db, url_data.url)
    return schemas.URLResponse(
        original_url=db_url.original_url,
        short_url=f"{BASE_URL}/{db_url.short_id}"
    )

@app.get("/{short_id}")
def redirect_to_url(short_id: str, request: Request, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_short_id(db, short_id)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # логируем клик
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    crud.create_click(db, db_url.id, ip, user_agent)
    
    # увеличиваем счетчик
    db_url.clicks += 1
    db.commit()
    
    return RedirectResponse(db_url.original_url)

@app.get("/analytics/{short_id}", response_model=schemas.URLAnalytics)
def url_analytics(short_id: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_short_id(db, short_id)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    clicks = crud.get_clicks(db, db_url.id)
    click_details = [
        schemas.ClickDetail(timestamp=str(c.timestamp), ip=c.ip, user_agent=c.user_agent)
        for c in clicks
    ]
    
    return schemas.URLAnalytics(
        original_url=db_url.original_url,
        short_url=f"{BASE_URL}/{db_url.short_id}",
        clicks=db_url.clicks,
        click_details=click_details
    )
