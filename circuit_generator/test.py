from LTSpice_generator import schematicAscGenerator 

G = schematicAscGenerator()

G.ground(0, -80)
G.voltage(0, 0, 0, 5)
G.wire(0, 0, 50, 0)
G.res(50, 0, 270, 12)
G.wire(130, 0, 180, -50)
G.ground(180, -50)

G.compile()


#G.wire(0, 0, 100, 100)
# G.res(0, 0, 0, 10)
# G.res(0, 0, 90, 20)
# G.res(0, 0, 180, 30)
# G.res(0, 0, 270, 40)


# for coords in G.getCoords():
#     print(coords["start_x"], coords["start_y"] ,coords["end_x"], coords["end_y"])
#     G.wire(coords["start_x"], coords["start_y"] ,coords["end_x"], coords["end_y"])

# print(G.getCoords())

# Resistencia e ind
# 0 - +
# 90 + +
# 180 + -
# 270 - -

# Diodo y cap
# 0 - 0
# 90 0 +
# 180 + 0
# 270 0 -

# voltage
# 0 0 +
# 90 + 0
# 180 0 -
# 270 - 0

# Current
# ----


# G.wire(16, 16, -16, 180)
#G.ind(0, 0, 0, 10)
# G.cap(0, 0, 0, 1)
# G.cap(0, 0, 90, 1)
# G.cap(0, 0, 180, 1)
# G.cap(0, 0, 270, 1)
#G.diode(0, 0, 0)



# G.current(0, 0, 0, 5)
# G.current(0, 0, 90, 5)
# G.current(0, 0, 180, 5)
# G.current(0, 0, 270, 5)
# G.voltage(0, 0, 0, 5)
# G.voltage(0, 0, 90, 5)
# G.voltage(0, 0, 180, 5)
# G.voltage(0, 0, 270, 5)

#G.ground(0, 0)
#G.ground(0, 0)
# print(G.getWires())

# G.res(0, 0, 270, 10)
# G.res(16*5, 0, 270, 10)

# G.cap(0, 0, 270, 10)
# G.cap(16*4, 0, 270, 10)

# G.ind(0, 0, 270, 10)
# G.ind(16*5, 0, 270, 10)

# G.diode(0, 0, 0)
# G.diode(0, 16*4, 0)

