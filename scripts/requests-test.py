# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///
import requests

# The Forge region ID 10000002
def main() -> None:
    payload = {
        "datasource": 'tranquility',
        "type_id": 34,
    }
    r = requests.get("https://esi.evetech.net/latest/markets/10000002/history/", params=payload)
    print(r)
    print(r.json())


if __name__ == "__main__":
    main()
