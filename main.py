from contourLoader import ContourLoader as cl
import matplotlib.pyplot as plt
import numpy as np
import ezdxf

path = ".\ht_Contour\ceramics.dxf"
contour = cl(path)
contour.load_contour_data()
print(contour.contour_data.shape)

contour.plot_contour_data()