

def get_obj_1(desplx, desply):
	listt = [[-1, 0], [0, -1], [0, 0], [0, 1], [1, 0]]
	suplist = []
	for x in listt:
		suplist.append([x[0] + desplx, x[1] + desply])
	return suplist