import os
import json
import matplotlib.pyplot as plt
import numpy as np

# path to the folder containing result JSON files
folder_path = rf"C:\Users\Lev\Documents\testing\LLM\opensbt-results\judge-eval\request_response\judge_eval_2025-09-24_00-31-52"
file_name = "metrics.json"

# collect data
results_f1 = {}     # {model: {technique: (f1, num_tests)}}
results_time = {}   # {model: {technique: (avg_time, num_tests)}}

for root, _, files in os.walk(folder_path):
    for file in files:
        if file == file_name:
            technique_name = os.path.basename(root)  # take folder name as technique
            with open(os.path.join(root, file), "r") as f:
                data = json.load(f)
                for model, metrics in data.items():
                    if model not in results_f1:
                        results_f1[model] = {}
                        results_time[model] = {}
                    f1 = metrics["overall"]["f1"]
                    avg_time = metrics["overall"]["avg_time"]
                    n = metrics["overall"]["num_tests"]
                    results_f1[model][technique_name] = (f1, n)
                    results_time[model][technique_name] = (avg_time, n)

# prepare data for plotting
techniques = sorted({t for m in results_f1.values() for t in m.keys()})
models = list(results_f1.keys())

print("models found:", len(models))

# helper function for plotting
def plot_metric(results, ylabel, title, is_f1=False):
    x = np.arange(len(techniques))
    bar_width = 0.6  # width of each individual bar
    group_spacing = 0.2  # space between groups

    fig, ax = plt.subplots(figsize=(15, 6))

    # use a colormap with moderately light but clear colors
    cmap = plt.get_cmap("Set2")

    num_models = len(models)
    bar_width = 0.35  # width of each bar
    group_spacing = 0.6  # space between groups (in x-axis units)

    x = np.arange(len(techniques)) * (num_models * bar_width + group_spacing)

    for i, model in enumerate(models):
        offsets = x + i * bar_width

        values = [results[model].get(t, (0, 0))[0] for t in techniques]
        ns = [results[model].get(t, (0, 0))[1] for t in techniques]
        bars = ax.bar(offsets, values, bar_width, label=model, color=cmap(i % cmap.N))

        # add metric value above bars and sample size inside bars
        for bar, val, n in zip(bars, values, ns):
            # metric value above bar
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (0.01 * max(values) if max(values) > 0 else 0.01),
                f"{val:.2f}",
                ha='center', va='bottom', fontsize=9
            )
            # # sample size inside bar
            # ax.text(
            #     bar.get_x() + bar.get_width() / 2,
            #     bar.get_height() / 2,
            #     f"({n})",
            #     ha='center', va='center', fontsize=9, color="black"
            # ) 

    # position tick labels in the center of each group
    group_centers = x + (len(models) - 1) * (bar_width / 2 + 0.005)
    ax.set_xticks(group_centers)
    ax.set_xticklabels(techniques, rotation=30, ha="right")

    ax.set_ylabel(ylabel)
    ax.set_title(title + f" (n = {n})")
    if is_f1:
        ax.set_ylim(0, 1.05)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.margins(x=0.05)  # small margin for spacing

    plt.tight_layout()
    plt.show()

# plot F1
plot_metric(results_f1, "F1 Score", "F1 Scores per Technique by Model", is_f1=True)

# plot Time
plot_metric(results_time, "Avg Time", "Average Time per Technique by Model", is_f1=False)
