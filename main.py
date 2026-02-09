from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from requests import get
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_buzzheavier_url(bh_link):
    bh_link = bh_link.strip().split("#")[0]
    headers = {
        "accept": "*/*",
        "hx-request": "true",
        "hx-current-url": bh_link,
        "referer": bh_link,
        "user-agent": "Mozilla/5.0"
    }
    r = get(bh_link + "/download", headers=headers, timeout=20)
    return r.headers.get("Hx-Redirect")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": None}
    )

@app.post("/extract", response_class=HTMLResponse)
def extract(request: Request, urls: str = Form(...)):
    found_urls = re.findall(r'https?://buzzheavier\.com/\S+', urls)
    results = []

    for u in found_urls:
        try:
            dl = get_buzzheavier_url(u)
            if not dl:
                raise Exception()
            results.append(dl)
        except:
            results.append(f"FAILED: {u}")

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": results}
    )
    return {
        "success": direct_links,
        "failed": failed
    }
