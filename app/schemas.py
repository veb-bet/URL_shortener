from pydantic import BaseModel

class URLCreate(BaseModel):
    url: str

class URLResponse(BaseModel):
    original_url: str
    short_url: str

class ClickDetail(BaseModel):
    timestamp: str
    ip: str
    user_agent: str

class URLAnalytics(BaseModel):
    original_url: str
    short_url: str
    clicks: int
    click_details: list[ClickDetail]
