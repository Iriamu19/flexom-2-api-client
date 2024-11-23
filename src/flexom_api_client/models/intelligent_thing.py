from .actuator import Actuator
from .sensor import Sensor


class IntelligentThing:
    def __init__(
        self,
        id_: str,
        name: str,
        sensors: list[Sensor],
        actuators: list[Actuator],
        zone_name: str,
        zone_type: str,
    ):
        self.id = id_
        self.name = name
        self.sensors = sensors
        self.actuators = actuators
        self.zone_name = zone_name
        self.zone_type = zone_type

    def __repr__(self):
        return (
            f"IntelligentThing(id='{self.id}', name='{self.name}', sensors={self.sensors}, "
            f"actuators={self.actuators}, zone_name='{self.zone_name}', zone_type='{self.zone_type}')"
        )
