from ..models import Actuator, UbiantClient


class ActuatorService:
    def __init__(self):
        self.ubiant_client = UbiantClient()

    def get_all_actuators(self):
        actuators = []
        api_response = self.ubiant_client.get_actuators()
        for item in api_response:
            # Retrieve all relevant fields
            it_id = item.get("itId") or item["state"].get("itId")
            actuator_id = item.get("actuatorId") or item["state"].get("actuatorId")
            state = item.get("state", {})

            value = state.get("value")
            timestamp = state.get("timeStamp")
            progressive = state.get("progressive")
            color_enable = state.get("colorEnable")
            min_value = state.get("minActionValue")
            max_value = state.get("maxActionValue")
            activated = item.get("activated")
            actionning_representation = item.get("actionningRepresentation")
            com_type = item.get("com_type")

            # Instantiate an Actuator with additional fields
            actuators.append(
                Actuator(
                    actuator_id,
                    it_id,
                    value,
                    timestamp,
                    progressive,
                    color_enable,
                    min_value,
                    max_value,
                    activated,
                    actionning_representation,
                    com_type,
                )
            )

        return actuators

    def change_value(self, actuator: Actuator, value):
        self.ubiant_client.set_multiple_actuators_value(
            it_id=actuator.it_id, actuator_id=actuator.actuator_id, value=value
        )
