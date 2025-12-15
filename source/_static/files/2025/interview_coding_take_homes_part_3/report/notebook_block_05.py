class HandlerArrowLine(HandlerLine2D):
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        # Create a line and an arrowhead as separate artists
        padding = 2
        line = Line2D([xdescent + padding, width - xdescent], [height / 2, height / 2], linestyle=orig_handle.get_linestyle(), color=orig_handle.get_color())
        arrow = Line2D([xdescent + padding], [height / 2], marker='<', color=orig_handle.get_color(), markersize=fontsize / 2, linestyle='None')
        return [line, arrow]

plt.figure(figsize=(15, 10))
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions_formatter))
bars_2022 = plt.bar(pop_2022_sorted.index, pop_2022_sorted, color=COLOR5)
plt.title('Relative population rank change between 2013 and 2022')
plt.xlabel('State')
plt.ylabel('Population')
plt.xticks(rotation=90)

line_handles = [
    Line2D([0], [1], color=COLOR3, marker='<', linestyle='-', label='rank change'),
    Line2D([0], [1], color=COLOR1, marker='<', linestyle='-', label='top three largest rank changes'),
    Line2D([0], [1], color=COLOR2, marker='<', linestyle='-', label='top three smallest rank changes'),
]
block_handles = [
    patches.Patch(color=COLOR5, label='Population & unchanged rank'),
    patches.Patch(color=COLOR4, label='Population & changed rank')
]
plt.legend(handles=line_handles + block_handles,  handler_map={handle: HandlerArrowLine() for handle in line_handles}).get_frame().set_alpha(1)
ax = plt.gca()
for bar, state in zip(bars_2022, pop_2022_sorted.index):
    if state in changed_states:
        bar.set_color(COLOR4)
        prev_pos = order_2013.index(state)
        new_pos = order_2022.index(state)
        con = ConnectionPatch(
            xyA=(prev_pos, pop_2013_sorted[state]),
            xyB=(new_pos, pop_2022_sorted[state]),
            coordsA="data", coordsB="data",
            axesA=ax, axesB=ax,
            color=COLOR1 if state in top_3_states_by_position_change else (COLOR2 if state in bottom_3_states_by_position_change else COLOR3),
            arrowstyle=ArrowStyle("simple", head_width=1, head_length=1, tail_width=0.1), 
            fill=True,
            linewidth=1,
            connectionstyle="arc3,rad=0.9"
        )
        ax.add_patch(con)
plt.show()
