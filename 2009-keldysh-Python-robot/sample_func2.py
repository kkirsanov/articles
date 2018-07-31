def GetPixcelColor(x, y):
    return (1, 2, 3)
pos = (1, 2)

color = GetPixcelColor(pos[0], pos[1])
color = GetPixcelColor(*pos)
r, g, b = GetPixcelColor(*pos)

pos = {'x':1, 'y':2}
r, g, b = GetPixcelColor(**pos)

def F(*args, **kwargs):
    print args #(1, 2, 3)
    print kwargs #{'z': 4}
    
F(1,2,3,z=4)