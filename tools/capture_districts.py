"""Cache public state/district options from the source form for local use."""

import concurrent.futures
import json
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup


API = "https://glawebapi.glaonline.com/api/AdmissionRegistration/"
ROOT = Path(__file__).resolve().parents[1]


def options(endpoint):
    with urllib.request.urlopen(API + endpoint, timeout=30) as response:
        source = json.load(response)
    if not isinstance(source, str):
        raise RuntimeError("Unexpected registration option response.")
    soup = BeautifulSoup(source, "lxml")
    return [
        (option.get("value"), option.get_text(strip=True))
        for option in soup.find_all("option")
        if option.get("value") not in {"", "-1", "0"} and option.get_text(strip=True)
    ]


def capture():
    states = options("GetOnlineStudentState?Code=101")
    if not states:
        raise RuntimeError("The source returned no states.")

    def district_state(state):
        code, name = state
        districts = options("GetOnlineStudentCity?Code=" + code)
        return {"name": name, "districts": [name for _, name in districts]}

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        data = list(executor.map(district_state, states))
    order = {"Uttar Pradesh": 0, "Haryana": 1, "Delhi": 2}
    data.sort(key=lambda state: order.get(state["name"], 3))
    (ROOT / "siteassets" / "districts.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8",
    )
    print(f"Captured {len(data)} states and {sum(len(state['districts']) for state in data)} district options.")


if __name__ == "__main__":
    capture()
