# Erosion in Hall thrusters
## Introduction
This repository contains the code used to simulate the erosion of the channel walls of a Hall thruster. The code is written in Python 3.10.5 and uses the following libraries:
- numpy
- matplotlib
- pandas
- scipy

## Usage
The code is divided into two parts:
1) The first part is reading and iterpolating experimental data. The data is read from the file `.cvs` files.
<p align="center">
  <img src="./illustrations/exp_data.png" alt="drawing" style="width:900px;"/>
</p>

2) The second part is the simulation of the erosion. The simulation is done by iterating over the ideal (un-eroded) profile and calculating the erosion at each point. The erosion is calculated using the following equation:

$$
\Delta y = S_1(\alpha)\cdot S_2(\varepsilon_i)\cdot j_{\perp i} \cdot \Delta t \cdot \cos(\gamma_i),
$$

where $S_1(\alpha)$, $S_2(\varepsilon_i)$ - take into account the dependence of the sputtering coefficient of the wall material in at a given point on the angle of incidence of ions $\alpha$ and ion energy $\varepsilon$, $j_{\perp i}$ - is the ion flux density directed perpendicular to the surface at a given point, $\Delta t$ - is the time step, $\gamma_i$ - is the angle between the ion flux vector and the surface normal.
For purpose of computing $\Delta y$ we need to calculate $\alpha_i$ and $\gamma_i$, since other parameters are known, or could be taken from the experimental data (that is already interpolated in the step 1). The angle $\alpha_i$ is calculated using the following Python code and as a block-scheme:

### Block-scheme
<p align="center">
    <img src="./illustrations/block-scheme_frame.png" alt="drawing" style="width:600px;"/>
</p>

### Python code

```python
def alpha_f(x0, y0, x1, y1):
    """
    Function calculates the angle between vector and x axis.
    First vector is defined by x0, y0 and x1, y1.
    Second "vector" is always x axis.
    """
    dx = np.abs(x1 - x0)
    dy = np.abs(y1 - y0)
    dx_is_zero = dx == 0
    alpha = np.where(dx_is_zero, np.pi/2, np.arctan(dy / dx))
    return alpha
```
```python np.where``` is used to avoid division by zero. The angle $\gamma_i$ is calculated using the following Python code:
```python
def gamma_f(x1, y1, x2, y2):
    """
    Function calculates the angle between current two vectors.
    First vector is defined by x1, y1 and x-axis.
    Second vector is defined by x2, y2 and x1, y1.
    """
    dx = np.abs(x1 - x2)
    dy = np.abs(y1 - y2)
    dx_is_zero = dx == 0
    gamma = np.where(dx_is_zero, np.pi/2, np.arctan(dy / dx))
    return gamma
```
Before the erosion is calculated, additional parameters are calculated or been set:
1) Is $\tau$ - total erosion time. It is set to $10^3\;s$.
2) $dt$ - time step. It is set to $1\;s$.
3) Ion source which is randomly positioned in the ellipse with the following parameters:
    - $x, y$ center coordinates of the ellipse. They are set to $0.25$ and $1$ units respectively.
    - $a, b$ - ellipse parameters. They are set to $0.05$ and $0.3$ units respectively.
4) Number of sampled point along the un-eroded profile. It is set to $10^2$ points.
5) Number of ion sources in the simulation. It is set to $1$ sources.
6) Ion energy $\varepsilon_i$. It is set to $200\;eV$ and $S_2(\varepsilon_i)$ is calculated using the following Python code:
```python s_energy = s_energy_f(ion_energy)```
After all parameters are set, the erosion is calculated using the following Python code:
```python
min_profile_y = np.inf  # Initialize a variable to keep track of the minimum profile_y

for step in range(num_steps):
    for i, x in enumerate(profile_x):
        # Calculate the angle between the current point and all ion sources
        alpha = alpha_f(ion_src_x, ion_src_y, x, profile_y[i])
        alpha_array[i] = np.degrees(alpha)

        # Calculate the angle between the current point and the previous point
        gamma = gamma_f(ion_src_x, ion_src_y, x, profile_y[i])
        gamma_array[i] = gamma

        # Calculate the erosion rate at the current point
        erosion = np.abs(s_alpha_f(alpha) * s_energy * j_y_f(x) * np.cos(gamma) * dt)

        # Check for shadowing
        if profile_y[i] > min_profile_y:
            min_profile_y = profile_y[i]
            # Calculate the angle between the current point and all ion sources
            alpha = alpha_f(ion_src_x, ion_src_y, x, profile_y[i])
            alpha_array[i] = alpha

            # Calculate the angle between the current point and the previous point
            gamma = gamma_f(ion_src_x, ion_src_y, x, profile_y[i])
            gamma_array[i] = gamma

            # Calculate the erosion rate at the current point
            erosion = np.abs(s_alpha_f(alpha) * s_energy * j_y_f(x) * np.cos(gamma) * dt)
        else:
            # Calculate the erosion rate at the minimum point if shadowed
            i_min = np.argmin(min_profile_y)
            # Calculate the angle between the current point and all ion sources
            alpha = alpha_f(ion_src_x, ion_src_y, x, profile_y[i_min])
            alpha_array[i_min] = alpha

            # Calculate the angle between the current point and the previous point
            gamma = gamma_f(ion_src_x, ion_src_y, x, profile_y[i_min])
            gamma_array[i_min] = gamma

            # Calculate the erosion rate at the current point
            erosion = np.abs(s_alpha_f(alpha) * s_energy * j_y_f(x) * np.cos(gamma) * dt)
            erosion = np.abs(s_alpha_f(alpha) * s_energy * j_y_f(x) * np.cos(gamma) * dt)

        if x < ion_src_x:
            erosion = 0
        profile_y[i] -= erosion
        profile_time[step, i] = profile_y[i]
```
