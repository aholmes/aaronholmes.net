class FillData(NamedTuple):
    year1: str
    year2: str
    zscore1: float
    zscore2: float
    change1: float
    change2: float
    middle_x: float
    middle_y: float

def zscore(change):
    """Calculate the zscore of a change."""
    return (change - change.mean()) / change.std()

def get_fill_data(year_idx, change1, change2, zscore1, zscore2):
    """Get data needed for plot_fill(...) and fill(...)"""
    year1, year2 = change1.index[i], change1.index[i + 1]
    zscore_change1 = zscore1.iloc[i + 1] - zscore1.iloc[i]
    zscore_change2 = zscore2.iloc[i + 1] - zscore2.iloc[i]
    middle_x = (year_idx + year_idx + 1) / 2
    middle_y = (zscore1.iloc[i] + zscore1.iloc[i + 1]) / 2
    return FillData(year1, year2, zscore1, zscore2, zscore_change1, zscore_change2, middle_x, middle_y)

def plot_fill(change1: float, change2: float, fill_data: FillData, color1: str = '#1f77b4', color2: str = '#ff7f0e'):
    """Draws the plot for fill data between fill_data.year1 and fill_data.year2"""
    if change1 < 0 and change2 < 0:  # Both changes are declining
        if abs(change1) > abs(change2):  # First change declines more
            fill(fill_data, color1, ('\u2193', color1), ('\u2193', color2), 0.5)
        else:  # Second change declines more
            fill(fill_data, color2, ('\u2193', color1), ('\u2193', color2), 0.5)
    elif change1 > 0 and change2 > 0:  # Both changes are growing
        if abs(change1) < abs(change2):  # Change1 grows less
            fill(fill_data, color2, ('\u2191', color1), ('\u2191', color2), 0.1)
        else:  # Change2 grows less
            fill(fill_data, color2, ('\u2191', color1), ('\u2191', color2), 0.1)
    else:  # One is growing, the other is declining
        change1_arrow = '\u2193' if change1 < 0 else '\u2191'
        change2_arrow = '\u2193' if change2 < 0 else '\u2191'
        if change1 < change2:  # Change1 declines more or grows less
            fill(fill_data, color1, (change1_arrow, color1), (change2_arrow, color2), 0.5)
        else:  # Change 2 declines more or grows less
            fill(fill_data, color2, (change1_arrow, color1), (change2_arrow, color2), 0.5)

def fill(
    fill_data: FillData,
    color: str,
    arrow_left: tuple[str, str],
    arrow_right: tuple[str, str],
    alpha: float
):
    """Fills the space between fill_data.year1 and fill_data.year2"""
    plt.fill_between([fill_data.year1, fill_data.year2],
                     fill_data.zscore1.iloc[i:i + 2], fill_data.zscore2.iloc[i:i + 2],
                     facecolor=color, alpha=alpha)
    middle_x = fill_data.middle_x
    middle_y = fill_data.middle_y
    plt.gca().add_patch(FancyBboxPatch((middle_x - 0.10, middle_y - 0.05), 0.1, 0.1,
                                        boxstyle="round,pad=0.01", facecolor='white', edgecolor='none', zorder=2))
    plt.gca().add_patch(FancyBboxPatch((middle_x + 0.0, middle_y - 0.05), 0.1, 0.1,
                                        boxstyle="round,pad=0.01", facecolor='white', edgecolor='none', zorder=2))
    plt.annotate(
        arrow_left[0],
        xy=(middle_x-0.05, middle_y),
        ha='center',
        va='center',
        color=arrow_left[1],
        fontsize=12
    )
    plt.annotate(
        arrow_right[0],
        xy=(middle_x+0.05, middle_y),
        ha='center',
        va='center',
        color=arrow_right[1],
        fontsize=12
    )

def draw_legend(line1_name: str, line2_name: str):
    line_handles = [
        Line2D([0], [0], color='#1f77b4', marker='o', linestyle='-', label=f'{" " * 10}{line1_name}'),
        Line2D([0], [0], color='#ff7f0e', marker='o', linestyle='-', label=f'{" " * 10}{line2_name}')
    ]
    arrow_handles = [
        Line2D([0], [0], color='none', marker='', linestyle='', label=f'\u2191{" " * 7}Mean-relative growth rate increase'),
        Line2D([0], [0], color='none', marker='', linestyle='', label=f'\u2193{" " * 7}Mean-relative growth rate decrease')
    ]
    block_handles = [
        patches.Patch(color='#1f77b4', alpha=0.25, label=f'{" " * 9}Lower {line1_name} rate increase'),
        patches.Patch(color='#ff7f0e', alpha=0.25, label=f'{" " * 9}Lower {line2_name} rate increase'),
        patches.Patch(color='#1f77b4', alpha=0.8, label=f'{" " * 9}Higher {line1_name} rate decrease'),
        patches.Patch(color='#ff7f0e', alpha=0.8, label=f'{" " * 9}Higher {line2_name} rate decrease')
    ]
    plt.legend(handles=line_handles + arrow_handles + block_handles, handletextpad=-1.4, loc='lower center').get_frame().set_alpha(1)
