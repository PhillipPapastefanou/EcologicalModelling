import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 1. The baseline data for Taiwan
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Taiwan_Cumulative_Cases': [19029, 21029, 24029, 124029, 2124029, 3924029, 
                                4674029, 5424029, 6624029, 7824029, 8374029, 8824029]
}

df = pd.DataFrame(data)

# 2. Set up the figure with a clean, modern aesthetic
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#f8f9fa')
ax.set_facecolor('#f8f9fa')

# 3. Plot the line with thicker weight and white-edged markers
line_color = '#2a9d8f' # A modern teal
ax.plot(df['Month'], df['Taiwan_Cumulative_Cases'], 
        marker='o', markersize=10, markeredgecolor='white', markeredgewidth=2.5,
        color=line_color, linewidth=3.5, zorder=3,
        label='Taiwan Cumulative Cases\nSource: Reconstructed Baseline Data')

# Add subtle shading under the line
ax.fill_between(df['Month'], df['Taiwan_Cumulative_Cases'], color=line_color, alpha=0.15, zorder=2)

# 4. Format the axes and titles
ax.set_title('Taiwan: Cumulative COVID-19 Cases (2022)', 
             fontsize=18, fontweight='800', color='#343a40', pad=20, loc='left')
ax.set_xlabel('Month (2022)', fontsize=12, fontweight='600', color='#495057', labelpad=10)
ax.set_ylabel('Total Cases (Millions)', fontsize=12, fontweight='600', color='#495057', labelpad=10)

# Format the Y-axis to millions
def millions_formatter(x, pos):
    return f'{x / 1e6:.1f}M'
ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

# 5. Clean up the grid and spines (borders)
ax.grid(axis='y', linestyle='-', alpha=0.7, color='#e9ecef', zorder=1)
ax.grid(axis='x', visible=False) # Hide vertical grid lines for a cleaner look

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ced4da')
ax.spines['bottom'].set_color('#ced4da')

# Tweak tick parameters to look softer
ax.tick_params(axis='both', colors='#495057', labelsize=11, length=0, pad=8)

# 6. Add the legend
legend = ax.legend(loc='upper left', fontsize=11, frameon=True, facecolor='white', edgecolor='#ced4da')
legend.get_frame().set_alpha(0.9)

# 7. Add visual data labels to key milestones (Start, Mid-Surge, End)
key_indices = [0, 5, 11] # Indices for Jan, Jun, Dec
for idx in key_indices:
    month = df['Month'].iloc[idx]
    val = df['Taiwan_Cumulative_Cases'].iloc[idx]
    
    # Format text based on size
    if val < 1000000:
        text = f"{val:,.0f}"
    else:
        text = f"{val / 1e6:.1f}M"
        
    ax.annotate(text, 
                xy=(month, val), 
                xytext=(0, 12), textcoords='offset points',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='#1d3557',
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=line_color, alpha=0.8))

# 8. Render the plot
plt.tight_layout()
plt.savefig("taiwan_covid_cases.png")