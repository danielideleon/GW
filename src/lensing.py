import numpy as np
from gwpy.timeseries import TimeSeries


def apply_lensing(waveform, lens_model, plot=False):
    """
    Applies gravitational lensing effects to a GW waveform with proper time-shifting.

    Args:
        waveform: Input GW waveform (TimeSeries)
        lens_model: PyAutoLens galaxy model
        plot: Generate verification plots (bool)

    Returns:
        lensed_waveform: TimeSeries with lensing effects
    """
    print(f"Applying lensing with Einstein radius {lens_model.mass.einstein_radius} arcsec...")

    # Extract lens parameters
    einstein_radius = lens_model.mass.einstein_radius
    redshift = lens_model.redshift

    # Convert Einstein radius to time delay (simplified cosmology)
    # 1 arcsec ~ 10 days delay for z_lens=0.5, z_source=2.0
    delay_seconds = einstein_radius * 10 * 86400  # Convert to seconds

    # Calculate magnification (simplified from lensing theory)
    magnification = 1 + (einstein_radius / 2) ** 2

    # Create primary and secondary images
    primary = waveform * np.sqrt(magnification)

    # Create time-shifted secondary image
    secondary = waveform * np.sqrt(magnification - 1)
    secondary = time_shift(secondary, delay_seconds)

    # Combine signals
    lensed = primary + secondary

    if plot:
        plot_lensing_effects(waveform, lensed, delay_seconds)

    return lensed


def time_shift(ts, delay_seconds):
    """Helper function to implement time-shifting for TimeSeries"""
    # Calculate number of samples to shift
    delay_samples = int(delay_seconds * ts.sample_rate.value)

    # Create new array with shifted data
    shifted_data = np.roll(ts.value, delay_samples)

    # Create new TimeSeries with same metadata
    return TimeSeries(
        shifted_data,
        t0=ts.t0,
        dt=ts.dt,
        unit=ts.unit,
        name=f"Time-shifted {ts.name}",
        channel=ts.channel
    )


def plot_lensing_effects(original, lensed, delay):
    """Visualization of lensing effects"""
    from gwpy.plot import Plot
    import matplotlib.pyplot as plt

    # Create plot
    plot = Plot(figsize=(12, 10))

    # Time domain around merger
    merger_time = 1126259462.4 if "GW150914" in str(original.channel) else original.times[-1].value / 2
    zoom_start = merger_time - 0.5
    zoom_end = merger_time + 0.5 + delay / 86400  # Include delay in days

    ax1 = plot.add_subplot(2, 1, 1)
    ax1.plot(original.times, original, label='Original')
    ax1.plot(lensed.times, lensed, label=f'Lensed (Δt={delay / 86400:.2f} days)')
    ax1.set_xlim(zoom_start, zoom_end)
    ax1.set_xlabel('Time [GPS]')
    ax1.set_ylabel('Strain')
    ax1.legend()

    # Frequency domain comparison
    ax2 = plot.add_subplot(2, 1, 2)
    asd_original = original.asd(fftlength=4)
    asd_lensed = lensed.asd(fftlength=4)
    ax2.plot(asd_original.frequencies, asd_original, label='Original')
    ax2.plot(asd_lensed.frequencies, asd_lensed, label='Lensed')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlim(10, 1000)
    ax2.set_ylim(1e-24, 1e-19)
    ax2.legend()

    plt.tight_layout()
    plt.show()