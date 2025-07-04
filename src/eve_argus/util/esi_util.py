from pathlib import Path
from typing import Any
from eve_argus.models import esi_data as ED
from eve_argus.models.market_history_summary import MarketHistorySummary
import csv


def market_history_summary(region_id:int, type_id:int,periods:list[int],data:list[ED.MarketHistory])->dict[int:MarketHistorySummary]:
    pass

def market_history_save_to_csv(region_id:int, type_id:int,data:list[ED.MarketHistory],dirpath:Path)->None:
    """
    Save market history data to a CSV file.
    
    Args:
        region_id (int): The ID of the region.
        type_id (int): The ID of the type.
        data (list[ED.MarketHistory]): List of market history data.
        dirpath (Path): The Path of the directory to save the data to.
    """
    filename = f"{region_id}_{type_id}_market_history.csv"
    filepath = dirpath / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    with filepath.open('w', encoding='utf-8') as file:
        writer=csv.DictWriter(file, fieldnames=ED.MarketHistory.__annotations__.keys())
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)  