# Configuration for gravitational wave event and lens parameters
GW_EVENT = "GW150914"  # Example gravitational wave event
DETECTOR = "H1"  # LIGO detector (can be H1, L1, etc.)

# Lens model parameters
LENS_PARAMETERS = {
    "einstein_radius": 1.6,  # Einstein radius in arcseconds
    "center": (0.0, 0.0),  # Center of the lens (x, y)
    "ellipticity": 0.2,  # Ellipticity of the lens
    "angle": 45.0  # Angle of the lens (degrees)
}

# Progress display settings
PROGRESS_CONFIG = {
    "bar_width": 40,
    "colour": "green",
    "unit": "step",
    "dynamic_ncols": True
}

# Expected maximum durations (seconds)
TIMING_THRESHOLDS = {
    "data_loading": 10,
    "waveform_processing": 8,
    "lens_modeling": 3,
    "lensing_application": 5,
    "visualization": 6
}