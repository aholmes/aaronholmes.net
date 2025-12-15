colors = ["green", "yellow", "red"]
cmap = LinearSegmentedColormap.from_list("mycmap", colors)
norm = plt.Normalize(0, len(average_annual_rate_of_change_sorted) - 1)
fig, ax = plt.subplots(figsize=(15, 10))
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))
bars = plt.bar(
    average_annual_rate_of_change_sorted.index,
    average_annual_rate_of_change_sorted,
    color=[cmap(norm(i)) for i in range(len(average_annual_rate_of_change_sorted))],
    zorder=2 # hide grid behind bars
)
ax = plt.gca()
for state in ['California', 'Texas']:
    idx = average_annual_rate_of_change_sorted.index.get_loc(state)
    bar = bars[idx]
    x = bar.get_x() + bar.get_width() / 2
    ax.axvline(x=x, color='red', linestyle='--', linewidth=1)
plt.title('Average Annual Rate of Change in Population for All States')
plt.xlabel('State')
plt.ylabel('Average Annual Rate of Change (%)')
plt.xticks(rotation=90)
plt.grid(True, zorder=0) # hide grid behind bars
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
sm.set_clim(0, len(average_annual_rate_of_change_sorted) - 1)
cbar_ax = fig.add_axes([0.161, 0.86, 0.698, 0.02])
cbar = plt.colorbar(sm, cax=cbar_ax, orientation='horizontal')
cbar.set_ticks([])
cbar_ax.text(0.0, 0.5, 'Highest Growth', va='center', ha='left', color='white', fontweight='bold', transform=cbar_ax.transAxes)
cbar_ax.text(0.5, 0.5, 'Moderate Growth', va='center', ha='center', color='black', fontweight='bold', transform=cbar_ax.transAxes)
cbar_ax.text(1.0, 0.5, 'Loss', va='center', ha='right', color='white', fontweight='bold', transform=cbar_ax.transAxes)
plt.show()
