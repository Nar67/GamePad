

def get_obj_1(desplx, desply):
	listt = [[-1, 0], [0, -1], [0, 0], [0, 1], [1, 0]]
	suplist = []
	for x in listt:
		suplist.append([x[0] + desplx, x[1] + desply])
	return suplist

def get_obj_2(desplx, desply):
	listt = [[0,-1] , [0, 0], [0, 1], [0, 2]]
	suplist = []
	for x in listt:
		suplist.append([x[0] + desplx, x[1] + desply])
	return suplist

def get_obj_3(desplx, desply):
	listt = [[-1, -1], [0, 0], [1, 1]]
	suplist = []
	for x in listt:
		suplist.append([x[0] + desplx, x[1] + desply])
	return suplist