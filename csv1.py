import pandas as pd

# Load the CSV
df = pd.read_csv("test.csv")

# Forward-fill the 'Group' column to associate each box row with its group
df["Group"] = df["Group"].fillna(method="ffill")

# Filter rows that have a valid 'Type' value (this avoids the 'Group' header rows)
df_filtered = df[df["Type"].notna()]

# Group by Group and Type, count entries
summary = df_filtered.groupby(["Group", "Type"]).size().reset_index(name="count")

# Pivot to reshape the table with types as columns
pivot_summary = summary.pivot(index="Group", columns="Type", values="count").fillna(0).astype(int)

# Save to CSV
pivot_summary.reset_index(inplace=True)
pivot_summary.to_csv("box_summary_by_group.csv", index=False)

print(pivot_summary)
