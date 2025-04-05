from gwpy.timeseries import TimeSeries


def load_gw_data(event="GW150914", detector="H1"):
    """
    Loads real gravitational wave strain data from LIGO.

    Args:
        event (str): Gravitational wave event name.
        detector (str): Detector used (e.g., 'H1' for LIGO Hanford).

    Returns:
        strain (gwpy.timeseries.TimeSeries): Gravitational wave strain data.
    """
    print(f"Loading data for {event} from {detector} detector...")

    # GW150914 occurred at 09:50:45 UTC on September 14, 2015
    # Using a 32-second window centered on the event
    center_time = '2015-09-14 09:50:45'
    strain = TimeSeries.fetch_open_data(detector,
                                        start=center_time,
                                        end='2015-09-14 09:51:17')  # 32-second window

    # Verify we got enough data
    if len(strain) < 100:
        raise ValueError(f"Only got {len(strain)} samples. Try a longer time window.")

    return strain


# Example usage
try:
    strain_data = load_gw_data()
    print(f"Successfully loaded {len(strain_data)} samples")
    print(f"Sample rate: {1 / strain_data.dt} Hz")
    print(strain_data)
except Exception as e:
    print(f"Error loading data: {str(e)}")