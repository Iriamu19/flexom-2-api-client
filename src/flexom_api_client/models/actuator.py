class Actuator:
    def __init__(
        self,
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
    ):
        self.actuator_id = actuator_id
        self.it_id = it_id
        self.value = value
        self.timestamp = timestamp
        self.progressive = progressive
        self.color_enable = color_enable
        self.min_value = min_value
        self.max_value = max_value
        self.activated = activated
        self.actionning_representation = actionning_representation
        self.com_type = com_type

    def __repr__(self):
        return (
            f"Actuator(actuatorId={self.actuator_id}, itId={self.it_id}, "
            f"value={self.value}, timestamp={self.timestamp}, progressive={self.progressive}, "
            f"colorEnable={self.color_enable}, minActionValue={self.min_value}, maxActionValue={self.max_value}, "
            f"activated={self.activated}, actionningRepresentation={self.actionning_representation}, comType={self.com_type})"
        )
