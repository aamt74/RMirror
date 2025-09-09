import requests
from enum import Enum
from typing import Dict
from pathlib import Path
from settings import hostname


class EntryType(Enum):
    FILE = 1
    DIRECTORY = 2


class Entry:

    def __init__(self, id, metadata):
        self.ID = id

        # Extract parent ID from metadata
        self.parentID = metadata.split("parent")[1].split("\"")[2]
        if not self.parentID.strip():
            self.parentID = None

        # Extract type info from metadata
        self.type = EntryType.DIRECTORY if "CollectionType" in metadata else EntryType.FILE

        # Extract name from metadata
        self.name = metadata.split("visibleName")[1].split("\"")[2]
        if self.is_file():
            self.name += ".pdf"

        # Completed later once all info is read in
        self.relative_path = None

    def is_top(self) -> bool:
        return self.parentID is None

    def is_file(self) -> bool:
        return self.type == EntryType.FILE

    def is_dir(self) -> bool:
        return self.type == EntryType.DIRECTORY


class EntryUtils:

    @staticmethod
    def CompletePath(entry: Entry, entries_map: Dict[str, Entry]) -> Path:
        result = Path(entry.name)
        curr_entry = entry
        while not curr_entry.is_top():
            curr_entry = entries_map[curr_entry.parentID]
            curr_path = Path(curr_entry.name)
            result = curr_path.joinpath(result)
        return result

    @staticmethod
    def DownloadPdf(entry: Entry) -> Path:
        url = f"http://{hostname}/download/{entry.ID}/placeholder"
        r = requests.get(url, stream=True)
        output_file = "placeholder"
        with open(output_file, "wb") as file:
            for chunk in r.iter_content(chunk_size=8192):  # Legge il file a blocchi
                file.write(chunk)
        return Path(output_file)
