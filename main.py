import ifcopenshell

from .rules import WallRule


model = ifcopenshell.open("path/to/ifcfile.ifc")

wallResult = wallRule.checkRule(model)


print("Wall result:", wallResult)

