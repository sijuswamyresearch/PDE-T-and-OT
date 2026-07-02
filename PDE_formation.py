import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ==========================================
# 1. SETUP THE 3D FIGURE & GRID
# ==========================================
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.25) # Make room for UI sliders

# Create the spatial coordinates (x, y)
x = np.linspace(-10, 10, 20)
y = np.linspace(-10, 10, 20)
X, Y = np.meshgrid(x, y)

# Initial arbitrary constants
a_init = 1.0
b_init = 1.0
k_const = 5.0

def calculate_surface(a, b, k):
    # Rearranging ax + by + z = k to solve for z
    return k - a * X - b * Y

# ==========================================
# 2. INITIAL PLOT & TEXT ANNOTATION
# ==========================================
Z = calculate_surface(a_init, b_init, k_const)
surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8)

# Fixed axis limits to prevent the plot from jumping around
def format_axes():
    ax.set_xlabel('Spatial X')
    ax.set_ylabel('Spatial Y')
    ax.set_zlabel('Voltage (Z)')
    ax.set_title('Family of Planes: ax + by + z = k')
    ax.set_zlim(-30, 30)

format_axes()

# Text box to show the real-time math
props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
text_box = fig.text(0.05, 0.90, '', transform=fig.transFigure, fontsize=11, 
                    verticalalignment='top', family='monospace', bbox=props)

def update_text(a, b):
    # p = dz/dx = -a
    # q = dz/dy = -b
    p = -a
    q = -b
    # The PDE: px + qy - z + k = 0
    # We show it always equals zero regardless of a and b
    text_str = (f"Current Constants:\n"
                f"a = {a:5.2f}  |  b = {b:5.2f}\n\n"
                f"Partial Derivatives:\n"
                f"p (dz/dx) = {-a:5.2f}\n"
                f"q (dz/dy) = {-b:5.2f}\n\n"
                f"Checking the formulated PDE:\n"
                f"px + qy - z + k = 0.00")
    text_box.set_text(text_str)

update_text(a_init, b_init)

# ==========================================
# 3. INTERACTIVE SLIDERS
# ==========================================
axcolor = 'lightgray'
ax_a = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_b = plt.axes([0.2, 0.10, 0.65, 0.03], facecolor=axcolor)

slider_a = Slider(ax_a, 'Constant a', -3.0, 3.0, valinit=a_init)
slider_b = Slider(ax_b, 'Constant b', -3.0, 3.0, valinit=b_init)

def update(val):
    a = slider_a.val
    b = slider_b.val
    
    # 3D plots in matplotlib need to be cleared and redrawn to update smoothly
    ax.clear()
    Z_new = calculate_surface(a, b, k_const)
    ax.plot_surface(X, Y, Z_new, cmap='plasma', alpha=0.8)
    
    format_axes()
    update_text(a, b)
    fig.canvas.draw_idle()

# Link the sliders to the update function
slider_a.on_changed(update)
slider_b.on_changed(update)

plt.show()