from ..models import IntelligentThing, UbiantClient
from .actuator_service import ActuatorService


class IntelligentThingService:
    def __init__(self):
        self.ubiant_client = UbiantClient()

    def get_all_intelligent_things(self) -> list:
        actuator_service = ActuatorService()
        things = []
        its_response = self.ubiant_client.get_all_intelligent_things()
        actuators = actuator_service.get_all_actuators()
        for item in its_response:
            # Extracting basic info
            id_ = item["id"]
            name = item["name"]
            zone_info = item["zoneInformation"]
            zone_name = zone_info["name"]
            zone_type = zone_info["type"]

            # Extracting actuators

            thing = IntelligentThing(
                id_=id_,
                name=name,
                sensors=[],
                actuators=[act for act in actuators if act.it_id == id_],
                zone_name=zone_name,
                zone_type=zone_type,
            )
            things.append(thing)

        return things

    def get_it_with_actuators(self, its: list[IntelligentThing]):
        its_with_actuators = [it for it in its if len(it.actuators) > 0]
        return its_with_actuators
