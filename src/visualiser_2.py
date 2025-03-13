import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

# Generate sample data (replace with your actual sensor data)
num_sensors = 16
time_steps = 100
sensor_data = np.zeros((num_sensors, time_steps))

# Fill with sample data - you'll replace this with your actual data
# Creating some sample patterns with values between 0 and 10 (newtons)
for i in range(num_sensors):
    # Base signal with random noise between 0 and 3
    sensor_data[i] = np.random.rand(time_steps) * 3

    # Add some peaks to simulate different sensor responses (keeping max at 10)
    if i % 4 == 0:
        peak = 6 * np.sin(np.linspace(0, np.pi, 20))
        sensor_data[i, 30:50] += peak
    if i % 3 == 0:
        peak = 4 * np.sin(np.linspace(0, np.pi, 20))
        sensor_data[i, 60:80] += peak

    # Ensure all values are between 0 and 10
    sensor_data[i] = np.clip(sensor_data[i], 0, 10)

# Create figure with specified size
plt.figure(figsize=(12, 8))

# Adjust layout
plt.subplots_adjust(hspace=0)

# Custom colormap for sensors
colors = [(0.9, 0.9, 0.9), (0.7, 0.7, 0.9), (0.5, 0.5, 0.9)]
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=100)

# Plot each sensor's data
for i in range(num_sensors):
    # Create subplot
    ax = plt.subplot(num_sensors, 1, i+1)

    # Calculate fixed y-position for each sensor's line
    fixed_y_position = 5  # Middle of the 0-10 range

    # Draw a horizontal reference line
    plt.axhline(y=fixed_y_position, color='lightgray', linestyle='-', linewidth=0.8, alpha=0.5)

    # Plot points with size based on force reading at the fixed y-position
    # Min size 5, max size 200 (for 0-10 newton range)
    sizes = sensor_data[i] * 20  # Scale from 0-10 to 0-200

    # Colors can vary slightly to help distinguish points if needed
    point_colors = plt.cm.Blues(0.5 + sensor_data[i]/20)

    plt.scatter(range(time_steps), [fixed_y_position] * time_steps,
                s=sizes, color='darkblue', alpha=0.7, zorder=3)

    # Remove most of the axes elements
    plt.yticks([])
    if i < num_sensors - 1:
        plt.xticks([])

    # Add sensor number on the left side
    plt.ylabel(f"{i+1}", rotation=0, labelpad=15, va='center', fontsize=10)

    # Remove the frame except for the left side
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if i < num_sensors - 1:
        ax.spines['bottom'].set_visible(False)

    # Set the same y-limit for all subplots
    plt.ylim(0, 10)

# Add title and labels
plt.xlabel("Time", fontsize=12)
plt.text(-5, num_sensors * 1.05, "Sensor #", rotation=90, fontsize=12,
         transform=plt.gca().transAxes)

# Add a legend for the point sizes
ax_main = plt.gcf().add_axes([0.92, 0.5, 0.03, 0.3])
ax_main.set_axis_off()

# Create example points for legend
forces = [2, 5, 8]
for j, force in enumerate(forces):
    y_pos = 0.8 - (j * 0.3)
    size = force * 20
    ax_main.scatter([0.5], [y_pos], s=size, color='darkblue', alpha=0.7)
    ax_main.text(0.6, y_pos, f"{force} N", va='center', fontsize=9)

ax_main.text(0.5, 1.0, "Force", ha='center', fontsize=10)

# Set the overall title
plt.suptitle("Tactile Sensor Readings (0-10 Newtons)", fontsize=14, y=0.95)

# Adjust the layout
plt.tight_layout(rect=[0, 0, 0.9, 0.95])

plt.savefig('tactile_sensor_plot.png', dpi=300, bbox_inches='tight')
plt.show()
