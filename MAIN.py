from finger2path import finger2path
import argparse
threshold = 2
test = True
def get_parser():
	parser = argparse.ArgumentParser(description='parameters of datasets')
	parser.add_argument('--file_dir', default='~', help='dir of all fp files')
	parser.add_argument('--points_num', default=5, help='how many points a path contain')
	args = parser.parse_args()
	return args

def compare_hash(paths1,paths2):
	sum = 0
	for ele in paths2:
		if ele in paths1:
			sum += 1
	return sum#*2.0/(len(paths1)+len(paths2))

def inside_class(num_i, thr = threshold):
	ans = set()
	summ = 0
	for i in range(1,7):
		ans = ans | finger2path(args.file_dir+'/%d_%d.fp'%(num_i,i),args.points_num)
	for i in range(7,9):
		num = compare_hash(ans,finger2path(args.file_dir+'/%d_%d.fp'%(num_i,i),args.points_num))
		if test:
			print("%d_%d sum is:" %(num_i,i),num)
		if num >= thr:
			summ += 1
	return summ

def outside_class(num_i, thr = threshold, range_of_id = range(1,101)):
	ans = set()
	summ = 0
	for i in range(1,7):
		ans = ans | finger2path(args.file_dir+'/%d_%d.fp'%(num_i,i),args.points_num)
	for i in range(1,9):
		for j in range_of_id:
			if num_i == j:
				continue
			else:
				num = compare_hash(ans,finger2path(args.file_dir+'/%d_%d.fp'%(j,i),args.points_num))
				if test:
					print("%d_%d num is:" %(j,i),num)
				if num < thr:
					summ += 1
	return summ

if __name__ == '__main__':
	args = get_parser()
	
	sum1 = 0
	sum2 = 0
	
	# test inside class
	for i in range(1,101):
		sum1 += inside_class(i)
	print("TA: ", sum1*1.0/100/2)
	'''
	# test outside class
	
	for i in range(1,101):
		print("sum is ",outside_class(i))
	#print(get_list(args.file_dir))
'''
	