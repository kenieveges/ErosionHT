import numpy as np
import matplotlib.pyplot as plt
import ezdxf

class ContourLoader:
    def __init__(self, path):
        self.path = path
        self.contour_data = self.load_contour_data()

    def load_contour_data(self):
        doc = ezdxf.readfile(self.path)
        msp = doc.modelspace()
        contour_data = []

        # Iterate through entities and extract LINES as contour data
        for entity in msp:
            if entity.dxftype() == 'LINE':
                start_point = (entity.dxf.start.x, entity.dxf.start.y)
                end_point = (entity.dxf.end.x, entity.dxf.end.y)
                contour_data.extend([start_point, end_point])

        return np.array(contour_data)

    def plot_contour_data(self):
        plt.plot(self.contour_data[:,0], self.contour_data[:,1],\
                 color='black', linewidth=1, linestyle='-')
        plt.grid()
        plt.axis('equal')
        plt.show()