"""
Backtests the assumption "beat estimates -> stock goes up" against real
historical outcomes. No model - just a direct correlation check between
surprise (beat/miss) and direction (up/down).
"""

from dataset_builder import dataset

beats = dataset[dataset["surprise"] > 0]
misses = dataset[dataset["surprise"] < 0]

beat_up_pct = (beats["direction"] == "up").mean()
miss_down_pct = (misses["direction"] == "down").mean()

correct = ((dataset["surprise"] > 0) & (dataset["direction"] == "up")) | \
          ((dataset["surprise"] < 0) & (dataset["direction"] == "down"))
overall_pct = correct.mean()

print("Total events:", len(dataset))
print("Beat events:", len(beats), "| of those, % that went up:", round(beat_up_pct * 100, 1))
print("Miss events:", len(misses), "| of those, % that went down:", round(miss_down_pct * 100, 1))
print("Overall (beat->up or miss->down):", round(overall_pct * 100, 1), "%")
