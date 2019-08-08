import argparse
import numpy as np
import os

test = False

def mapping(angle):
	return int(angle/45)
def mapping_dis(distance):
	return int(distance/10)
def get_parser():
	parser = argparse.ArgumentParser(description='parameters of datasets')
	parser.add_argument('--file_dir', default='~', help='dir of all fp files')
	parser.add_argument('--points_num', default=4, help='how many points a path contain')
	args = parser.parse_args()
	return args

def distance(tuple1, tuple2):
	return ((tuple1[1] - tuple2[1])**2 + (tuple1[0] - tuple2[0])**2)**0.5
	#0:x 1:y 2:angle

def insight_angle(tuple1, tuple2, tuple3):
	a = np.array([tuple1[0] - tuple2[0], tuple1[1] - tuple2[1]])
	b = np.array([tuple3[0] - tuple2[0], tuple3[1] - tuple2[1]])
	La=np.sqrt(a.dot(a))
	Lb=np.sqrt(b.dot(b))
	if La == 0 or Lb == 0:
		return 90
	cos_angle=a.dot(b)/(La*Lb)
	if cos_angle > 1:
		cos_angle = 1
	if cos_angle < -1:
		cos_angle = -1
	return mapping(np.arccos(cos_angle)*360/2/np.pi)

def cop_sort(tuple,tuple_ele):
	new_list = sorted(tuple,key=lambda x:distance(x,tuple_ele))
	return new_list

def find_all(source, num_points, org_list):
	ans = []
	check = set()
	ans.append(source)
	min_dis = 10000
	target = []
	for i in range(num_points):
		min_dis = 10000
		target = []
		itr = 0
		for ele in org_list:
			if distance(ele, ans[len(ans) - 1]) < min_dis and distance(ele, ans[len(ans) - 1])>0.001:
				target = ele
				min_dis = distance(ele, ans[len(ans)-1])
		ans.append(target)
	return ans


def make_path(minutiaes):
	dis = []
	phi = []
	sigma = []
	for i in range(len(minutiaes) - 2):
		dis.append(int(distance(minutiaes[i],minutiaes[i+1])))
		phi.append(int(insight_angle(minutiaes[i],minutiaes[i+1],minutiaes[i+2])))
		sigma.append(int(minutiaes[i+1][2] - minutiaes[i][2])%360)
	dis.append(int(distance(minutiaes[len(minutiaes) - 2],minutiaes[len(minutiaes) - 1])))
	sigma.append(int(minutiaes[len(minutiaes) - 2][2] - minutiaes[len(minutiaes) - 1][2])%360)
	return dis + phi + sigma

def make_path_str(minutiaes):
	dis = ''
	phi = ''
	sigma = ''
	for i in range(len(minutiaes) - 2):
		dis += str(mapping_dis(int(distance(minutiaes[i],minutiaes[i+1]))))
		if test:
			print('distance is ', distance(minutiaes[i],minutiaes[i+1]))
		phi += str(int(insight_angle(minutiaes[i],minutiaes[i+1],minutiaes[i+2])))
		sigma += str(mapping(int(minutiaes[i+1][2] - minutiaes[i][2])%360))
	dis += str(mapping_dis(int(distance(minutiaes[len(minutiaes) - 2],minutiaes[len(minutiaes) - 1]))))
	sigma += str(mapping(int(minutiaes[len(minutiaes) - 2][2] - minutiaes[len(minutiaes) - 1][2])%360))
	return dis + phi + sigma

def finger2path(file,points_num):
	path = set()
	with open(file,'r') as reader:
		minutiaes = []
		while True:
			line = reader.readline()
			if line.startswith('[minutiae]'):
				break
		num = int(reader.readline())
		for _ in range(num):
			line = reader.readline()
			minutiaes.append([int(x) for x in line.split()[:3]])
	for ele in minutiaes:
		#sort ascend take minutiaes
		minutiaes_copy = cop_sort(minutiaes,ele)

		#iterate ascend

		#minutiaes_copy = find_all(ele, points_num, minutiaes)
		if test:
			print("list of path points is:",minutiaes_copy)
		path.add(make_path_str(minutiaes_copy[:points_num]))
	''' for test break'''
	if test:
		print(path)
	''' test end '''
	return path

def bat_deal_files(filespath, points_num):
	files = os.listdir(filespath)
	for file in files:
		finger2path(filespath + '/' + file, points_num)



def test_this_file(filespath):
	get_list(filespath)
	pass
if __name__ == '__main__':
	args = get_parser()
	finger2path(args.file_dir+'/1_1.fp',args.points_num)
	#print(get_list(args.file_dir))