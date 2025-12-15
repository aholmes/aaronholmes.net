plt.figure(figsize=(15, 10))
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))
plt.plot(california_change.index, california_zscore, marker='o', label='California', color=COLOR1)
plt.plot(texas_change.index, texas_zscore, marker='o', label='Texas', color=COLOR2)
for i in range(len(california_zscore) - 1):
    fill_data = get_fill_data(i, california_change, texas_change, california_zscore, texas_zscore)
    ca_change = fill_data.change1
    tx_change = fill_data.change2
    plot_fill(ca_change, tx_change, fill_data)
plt.title('Normalized Year-over-Year Percentage Change in Population for California and Texas')
plt.xlabel('Year')
plt.ylabel('Z-Score of % Change')
draw_legend('California', 'Texas')
plt.grid(True)
plt.show()
