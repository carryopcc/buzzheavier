import re
from requests import get
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class URLInput(BaseModel):
    text: str

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

@app.post("/extract")
def extract_links(data: URLInput):
    urls = re.findall(r'https?://buzzheavier\.com/\S+', data.text)
    direct_links = []
    failed = []

    for u in urls:
        try:
            dl = get_buzzheavier_url(u)
            if not dl:
                raise Exception("No redirect")
            direct_links.append(dl)
        except:
            failed.append(u)

    return {
        "success": direct_links,
        "failed": failed
    }
