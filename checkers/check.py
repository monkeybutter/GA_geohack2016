import json

class Checker:
    def __init__(self, path):
        self.path = path
        self.type = "Generic"
        self.result = None

    @property
    def dict(self):
        return {"result": self.result, "file": self.path, "type": self.type}

    def __str__(self):
        return "{} checker for file: {}" % (self.type, self.path)

    def to_json(self):
        return json.dumps(self.dict)
