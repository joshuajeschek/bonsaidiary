from dataclasses import dataclass, asdict
from datetime import datetime
import json

@dataclass
class Diary:
    created: str
    modified: str
   
    def __init__(self):
        self.created = datetime.now().isoformat()
        self.modified = datetime.now().isoformat()

    def update(self):
        self.modified = datetime.now().isoformat()

    def save(self, location:str):
        self.update()
        print(json.dumps(asdict(self)))
        with open(location, 'w') as f:
            f.write(json.dumps(asdict(self)))

