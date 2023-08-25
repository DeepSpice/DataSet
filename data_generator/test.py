from LTSpice_generator import schematicAscGenerator 

G = schematicAscGenerator()

G.wire(0, 0, 0, 96)
G.res(-16, 80, 0, 270)
G.wire(0, 180, 100, 180)
G.voltage(80, 180, 270, 5)
G.ground(176, 180)
G.ground(0, 0)
print(G.getWires())
G.compile()