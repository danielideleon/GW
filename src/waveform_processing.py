import numpy as np
from gwpy.signal.filter_design import bandpass
from gwpy.plot import Plot
import matplotlib.pyplot as plt


def preprocess_waveform(strain, plot=False):
    """
    Enhanced processing with better time handling
    """
    # Convert to float32 to save memory
    strain = strain.astype('float32')

    # Get precise GPS times
    start_time = strain.t0.value
    end_time = strain.times[-1].value
    duration = end_time - start_time

    print(f"Processing {duration:.2f}s of data from GPS {start_time:.1f} to {end_time:.1f}")

    # 1. Bandpass Filter (safer implementation)
    try:
        bp_filter = bandpass(30, 400, strain.sample_rate)
        filtered = strain.filter(bp_filter, filtfilt=True)
    except ValueError as e:
        raise ValueError(f"Bandpass failed: {str(e)}") from e

    # 2. Whitening with buffer management
    whitened = filtered.whiten(fftlength=4, overlap=2, window='hann')

    # 3. Smart Cropping - keep central 24s (remove 4s from each end)
    crop_amount = 4  # seconds
    if duration > 2 * crop_amount:
        final_start = start_time + crop_amount
        final_end = end_time - crop_amount
        processed = whitened.crop(final_start, final_end)
    else:
        print("Warning: Not enough data for full cropping")
        processed = whitened

    # Visualization
    if plot:
        from gwpy.plot import Plot
        plot = Plot(figsize=(12, 8))

        # Time series comparison
        ax1 = plot.add_subplot(2, 1, 1)
        ax1.plot(strain.times, strain, label='Original')
        ax1.plot(processed.times, processed, label='Processed')
        ax1.set_xlim(processed.times[0].value, processed.times[-1].value)
        ax1.legend()

        # Frequency domain comparison
        ax2 = plot.add_subplot(2, 1, 2)
        asd_original = strain.asd(fftlength=4)
        asd_processed = processed.asd(fftlength=4)
        ax2.plot(asd_original.frequencies, asd_original, label='Original')
        ax2.plot(asd_processed.frequencies, asd_processed, label='Processed')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlim(10, 1000)
        ax2.legend()

        plot.show()

    return processed