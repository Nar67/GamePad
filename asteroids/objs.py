

def resta_tots(listt, desplx, desply, resx, resy):
	suplist = []
	for x in listt:
		suplist.append([x[0] + desplx - resx, x[1] + desply - resy])
	return suplist

def get_obj_1(desplx, desply, resx, resy):
	listt = [[-1, 0], [0, -1], [0, 0], [0, 1], [1, 0]]
	return resta_tots(listt, desplx, desply, resx, resy)

def get_obj_2(desplx, desply, resx, resy):
	listt = [[0,-1] , [0, 0], [0, 1], [0, 2]]
	return resta_tots(listt, desplx, desply, resx, resy)

def get_obj_3(desplx, desply, resx, resy):
	listt = [[-1, -1], [0, 0], [1, 1]]
	return resta_tots(listt, desplx, desply, resx, resy)