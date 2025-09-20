# diagnose_404.py — pinpoints 404 causes in RAG setup
import os, json, sys, requests
from dotenv import load_dotenv

def p(title, x): print(f"\n=== {title} ===\n{x}")

load_dotenv()
errors = []

# 0) Show the key env vars you're using (no secrets)
p("ENV", json.dumps({
    "PROJECT_ENDPOINT": os.getenv("PROJECT_ENDPOINT"),
    "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "CHAT_DEPLOYMENT": os.getenv("CHAT_DEPLOYMENT") or os.getenv("MODEL_DEPLOYMENT"),
    "EMBEDDING_DEPLOYMENT": os.getenv("EMBEDDING_DEPLOYMENT"),
    "SEARCH_ENDPOINT": os.getenv("SEARCH_ENDPOINT"),
    "SEARCH_INDEX": os.getenv("SEARCH_INDEX"),
}, indent=2))

# 1) Azure OpenAI (resource) — list deployments directly
aoai_ep = (os.getenv("AZURE_OPENAI_ENDPOINT") or "").rstrip("/")
aoai_key = os.getenv("AZURE_OPENAI_API_KEY")
if aoai_ep and aoai_key:
    url = f"{aoai_ep}/openai/deployments?api-version=2024-10-21"
    p("AOAI LIST URL", url)
    r = requests.get(url, headers={"api-key": aoai_key})
    p("AOAI LIST STATUS", r.status_code)
    try: p("AOAI LIST BODY", json.dumps(r.json(), indent=2)[:2000])
    except Exception: p("AOAI LIST RAW", r.text[:2000])
else:
    errors.append("Missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY")

# 2) Project endpoint (Foundry) — optional but helpful
proj_ep = os.getenv("PROJECT_ENDPOINT")
if proj_ep:
    # Simple ping to see if project URL is reachable
    ping = proj_ep.rstrip("/") + "/connections?api-version=2024-10-01-preview"
    p("PROJECT PING URL", ping)
    try:
        # Expect 401/403 without AAD token; we only care it's not 404/DNS
        r = requests.get(ping, timeout=10)
        p("PROJECT PING STATUS", r.status_code)
    except Exception as e:
        p("PROJECT PING ERROR", repr(e))

# 3) Try an OpenAI “list models” call via resource (often returns deployments)
try:
    from openai import OpenAI
    if aoai_ep and aoai_key:
        oai = OpenAI(api_key=aoai_key, base_url=aoai_ep.rstrip("/") + "/openai/v1/")
        models = oai.models.list()
        names = [m.id for m in models.data]
        p("OpenAI models.list()", names[:20])
except Exception as e:
    p("OpenAI models.list() error", repr(e))

# 4) Azure Cognitive Search — does the index exist?
se = os.getenv("SEARCH_ENDPOINT")
sk = os.getenv("SEARCH_API_KEY")
sidx = os.getenv("SEARCH_INDEX")
if se and sk:
    url = f"{se.rstrip('/')}/indexes?api-version=2024-07-01"
    p("SEARCH LIST INDEXES URL", url)
    r = requests.get(url, headers={"api-key": sk})
    p("SEARCH LIST STATUS", r.status_code)
    try:
        data = r.json()
        names = [i.get("name") for i in data.get("value", [])]
        p("SEARCH INDEXES", names)
        if sidx and sidx not in names:
            p("SEARCH WARNING", f"Configured SEARCH_INDEX '{sidx}' was not found.")
    except Exception:
        p("SEARCH RAW", r.text[:2000])
else:
    errors.append("Missing SEARCH_ENDPOINT or SEARCH_API_KEY")

# 5) Final hint: the two most common mismatches
p("Common Fixes",
"""- If your deployment name isn't in AOAI LIST or models.list(), you're calling the wrong AOAI resource/region, or the name is off.
- If the portal Playground works but local fails: your local code uses the AOAI resource endpoint, while the portal project is connected to a different AOAI resource. Align the resource or switch the project’s default connection.
- If SEARCH_INDEX isn't listed, point to the Search service where the vector index actually lives (or fix the index name).""")

if errors:
    p("Missing required env", errors)
