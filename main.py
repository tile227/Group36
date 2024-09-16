import ifcopenshell

from .rules import beamRule


model = ifcopenshell.open("path/to/ifcfile.ifc")

beamResult = beamRule.checkRule(model)


print("Beam result:", beamResult)

