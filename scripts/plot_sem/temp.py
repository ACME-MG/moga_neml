import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Sample data for three different datasets with different scales
data_list = [
    np.random.normal(loc=0, scale=1, size=100),
    np.random.normal(loc=5, scale=2, size=100),
    np.random.normal(loc=10, scale=3, size=100),
]
y_limits = [(-3, 3), (0, 15), (5, 20)]

# Create subplots for each boxplot with specified subplot widths and individual scales
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8, 4), sharey=False)

for i, axis in enumerate(axes):
    x_list = [i+1] * len(data_list[i])
    sns.boxplot(x=x_list, y=data_list[i], ax=axis, color="orange", width=0.4, showfliers=False)
    sns.stripplot(x=x_list, y=data_list[i], ax=axis, color="black", alpha=0.5)
    axis.set_ylim(y_limits[i])

# Adjust layout
fig.tight_layout()

# Display the plot
plt.savefig("box.png")
