import matplotlib.pyplot as plt
from gwpy.plot import Plot
import os


def plot_waveforms(original, lensed, event_name="", save_path=None):
    """
    Generate professional comparison plots with proper formatting

    Args:
        original: Unlensed TimeSeries
        lensed: Lensed TimeSeries
        event_name: Event identifier for titles
        save_path: Optional path to save figure
    """
    # Create output directory if needed
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Create figure
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle(f"Gravitational Wave Lensing: {event_name}", y=1.02)

    # Time domain plot
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(original.times, original, label='Original', alpha=0.8)
    ax1.plot(lensed.times, lensed, label='Lensed', alpha=0.8)
    ax1.set_xlabel('Time [GPS]')
    ax1.set_ylabel('Strain')
    ax1.legend()
    ax1.grid(True)

    # Frequency domain plot
    ax2 = fig.add_subplot(2, 1, 2)
    asd_original = original.asd(fftlength=4)
    asd_lensed = lensed.asd(fftlength=4)
    ax2.plot(asd_original.frequencies, asd_original, label='Original')
    ax2.plot(asd_lensed.frequencies, asd_lensed, label='Lensed')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('ASD [strain/√Hz]')
    ax2.legend()
    ax2.grid(True)

    # Adjust layout and save
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()