from .models import UbiantClient

ub = UbiantClient()
print(ub.get_my_infos())
