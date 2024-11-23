import rich_click as click
from rich import print
from rich.table import Table
from rich.tree import Tree

from .models import UbiantClient
from .services import ActuatorService, IntelligentThingService


@click.group()
def cli():
    return None


@cli.command()
def actuators_tree_view():
    ub_client = UbiantClient()
    it_service = IntelligentThingService()
    zone_names = ub_client.get_all_zone_names()  # zone_names = room names
    intelligent_things = it_service.get_all_intelligent_things()
    tree = Tree("My Home")
    for zone_name in zone_names:
        zone_node = tree.add("[red]" + zone_name)
        its_from_current_zone = [
            it for it in intelligent_things if it.zone_name == zone_name
        ]
        for it in its_from_current_zone:
            it_table = Table(show_header=False)
            it_table.add_row(it.name, it.id)
            it_node = zone_node.add(it_table)
            for actuator in it.actuators:
                actuator_table = Table(show_header=False)
                actuator_table.add_row(actuator.actuator_id, str(actuator.value))
                it_node.add(actuator_table)

    print(tree)


@cli.command()
@click.argument("actuator_id")
@click.argument("value")
@click.option("--it_id", required=False, help="Intelligent Thing ID")
def set_actuator_value(it_id, actuator_id, value):
    if it_id is not None:
        ub_client = UbiantClient()
        ub_client.set_multiple_actuators_value(
            actuator_id=actuator_id, it_id=it_id, value=value
        )
    else:
        print("coucou")
        actuator_service = ActuatorService()
        actuators = actuator_service.get_all_actuators()
        actuator = [
            actuator for actuator in actuators if actuator.actuator_id == actuator_id
        ][0]
        actuator_service.change_value(actuator, value)
