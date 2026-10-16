import os
import re
import time
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    raise SystemExit("Установи переменную окружения GITHUB_TOKEN")

REPO = "egogoga/habitflow"
FILE = "use_cases.md"
LABEL_MVP = "mvp"                         
# ==================

API = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
}

# Читаем файл
with open(FILE, encoding="utf-8") as f:
    text = f.read()

# Регуляркой ловим строки вида "1. [MVP] Как ...", "2. Как ..."
pattern = re.compile(r"^(\d+)\.\s*(\[MVP\])?\s*(.+)$", re.MULTILINE)

matches = pattern.findall(text)
print(f"Найдено use case: {len(matches)}")

for num, mvp_flag, body in matches:
    title = f"UC-{int(num):02d}: {body[:70]}"
    payload = {
        "title": title,
        "body": body.strip(),
    }
    if mvp_flag:
        payload["labels"] = [LABEL_MVP]

    r = requests.post(f"{API}/repos/{REPO}/issues",
                      headers=HEADERS, json=payload)

    if r.status_code == 201:
        print(f"✓ {title}")
    else:
        print(f"✗ {title} → {r.status_code}: {r.text}")

    time.sleep(0.5)  # чтобы не упереться в rate limit