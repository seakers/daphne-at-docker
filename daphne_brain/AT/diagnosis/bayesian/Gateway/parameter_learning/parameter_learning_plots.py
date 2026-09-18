# parameter_learning_plots.py
#  Author: Joshua Elston
# Last Edited: 04/06/2026

# Plot data from testing_results.csv to see parameter learning
# performance (measured by simulation/learning speed) with
# different numbers of workers

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('testing_results.csv')

# Drop failed runs from dataset (with a value of -1)
df = df[df['total_time'] > 0].copy()

# Only keep columns of interest for plotting
df = df[['workers', 'ticks', 'sim_time', 'be_time', 'total_time']]

# Set the baseline time to compare to in the 500 and 1,000 tick cases
baseline = df[df['workers'] == 1].set_index('ticks')['total_time']
df['speedup'] = df.apply(lambda r: baseline[r['ticks']] / r['total_time'], axis=1)

# Ideal speedup (theoretical performance ceiling)
df['ideal_speedup'] = df['workers']

# Parallel efficiency
df['parallel_efficiency'] = df['speedup'] / df['workers']

# Fraction of time spent in simulation vs parameter learning
df['sim_fraction'] = df['sim_time'] / df['total_time']
df['be_fraction'] = df['be_time'] / df['total_time']

# print(df)

# Plot the number of workers against total runtime (simulation + parameter learning)
fig, ax = plt.subplots(figsize=(8,8))
for tick_count, group in df.groupby('ticks'):
    ax.plot(group['workers'], group['total_time'], marker = 'o', label=f'{tick_count} ticks')

ax.set_xlabel('Number of Workers')
ax.set_ylabel('Total Runtime [s]')
ax.set_title(f'Workers vs. Total Runtime')
ax.legend()
plt.show()

# Plot the speedup of the total runtime relative to the baseline (workers = 1)
# per the number of workers
fig, ax = plt.subplots(figsize=(8,8))
for tick_count, group in df.groupby('ticks'):
    ax.plot(group['workers'], group['speedup'], marker = 'o', label=f'{tick_count} ticks')

ax.set_xlabel('Number of Workers')
ax.set_ylabel('Speedup (Relative to 1 Worker Baseline)')
ax.set_title(f'Speedup Relative to Baseline Performance')
ax.legend()
plt.show()

# Create boxplots with simulation and parameter learning fractions of
# total runtime
fig, axes = plt.subplots(1, len(df["ticks"].unique()), figsize=(14, 6), sharey=True)

for ax, (tick_count, group) in zip(axes, df.groupby("ticks")):
    group = group.sort_values("workers")
    x = group["workers"].astype(str)  # use strings so matplotlib treats them as categories
    
    ax.bar(x, group["sim_time"],  label="Simulation")
    ax.bar(x, group["be_time"], bottom=group["sim_time"], label="Parameter Learning")
    
    ax.set_title(f"{tick_count} ticks")
    ax.set_xlabel("Number of Workers")
    ax.set_ylim(0, max(group['total_time']) + 25)

axes[0].set_ylabel("Total Time [s]")
axes[1].legend()
plt.suptitle("Runtime Composition by Worker Count")
plt.tight_layout()
plt.show()