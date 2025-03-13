import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

# Generate sample data (replace with your actual sensor data)
num_sensors = 16
time_steps = 100
sensor_data = np.zeros((num_sensors, time_steps))

# Fill with sample data - you'll replace this with your actual data
# Creating some sample patterns
for i in range(num_sensors):
    # Base signal
    sensor_data[i] = np.random.rand(time_steps) * 10

    # Add some peaks and variations to simulate different sensor responses
    if i % 4 == 0:
        sensor_data[i, 30:50] += 50 * np.sin(np.linspace(0, np.pi, 20))
    if i % 3 == 0:
        sensor_data[i, 60:80] += 30 * np.sin(np.linspace(0, np.pi, 20))

# Create figure with specified size
plt.figure(figsize=(12, 8))

# Adjust layout
plt.subplots_adjust(hspace=0)

# Custom colormap similar to the gradient in the image
colors = [(0.9, 0.9, 0.9), (0.7, 0.7, 0.9), (0.5, 0.5, 0.9)]
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=100)

# Plot each sensor's data
for i in range(num_sensors):
    # Calculate y positions to stack the plots
    y_pos = num_sensors - i

    # Create subplot without internal axes
    ax = plt.subplot(num_sensors, 1, i+1)

    # Plot the sensor data line
    plt.plot(range(time_steps), sensor_data[i], 'k-', linewidth=1.5)

    # Fill area under the curve
    plt.fill_between(range(time_steps), 0, sensor_data[i],
                     alpha=0.3, color=cmap(i/num_sensors))

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
    plt.ylim(0, max(np.max(sensor_data) * 1.1, 100))

# Add title and labels
plt.xlabel("Time", fontsize=12)
plt.text(-5, num_sensors * 1.05, "Force", rotation=90, fontsize=12,
         transform=plt.gca().transAxes)

# Set the overall title
plt.suptitle("Tactile Sensor Readings", fontsize=14, y=0.95)

# Adjust the layout to ensure everything fits
plt.tight_layout(rect=[0, 0, 1, 0.95])

plt.savefig('tactile_sensor_plot.png', dpi=300, bbox_inches='tight')
plt.show()
