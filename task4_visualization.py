import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the analysed data from Task 3
input_file = "data/trends_analysed.csv"
df = pd.read_csv(input_file)

# Create the output folder if it does not exist
os.makedirs("outputs", exist_ok=True)


# ============================================================
# Chart 1 - Top 10 Stories by Score
# ============================================================

# Select the 10 stories with the highest scores
top_stories = df.nlargest(10, "score").copy()

# Shorten long titles for better readability
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

plt.figure(figsize=(10, 7))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

# Put the highest-scoring story at the top
plt.gca().invert_yaxis()

plt.tight_layout()

# Save before displaying
plt.savefig("outputs/chart1_top_stories.png", dpi=150)

plt.show()
plt.close()


# ============================================================
# Chart 2 - Stories per Category
# ============================================================

category_counts = df["category"].value_counts()

plt.figure(figsize=(9, 6))

# Give each category bar a different colour
plt.bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ]
)

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.xticks(rotation=20)

plt.tight_layout()

# Save before displaying
plt.savefig("outputs/chart2_categories.png", dpi=150)

plt.show()
plt.close()


# ============================================================
# Chart 3 - Score vs Comments
# ============================================================

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(10, 7))

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    color="green",
    alpha=0.7
)

plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    color="red",
    alpha=0.7
)

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()

# Save before displaying
plt.savefig("outputs/chart3_scatter.png", dpi=150)

plt.show()
plt.close()


# ============================================================
# Bonus - TrendPulse Dashboard
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 11))

fig.suptitle(
    "TrendPulse Dashboard",
    fontsize=18,
    fontweight="bold"
)


# Dashboard Chart 1
axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story")

axes[0, 0].invert_yaxis()


# Dashboard Chart 2
axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ]
)

axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")

axes[0, 1].tick_params(axis="x", rotation=20)


# Dashboard Chart 3
axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    color="green",
    alpha=0.7
)

axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    color="red",
    alpha=0.7
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Comments")
axes[1, 0].legend()


# Use the fourth dashboard area for a summary
axes[1, 1].axis("off")

summary_text = (
    f"Total Stories: {len(df)}\n\n"
    f"Average Score: {df['score'].mean():.2f}\n\n"
    f"Average Comments: {df['num_comments'].mean():.2f}\n\n"
    f"Most Common Category: {category_counts.idxmax()}"
)

axes[1, 1].text(
    0.5,
    0.5,
    summary_text,
    ha="center",
    va="center",
    fontsize=14
)

plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the complete dashboard
plt.savefig("outputs/dashboard.png", dpi=150)

plt.show()
plt.close()

print("\nVisualization complete!")
print("Saved:")
print("  outputs/chart1_top_stories.png")
print("  outputs/chart2_categories.png")
print("  outputs/chart3_scatter.png")
print("  outputs/dashboard.png")
