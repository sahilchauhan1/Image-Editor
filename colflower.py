# name: File path of the pgm image file
# Output is a 2D list of integers
def readpgm(name):
	image = []
	with open(name) as f:
		lines = list(f.readlines())
		if len(lines) < 3:
			print("Wrong Image Format\n")
			exit(0)

		count = 0
		width = 0
		height = 0
		for line in lines:
			if line[0] == '#':
				continue

			if count == 0:
				if line.strip() != 'P2':
					print("Wrong Image Type\n")
					exit(0)
				count += 1
				continue

			if count == 1:
				dimensions = line.strip().split(' ')
				print(dimensions)
				width = dimensions[0]
				height = dimensions[1]
				count += 1
				continue

			if count == 2:	
				allowable_max = int(line.strip())
				if allowable_max != 255:
					print("Wrong max allowable value in the image\n")
					exit(0)
				count += 1
				continue

			data = line.strip().split()
			data = [int(d) for d in data]
			image.append(data)
	return image	

# img is the 2D list of integers
# file is the output file path
def writepgm(img, file):
	with open(file, 'w') as fout:
		if len(img) == 0:
			pgmHeader = 'p2\n0 0\n255\n'
		else:
			pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
			fout.write(pgmHeader)
			line = ''
			for i in img:
				for j in i:
					line += str(j) + ' '
				line += '\n'
			fout.write(line)
def avg_fltr(image):
	H=len(image)
	W=len(image[0])
	pixel=[[0 for j in range(W)]for i in range(H)]
	for i in range(1,H-1):
		for j in range(1,W-1):
			pixel[i][j]=int((image[i-1][j-1]+image[i-1][j]+image[i-1][j+1]+image[i][j-1]+image[i][j]+image[i][j+1]+image[i+1][j-1]+ image[i+1][j]+image[i+1][j+1])/9)
	for i in range(0,H):
		pixel[i][0]=image[i][0]
		pixel[i][W-1]=image[i][W-1]
	for j in range(0,W):
		pixel[0][j]=image[0][j]
		pixel[H-1][j]=image[H-1][j]
	return pixel

def edge_detection(image):
	H=len(image)
	W=len(image[0])
	grad=[[0 for j in range(W)]for i in range(H)]
	im=[[0 for j in range(W+2)]for i in range(H+2)]

	for i in range(1,H+1):
		for j in range(1,W+1):
			im[i][j]=image[i-1][j-1]
	
	m=0

	for i in range(1,H+1):
		for j in range(1,W+1):
			hdif = (im[i-1][j-1]-im[i-1][j+1]) + 2*(im[i][j-1]-im[i][j+1]) + (im[i+1][j-1]-im[i+1][j+1])
			vdif = (im[i-1][j-1]-im[i+1][j-1]) + 2*(im[i-1][j]-im[i+1][j]) + (im[i-1][j+1]-im[i+1][j+1])
			grad[i-1][j-1] = (hdif**2+vdif**2)**.5
			if(grad[i-1][j-1]>m):
				m=grad[i-1][j-1]

	for i in range (H):
		for j in range (W):
			grad[i][j]=int((grad[i][j])*255/m)


	return grad

def least_energy(image):
	H=len(image)
	W=len(image[0])
	grad=[[0 for j in range(W)]for i in range(H)]
	im=[[0 for j in range(W+2)]for i in range(H+2)]

	for i in range(1,H+1):
		for j in range(1,W+1):
			im[i][j]=image[i-1][j-1]
	
	

	m=0
	for i in range(1,H+1):
		for j in range(1,W+1):
			hdif = (im[i-1][j-1]-im[i-1][j+1]) + 2*(im[i][j-1]-im[i][j+1]) + (im[i+1][j-1]-im[i+1][j+1])
			vdif = (im[i-1][j-1]-im[i+1][j-1]) + 2*(im[i-1][j]-im[i+1][j]) + (im[i-1][j+1]-im[i+1][j+1])
			grad[i-1][j-1] = (hdif**2+vdif**2)**.5
			if(grad[i-1][j-1]>m):
				m=grad[i-1][j-1]

	
			
	
	

	ext=[[0 for j in range(W)]for i in range(H)]
	for j in range(0,W):
		ext[0][j]=int(grad[0][j])


	for i in range(1,H):
		for j in range(0,W):
			if (j==0):
				ext[i][j]= int(grad[i][j] + min(ext[i-1][j], ext[i-1][j+1]))
			elif (j==W-1):
				ext[i][j]= int(grad[i][j] + min(ext[i-1][j-1], ext[i-1][j]))
			else:
				ext[i][j]= int(grad[i][j] + min(ext[i-1][j-1], ext[i-1][j], ext[i-1][j+1]))
	


	
	m=0
	for j in range(W):
		if (ext[H-1][j]>m):
			m=ext[H-1][j]
	print(m)


	n=m
	for j in range(W):
		if (ext[H-1][j]<n):
			n=ext[H-1][j]
	print(n)
	for j in range(W):
		if ext[H-1][j]==n:
			image[H-1][j]=255
			i=H-1
			while i>=0:
				if j==W-1:
					if min(ext[i-1][j-1], ext[i-1][j])==ext[i-1][j-1]:
						image[i-1][j-1]=255
					if min(ext[i-1][j-1], ext[i-1][j])==ext[i-1][j]:
						image[i-1][j]=255
					
					
				elif j==0:
					if min(ext[i-1][j], ext[i-1][j+1])==ext[i-1][j]:
						image[i-1][j]=255
					if min(ext[i-1][j], ext[i-1][j+1])==ext[i-1][j+1]:
						image[i-1][j+1]=255
				else:
					if min(ext[i-1][j-1], ext[i-1][j], ext[i-1][j+1])==ext[i-1][j-1]:
						image[i-1][j-1]=255
					if min(ext[i-1][j-1], ext[i-1][j], ext[i-1][j+1])==ext[i-1][j]:
						image[i-1][j]=255
					if min(ext[i-1][j], ext[i-1][j+1])==ext[i-1][j+1]:
						image[i-1][j+1]=255
				i=i-1
					
			






	
	
	return image










			






	
	
			
	

	


		
		

########## Function Calls ##########
x = readpgm('test.pgm')			# test.pgm is the image present in the same working directory
y=avg_fltr(x)
writepgm(y, 'test_average.pgm')		# x is the image to output and test_o.pgm is the image output in the same working directory
###################################def edge_detection(H,W,hdif,vdif):

