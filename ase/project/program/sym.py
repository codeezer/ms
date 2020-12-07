import pySym
proj = pySym.Project("./test.py")
pg = proj.factory.path_group()
pg.explore()
pg.completed[0].state.any_int('z')
