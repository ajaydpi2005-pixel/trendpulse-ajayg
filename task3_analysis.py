import pandas as pd
import numpy as np

# Load the cleaned CSV created in Task 2
input_file = "data/trends_clean.csv"
df = pd.read_csv(input_file)

print(f"Loaded data: {df.shape}")

# Display the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and average number of comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")


# -------------------------------
# NumPy Statistics
# -------------------------------

scores = df["score"].to_numpy()

# Calculate mean, median and standard deviation using NumPy
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

# Find highest and lowest scores
highest_score = np.max(scores)
lowest_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {highest_score}")
print(f"Min score    : {lowest_score}")


# Find the category with the most stories
category_counts = df["category"].value_counts()
most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print(
    f"\nMost stories in: "
    f"{most_common_category} ({most_common_count} stories)"
)


# Find the story with the most comments
most_commented_index = df["num_comments"].idxmax()
most_commented_story = df.loc[most_commented_index, "title"]
most_commented_count = df.loc[most_commented_index, "num_comments"]

print(
    f'\nMost commented story: "{most_commented_story}" '
    f"— {most_commented_count} comments"
)


# -------------------------------
# Add New Columns
# -------------------------------

# Engagement measures comments relative to the number of upvotes
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# A story is popular when its score is above the average score
df["is_popular"] = df["score"] > average_score


# -------------------------------
# Save the analysed data
# -------------------------------

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
