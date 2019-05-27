import os
import json

import matplotlib.pyplot as plt

import data_gen.util
from data_gen.config import matplotlib_config

matplotlib_config()

cur_dir = data_gen.util.curdir(__file__)
products_dir = os.path.join(data_gen.util.updir(cur_dir, 1), "products")


def plot_purity_results(results_path):
    key_map = {
        "test_complex_sinusoid": "freq",
        "test_time_domain_impulse": "offset"
    }

    purity_measures = [
        "max_spurious_power",
        "total_spurious_power",
        "mean_spurious_power"
    ]

    diff_measures = [
        "mean_diff",
        "total_diff"
    ]

    in_per_row = 4

    with open(results_path, "r") as f:
        results = json.load(f)

    def plot_results(x, x_label, dat, dat_labels):
        fig, axes = plt.subplots(len(dat), 1,
                                 figsize=(in_per_row*len(dat), 10))

        for i, label, d in zip(range(len(dat)), dat_labels, dat):
            axes[i].scatter(x, d)
            axes[i].set_title(label)
            axes[i].set_ylabel("Power (dB)")
            axes[i].set_xlabel(x_label)
            axes[i].grid(True)

        fig.tight_layout(rect=[0, 0.03, 1, 0.95])

        return fig, axes

    for key in key_map:
        domain_key = key_map[key]
        domain = []
        purity = []
        diff = []
        for val in results[key]:
            domain.append(val[domain_key])
            purity.append([val[k] for k in purity_measures])
            diff.append(val[k] for k in diff_measures)

        purity = list(zip(*purity))
        diff = list(zip(*diff))

        fig, axes = plot_results(domain, domain_key, purity, purity_measures)
        fig.suptitle(f"{key} Purity")
        fig.savefig(
            os.path.join(products_dir, f"purity.{key}.png"))

        fig, axes = plot_results(domain, domain_key, diff, diff_measures)
        fig.suptitle(f"{key} Difference")
        fig.savefig(
            os.path.join(products_dir, f"diff.{key}.png"))


if __name__ == "__main__":
    results_path = os.path.join(products_dir, "report.purity.json")
    plot_purity_results(results_path)