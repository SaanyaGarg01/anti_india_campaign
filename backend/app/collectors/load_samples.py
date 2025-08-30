import os
import json
import time
import requests


def main():
    api = os.getenv("API_BASE_URL", "http://localhost:8000") + "/api/posts/"
    data_dir = os.getenv("DATA_DIR", "/data")
    files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    for f in files:
        path = os.path.join(data_dir, f)
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        r = requests.post(api, json=payload, timeout=10)
        print(f"POST {f} -> {r.status_code}")
        time.sleep(0.2)


if __name__ == "__main__":
    main()


