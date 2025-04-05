import autolens as al
from src.config import LENS_PARAMETERS
import logging
import numpy as np


def create_lens_model(einstein_radius=None, center=None, ellipticity=None, angle=None):
    """
    Creates a physically motivated gravitational lens model with configurable parameters.

    Args:
        einstein_radius: Optional override for Einstein radius (arcsec)
        center: Optional override for lens center (x,y)
        ellipticity: Optional override for ellipticity (0-1)
        angle: Optional override for orientation angle (degrees)

    Returns:
        lens_galaxy (autolens.Galaxy): Configured lens galaxy model
    """
    # Use config defaults if parameters not provided
    params = {
        "einstein_radius": einstein_radius or LENS_PARAMETERS["einstein_radius"],
        "center": center or LENS_PARAMETERS["center"],
        "ellipticity": ellipticity or LENS_PARAMETERS["ellipticity"],
        "angle": angle or LENS_PARAMETERS["angle"]
    }

    logging.info("Creating lens model with parameters:")
    logging.info(f"• Einstein radius: {params['einstein_radius']} arcsec")
    logging.info(f"• Center: {params['center']}")
    logging.info(f"• Ellipticity: {params['ellipticity']}")
    logging.info(f"• Angle: {params['angle']}°")

    # Convert angle to radians for calculations
    angle_rad = np.radians(params["angle"])

    # Calculate ellipticity components (correct modern AutoLens API approach)
    ell_comps = (
        params["ellipticity"] * np.cos(2 * angle_rad),
        params["ellipticity"] * np.sin(2 * angle_rad)
    )

    lens_galaxy = al.Galaxy(
        redshift=0.5,  # Typical lens redshift
        mass=al.mp.Isothermal(
            centre=params["center"],
            einstein_radius=params["einstein_radius"],
            ell_comps=ell_comps
        )
    )

    return lens_galaxy