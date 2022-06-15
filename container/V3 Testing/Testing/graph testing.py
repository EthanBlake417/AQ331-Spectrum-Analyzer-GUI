import matplotlib.pyplot as plt
import numpy as np

x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 0, 1, 0])

fig, ax, = plt.subplots(1, 1)

h, = ax.plot(x, y)
print(type(h))
x_new = np.array([0, 2, 4, 6, 8])
h.set_xdata(x_new)
ax.relim()
plt.show()
