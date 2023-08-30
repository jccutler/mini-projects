import numpy as np
import sys
from numba import jit
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from screeninfo import get_monitors

class MandelVis:
    def __init__(self, x_init, y_init, depth, res):
        self.x_range = x_init
        self.y_range = y_init
        self.width = self.x_range[1] - self.x_range[0]
        self.height = self.y_range[1] - self.y_range[0]
        self.depth = depth
        self.res = res

        pixels = self.render_mandelbrot() 
        fig, ax = plt.subplots(figsize=self.initial_size(), dpi=100)
        ax.imshow(pixels, cmap='inferno', interpolation='bilinear')
        ax.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        plt.margins(0,0)
        plt.show()
                
    def initial_size(self):
        # Get largest possible size for figure while preserving aspect ratio 

        monitor = get_monitors()[0]
        dpi = 100 
        width_in = monitor.width / dpi
        height_in = monitor.height / dpi
        
        aspect_ratio = self.width / self.height

        fig_height = height_in
        fig_width = fig_height * aspect_ratio
        if fig_width > width_in:
            fig_height = fig_height * (width_in / fig_width)
            fig_width = width_in

        return (fig_width, fig_height)

    def render_mandelbrot(self):
        # Generate pixel array and get normalized index value for each pixel 

        re_slices = int(self.width * self.res)
        im_slices = int(self.height * self.res)

        pixel_levels = np.empty((im_slices, re_slices))

        for i in range(re_slices):
            for j in range(im_slices):
                x = self.x_range[0] + i/self.res
                y = self.y_range[0] + j/self.res
                index = mandelbrot_index(x, y, self.depth)
                pixel_levels[j,i] = index / self.depth

        return pixel_levels


@jit(nopython=True)
def mandelbrot_index(x_0, y_0, depth):
    # Generates sequence with initial values x_0 y_0 until divergence OR depth is reached

    x = 0
    y = 0
    i = 0
    while x*x + y*y <= 2*2 and i < depth:
        temp = x*x - y*y + x_0
        y = 2*x*y + y_0
        x = temp
        i += 1
    return i

def main():
    if len(sys.argv) < 5:
        print("Usage: x_0,x_1 y_0,y_1 depth resolution")
        sys.exit(1)
        
    x_range_init = tuple(map(float, sys.argv[1].split(','))) 
    y_range_init = tuple(map(float, sys.argv[2].split(',')))
    depth = int(sys.argv[3])
    res_init = int(sys.argv[4])

    mandelbrot = MandelVis(x_range_init, y_range_init, depth, res_init)

if __name__ == "__main__":
    main()
