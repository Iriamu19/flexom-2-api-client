class Sensor:
    def __init__(self, type_id: str, name: str):
        self.type_id = type_id
        self.name = name

    def __repr__(self):
        return f"Sensor(type_id='{self.type_id}', name='{self.name}')"
