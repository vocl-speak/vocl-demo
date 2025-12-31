"""
EMG Signal Visualizer Component

Component for visualizing EMG signals in the Streamlit demo.
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def plot_emg_signals(emg_data):
    """
    Plot 4-channel EMG signals.
    
    Args:
        emg_data: EMG data array of shape (4, 5) - 4 channels, 5 timesteps
        
    Returns:
        matplotlib figure
    """
    channels = ['DLI', 'OOS', 'OOI', 'Platysma']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    fig.suptitle('EMG Signal Channels', fontsize=14, fontweight='bold')
    
    time_points = np.arange(5) * 4  # 4ms per sample
    
    for i, (channel, color) in enumerate(zip(channels, colors)):
        axes[i].plot(time_points, emg_data[i], marker='o', color=color, linewidth=2, markersize=6)
        axes[i].set_ylabel(channel, fontweight='bold')
        axes[i].grid(True, alpha=0.3)
        axes[i].set_ylim([0, 1])  # Normalized data range
    
    axes[-1].set_xlabel('Time (ms)', fontweight='bold')
    plt.tight_layout()
    
    return fig
