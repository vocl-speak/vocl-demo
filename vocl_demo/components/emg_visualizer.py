"""
EMG Signal Visualizer Component

Component for visualizing EMG signals in the Streamlit demo.
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


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


def plot_phoneme_emg_grid(emg_windows, phonemes):
    """
    Plot mini EMG graphs for each phoneme in a grid layout.
    
    Args:
        emg_windows: List of EMG data arrays, each of shape (4, 5)
        phonemes: List of phoneme strings corresponding to each EMG window
        
    Returns:
        matplotlib figure
    """
    if not emg_windows or not phonemes:
        return None
    
    n_phonemes = len(phonemes)
    channels = ['DLI', 'OOS', 'OOI', 'Platysma']
    colors = ['#1565c0', '#f57c00', '#00897b', '#c62828']  # Scientific color palette
    time_points = np.arange(5) * 4  # 4ms per sample
    
    # Calculate grid dimensions (prefer wider layout)
    if n_phonemes <= 4:
        ncols = n_phonemes
        nrows = 1
    elif n_phonemes <= 8:
        ncols = 4
        nrows = 2
    else:
        ncols = 4
        nrows = (n_phonemes + 3) // 4  # Round up
    
    # Create figure with subplots for each phoneme
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows))
    fig.suptitle('Electromyographic Signal Analysis - Multi-Channel EMG Patterns', 
                 fontsize=16, fontweight='bold', color='#000000', y=0.995)
    fig.patch.set_facecolor('white')
    
    # Handle single subplot case
    if n_phonemes == 1:
        axes = [axes]
    elif nrows == 1:
        axes = axes if isinstance(axes, np.ndarray) else [axes]
    else:
        axes = axes.flatten()
    
    for idx, (emg_data, phoneme) in enumerate(zip(emg_windows, phonemes)):
        ax = axes[idx]
        ax.set_facecolor('white')
        
        # Plot all 4 channels in the same subplot
        for i, (channel, color) in enumerate(zip(channels, colors)):
            ax.plot(time_points, emg_data[i], marker='o', color=color, 
                   linewidth=2.5, markersize=6, label=channel, alpha=0.9,
                   markerfacecolor=color, markeredgecolor='white', markeredgewidth=1)
        
        ax.set_title(f'{phoneme}', fontweight='bold', fontsize=12, color='#000000', pad=10)
        ax.set_ylim([0, 1])
        ax.set_xlim([0, 16])
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, color='#e0e0e0')
        ax.set_xlabel('Time (ms)', fontsize=10, fontweight='bold', color='#424242')
        ax.set_ylabel('Amplitude', fontsize=10, fontweight='bold', color='#424242')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#bdbdbd')
        ax.spines['bottom'].set_color('#bdbdbd')
        ax.tick_params(labelsize=9, colors='#424242')
    
    # Add legend below all graphs using handles from first subplot
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=4, fontsize=10, framealpha=0.9,
               edgecolor='#e0e0e0', facecolor='white', bbox_to_anchor=(0.5, -0.02))
    
    # Hide unused subplots
    for idx in range(n_phonemes, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    return fig


def plot_phoneme_emg_grid_interactive(emg_windows, phonemes):
    """
    Plot interactive EMG graphs for each phoneme using Plotly (with zoom functionality).
    
    Args:
        emg_windows: List of EMG data arrays, each of shape (4, 5)
        phonemes: List of phoneme strings corresponding to each EMG window
        
    Returns:
        plotly figure object
    """
    if not PLOTLY_AVAILABLE:
        # Fallback to matplotlib if plotly not available
        return plot_phoneme_emg_grid(emg_windows, phonemes)
    
    if not emg_windows or not phonemes:
        return None
    
    n_phonemes = len(phonemes)
    channels = ['DLI', 'OOS', 'OOI', 'Platysma']
    colors = ['#1565c0', '#f57c00', '#00897b', '#c62828']  # Scientific color palette
    time_points = np.arange(5) * 4  # 4ms per sample
    
    # Calculate grid dimensions - simpler layout: one subplot per phoneme
    if n_phonemes <= 4:
        ncols = n_phonemes
        nrows = 1
    elif n_phonemes <= 8:
        ncols = 4
        nrows = 2
    else:
        ncols = 4
        nrows = (n_phonemes + 3) // 4
    
    # Create subplots - one per phoneme, showing all 4 channels
    subplot_titles = [f'<b>{phoneme}</b>' for phoneme in phonemes]
    
    fig = make_subplots(
        rows=nrows,
        cols=ncols,
        subplot_titles=subplot_titles,
        vertical_spacing=0.15,
        horizontal_spacing=0.1,
        shared_xaxes=True,
        shared_yaxes=True
    )
    
    # Update layout for scientific appearance
    fig.update_layout(
        title={
            'text': 'Electromyographic Signal Analysis - Multi-Channel EMG Patterns',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#0d47a1', 'family': 'Arial, sans-serif'}
        },
        height=350 * nrows,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
            bgcolor='rgba(255, 255, 255, 0.8)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=11, color='#212121'),
        hovermode='closest'
    )
    
    # Plot each phoneme
    for phoneme_idx, (emg_data, phoneme) in enumerate(zip(emg_windows, phonemes)):
        row = (phoneme_idx // ncols) + 1
        col = (phoneme_idx % ncols) + 1
        
        # Plot all 4 channels in the same subplot
        for channel_idx, (channel, color) in enumerate(zip(channels, colors)):
            fig.add_trace(
                go.Scatter(
                    x=time_points,
                    y=emg_data[channel_idx],
                    mode='lines+markers',
                    name=channel if phoneme_idx == 0 else '',  # Only show legend once
                    line=dict(color=color, width=2.5),
                    marker=dict(size=7, color=color, line=dict(width=1, color='white')),
                    hovertemplate=f'<b>{phoneme} - {channel}</b><br>' +
                                  'Time: %{x:.1f} ms<br>' +
                                  'Amplitude: %{y:.3f}<br>' +
                                  '<extra></extra>',
                    legendgroup=channel,
                    showlegend=(phoneme_idx == 0)
                ),
                row=row,
                col=col
            )
        
        # Update axes for this subplot
        fig.update_xaxes(
            title_text='Time (ms)' if row == nrows else '',
            range=[0, 16],
            row=row,
            col=col,
            gridcolor='#e0e0e0',
            gridwidth=1,
            showgrid=True,
            zeroline=False
        )
        
        fig.update_yaxes(
            title_text='Amplitude' if col == 1 else '',
            range=[0, 1],
            row=row,
            col=col,
            gridcolor='#e0e0e0',
            gridwidth=1,
            showgrid=True,
            zeroline=False
        )
    
    # Hide unused subplots
    for idx in range(n_phonemes, nrows * ncols):
        row = (idx // ncols) + 1
        col = (idx % ncols) + 1
        fig.update_xaxes(visible=False, row=row, col=col)
        fig.update_yaxes(visible=False, row=row, col=col)
    
    return fig
