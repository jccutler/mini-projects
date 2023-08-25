import numpy as np
import sys
from numba import jit
import matplotlib.pyplot as plt

@jit(nopython=True)
def mandelbrot_index(x_0, y_0, depth):
    x = 0
    y = 0
    i = 0
    while x*x + y*y <= 2*2 and i < depth:
        temp = x*x - y*y + x_0
        y = 2*x*y + y_0
        x = temp
        i += 1
    return i
        
def render_mandelbrot(x_range, y_range, depth, res):
    width = x_range[1] - x_range[0]
    height = y_range[1] - y_range[0]

    re_slices = int(width * res)
    im_slices = int(height * res)

    pixel_levels = np.empty((im_slices, re_slices))

    for i in range(re_slices):
        for j in range(im_slices):
            x = x_range[0] + i/res
            y = y_range[0] + j/res
            index = mandelbrot_index(x, y, depth)
            pixel_levels[j,i] = index / depth

    return pixel_levels

def main():
    if len(sys.argv) < 5:
        print("Usage: x_0,x_1 y_0,y_1 depth resolution")
        sys.exit(1)
        
    x_range_init = tuple(map(float, sys.argv[1].split(','))) 
    y_range_init = tuple(map(float, sys.argv[2].split(',')))
    depth = int(sys.argv[3])
    res_init = int(sys.argv[4])

    pixels = render_mandelbrot(x_range_init, y_range_init, depth, res_init) 
    plt.imshow(pixels, cmap='inferno', interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
