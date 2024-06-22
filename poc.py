#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
from datetime import datetime


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-usage.ndjson>")
        sys.exit(1)

    usage_file_path = sys.argv[1]

    data = []
    with open(usage_file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))

    # Convert timestamps to datetime objects
    timestamps = [datetime.fromisoformat(entry["timestamp"]) for entry in data]

    # Calculate elapsed time in seconds
    elapsed_time = np.array([(ts - timestamps[0]).total_seconds() for ts in timestamps])

    # Extract other data
    pmem = np.array([entry["totals"]["pmem"] for entry in data])
    pcpu = np.array([entry["totals"]["pcpu"] for entry in data])
    rss_kb = np.array([entry["totals"]["rss_kb"] for entry in data])
    vsz_kb = np.array([entry["totals"]["vsz_kb"] for entry in data])

    # Plotting
    fig, ax1 = plt.subplots()

    # Plot pmem and pcpu on primary y-axis
    ax1.plot(elapsed_time, pmem, label='pmem (%)', color='tab:blue')
    ax1.plot(elapsed_time, pcpu, label='pcpu (%)', color='tab:orange')
    ax1.set_xlabel('Elapsed Time (s)')
    ax1.set_ylabel('Percentage')
    ax1.legend(loc='upper left')

    # Create a second y-axis for rss and vsz
    ax2 = ax1.twinx()
    ax2.plot(elapsed_time, rss_kb, label='rss (KiB)', color='tab:green')
    ax2.plot(elapsed_time, vsz_kb, label='vsz (KiB)', color='tab:red')
    ax2.set_ylabel('KiB')
    ax2.legend(loc='upper right')

    plt.title('Resource Usage Over Time')
    # plt.savefig('resource_usage.png')
    plt.show()


if __name__ == "__main__":
    main()
