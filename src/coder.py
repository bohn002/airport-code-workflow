"""Get codes from wiki and clean them"""
from bs4 import BeautifulSoup
import requests
import json

url = "https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_"


def get_page(url, index_letter):
    return requests.get(f"{url}{index_letter}")


codes_dict = {"items": []}


def dump_json(code_data):
    with open("workflow/airport_codes.json", "w", encoding="utf-8") as file:
        json.dump(code_data, file)


def get_codes():
    """Get Codes and format them"""
    index_letter = "A"
    while True:
        page_data = get_page(url, index_letter)
        soup = BeautifulSoup(page_data.content, "html.parser")
        code_list_raw = []
        code_list = []
        table_data = soup.select("table.wikitable tbody tr")
        for row in table_data:
            code_list_raw.append(row.get_text())
        code_list_raw = code_list_raw[1:]
        for r in code_list_raw:
            z = list(filter(lambda x: not x.startswith("-"), r.split("\n")))
            z = z[1:]
            if len(z) > 1:
                code_list.append(z)

        for code in code_list:
            iata_code = code[0]
            station_name = code[2]
            station_location = code[3]
            codes_dict["items"].append(
                {
                    "arg": iata_code,
                    "autocomplete": iata_code,
                    "icon": {"path": "./plane.png"},
                    "subtitle": station_location,
                    "title": f"{iata_code} - {station_name}",
                    "uid": iata_code
                }
            )
        index_letter = chr(ord(index_letter) + 1)
        if index_letter > "Z":
            break
    dump_json(codes_dict)


if __name__ == "__main__":
    get_codes()
