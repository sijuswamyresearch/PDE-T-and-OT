import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ==========================================
# 1. THE GRID (Space & Time Parameters)
# ==========================================
# Simulating a physical wire of length L
nx = 200                  # Number of spatial nodes along the wire
dx = 0.1                  # Distance between each node (m)
L = nx * dx               # Total length of the wire

c = 1.0                   # Propagation velocity of the signal
dt = 0.05                 # Time step size (must be <= dx/c for Courant stability)
C_courant = (c * dt) / dx # Courant number (governs numerical stability)

x_axis = np.linspace(0, L, nx)

# We need three arrays to track the dynamic system across time (t-1, t, t+1)
# This breaks the "instantaneous" lumped circuit assumption.
V_prev = np.zeros(nx)     # Voltage at time t - dt
V_curr = np.zeros(nx)     # Voltage at time t
V_next = np.zeros(nx)     # Voltage at time t + dt

# ==========================================
# VISUALIZATION SETUP
# ==========================================
fig, ax = plt.subplots(figsize=(10, 5))
line, = ax.plot(x_axis, V_curr, color='b', lw=2, label="Voltage V(x,t)")

# Formatting the plot for electronics students
ax.set_ylim(-1.5, 1.5)
ax.set_xlim(0, L)
ax.set_title("Dynamic System: Voltage Pulse on a Distributed Transmission Line")
ax.set_xlabel("Distance along the wire (x)")
ax.set_ylabel("Voltage Amplitude (V)")
ax.axhline(0, color='black', lw=0.5)
ax.legend(loc="upper right")
ax.grid(True, linestyle='--', alpha=0.7)

# ==========================================
# 2 & 3. THE UPDATE RULE & BOUNDARY CONDITIONS
# ==========================================
def update(frame):
    """
    This function calculates the next time step of the PDE and updates the plot.
    It executes once per animation frame.
    """
    global V_prev, V_curr, V_next

    # --- SOURCE CONDITION (x = 0) ---
    # Injecting a Gaussian voltage pulse at the start of the wire for the first few frames
    if frame < 60:
        # Simulating a switch turning on and off quickly
        V_curr[0] = np.exp(-0.5 * ((frame - 30) / 8.0)**2) 
    else:
        V_curr[0] = 0.0 # Return the source to 0V (grounded)

    # --- THE PDE DISCRETIZATION (The Core Math) ---
    # We solve the 2nd-order wave equation by isolating V(x, t+dt)
    # Using vectorized NumPy operations for high computational efficiency
    V_next[1:-1] = (2 * V_curr[1:-1] - V_prev[1:-1] + 
                   (C_courant**2) * (V_curr[2:] - 2 * V_curr[1:-1] + V_curr[:-2]))

    # --- TERMINAL BOUNDARY CONDITION (x = L) ---
    # This is where the physical engineering meets the math.
    
    # Option A: Short Circuit (V = 0). The wave reflects inverted.
    V_next[-1] = 0.0 
    
    # Option B: Open Circuit (Current = 0, dV/dx = 0). The wave reflects positively.
    # To demonstrate an open circuit to students, comment out Option A and uncomment below:
    #V_next[-1] = V_next[-2] 

    # --- ADVANCE TIME ---
    # Shift our memory arrays forward by one time step
    V_prev[:] = V_curr[:]
    V_curr[:] = V_next[:]

    # Update the visual plot
    line.set_ydata(V_curr)
    return line,

# ==========================================
# 4. THE ANIMATION
# ==========================================
# Run the simulation for 400 frames, updating every 20 milliseconds
ani = animation.FuncAnimation(fig, update, frames=400, interval=20, blit=True)

plt.tight_layout()
plt.show()