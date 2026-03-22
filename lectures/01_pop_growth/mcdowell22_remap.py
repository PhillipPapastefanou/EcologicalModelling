import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Generate Approximated Data
# ---------------------------------------------------------
years = np.arange(1940, 2101)

# Base trends mimicking the exponential/quadratic increase in the image
# Temp goes from ~9.2 in 1940 to ~16.5 in 2100
# VPD goes from ~6.6 in 1940 to ~9.6 in 2100
temp_trend = 9.0 + 0.0001 * (years - 1940)**2.2
vpd_trend = 6.4 + 0.000045 * (years - 1940)**2.2

# Generate correlated noise to mimic the historical wiggles, 
# smoothing it slightly so it looks like climate model output
np.random.seed(42)
noise_base = np.random.normal(0, 0.15, len(years))
smoothed_noise = np.convolve(noise_base, np.ones(3)/3, mode='same')

# Apply noise
temp = temp_trend + smoothed_noise * 1.5
vpd = vpd_trend + smoothed_noise * 0.7

# Mimic the visible dip around 1970
dip_index = np.where((years > 1965) & (years < 1975))[0]
temp[dip_index] -= 0.3
vpd[dip_index] -= 0.15

# ---------------------------------------------------------
# 2. Replot the Figure
# ---------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 7))

# Define the colors from the original image
color_temp = '#a6b141' # Olive green
color_vpd = '#801b1b'  # Dark red

# --- Plot Temperature (Left Axis) ---
ax1.plot(years, temp, color=color_temp, linewidth=1.2)
ax1.set_xlabel('Year', fontsize=16)

# Style Temperature Y-axis label with the background box
ax1.set_ylabel('Temperature (°C)', color='black', fontsize=16, labelpad=15,
               bbox=dict(facecolor=color_temp, edgecolor='none', alpha=0.9, pad=5))

# Style Temperature Y-ticks
ax1.set_ylim(8.5, 17.5)
ax1.set_yticks([9, 11, 13, 15, 17])
ax1.tick_params(axis='y', labelsize=14)

# Add colored boxes to Left Y-tick labels
for label in ax1.get_yticklabels():
    label.set_bbox(dict(facecolor=color_temp, edgecolor='none', alpha=0.9, pad=3))

# Style X-axis ticks (rotated like the original)
ax1.set_xlim(1930, 2110)
ax1.set_xticks(np.arange(1940, 2101, 20))
ax1.tick_params(axis='x', rotation=45, labelsize=14)

# --- Plot Vapour Pressure Deficit (Right Axis) ---
ax2 = ax1.twinx()
ax2.plot(years, vpd, color=color_vpd, linewidth=1.2)

# Style VPD Y-axis label with the background box
ax2.set_ylabel('Vapour pressure deficit (hPa)', color='white', fontsize=16, 
               rotation=-90, labelpad=35,
               bbox=dict(facecolor=color_vpd, edgecolor='none', alpha=0.9, pad=5))

# Style VPD Y-ticks
ax2.set_ylim(6.0, 9.8)
ax2.set_yticks([6.5, 7.5, 8.5, 9.5])
ax2.tick_params(axis='y', labelcolor='white', labelsize=14)

# Add colored boxes to Right Y-tick labels
for label in ax2.get_yticklabels():
    label.set_color('white')
    label.set_bbox(dict(facecolor=color_vpd, edgecolor='none', alpha=0.9, pad=3))

# Final layout adjustments
plt.tight_layout()
plt.savefig("mcdowell22_t_vpg.png")