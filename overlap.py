
import numpy as np 
from matplotlib import pyplot as plt
from celluloid import Camera # for animation 

def rotation_mat( theta ):
	# rotation matrix, assumes positive theta values, hence counterclockwise rotation
	return( np.array( [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]] ) )

if __name__ == "__main__":

	discretization = 100

	# pore is static 
	# pore extents on the x axis
	pxi = 5.
	pxf = 6.
	pyi = 5.
	pyf = 6.
	x = np.linspace(pxi, pxf, discretization) 
	# pore extents on the y axis
	y = np.linspace(pyi, pyf, discretization) 
	# pore "lines" in the x y plane (for plotting and overlap calculatin)
	pore_xv, pore_yv = np.meshgrid(x, y)

	# a bunch of values for rotation angle (positive values mean counterclockwise rotation from horizontal)
	angle_vals = np.linspace(0.,0.5*np.pi,51)

	# initial slit coordinates (slit is revolving)
	x = np.linspace(1., 10., discretization) # x domain 
	y = np.linspace(-.5, .5, discretization) # y domain
	# slit "lines"
	slit_xv, slit_yv = np.meshgrid(x, y)
	# elements will be the denominator in the overlap calculation (number of coordinates in the entire slit)
	elements = np.float(slit_xv.shape[0]*slit_xv.shape[1]) 

	# animation
	fig, axs = plt.subplots(1,1)
	camera = Camera(fig)

	for counter, angle in enumerate(angle_vals):
	#for counter in range(18,19):
		angle = angle_vals[counter] 
		# have to replot the pore for every animation snapshot
		axs.plot( pore_xv, pore_yv, 'r-' )

		# overlap is the percentage of slit coordinates that falls within the pore extents
		overlap = 0.

		# the i loop below rotates each "line" that the slit consists of
		# would be great to vectorize this code
		for i in range(slit_xv.shape[0]):

			# apply the rotation matrix to a "line" in the "slit"
			slit_line_coords = np.dot(rotation_mat( angle ), np.array([slit_xv[i,:],slit_yv[i,:]]))
			# plot the rotated "line"
			axs.plot( slit_line_coords[0,:], slit_line_coords[1,:], 'b' )

			# calculate the overlap of the slit "line" with the pore
			for j in range(slit_line_coords.shape[1]):
				if slit_line_coords[0,j] >= pxi and slit_line_coords[0,j] <= pxf and slit_line_coords[1,j] >= pyi and slit_line_coords[1,j] <= pyf:
					# add the number of (x,y) coordinates in the slit "line" that are within the confines of the pore
					overlap += 1

		overlap /= elements 
		overlap *= 100.0 # convert to percentage

		# add textbox in the plot
		axs.text( -2, 9, str(np.round(angle/2/np.pi*360,2))+' degrees'+'\n'+str(np.round(overlap,2))+' % of slit area overlaps with pore')

		axs.axis('equal')
		
		# monitor the rotation angle and the overlap
		print(counter, np.round(angle/2/np.pi*360,2), np.round(overlap,2))
		camera.snap()

	animation = camera.animate()
	animation.save('overlap.gif')
