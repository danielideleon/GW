from src.data_loader import load_gw_data
from src.waveform_processing import preprocess_waveform
from src.lens_model import create_lens_model
from src.lensing import apply_lensing
from src.plot_utils import plot_waveforms
from src.config import GW_EVENT, DETECTOR, LENS_PARAMETERS
from tqdm import tqdm
import time
import logging


def configure_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('gw_lensing.log'),
            logging.StreamHandler()
        ]
    )


def run_pipeline_step(step_func, description, *args, **kwargs):
    """Wrapper function to execute pipeline steps with progress tracking"""
    with tqdm(total=1, desc=description, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        start_time = time.time()
        result = step_func(*args, **kwargs)
        pbar.update(1)
        elapsed = time.time() - start_time
        logging.info(f"{description} completed in {elapsed:.2f}s")
        return result


def main():
    """
    Main pipeline for GW lensing analysis with progress tracking:
    1. Load GW data
    2. Preprocess waveform
    3. Create lens model
    4. Apply lensing effects
    5. Visualize results
    """
    configure_logging()

    try:
        # Initialize overall progress
        overall = tqdm(total=5, desc='Overall Progress', position=0)

        # Step 1: Data loading
        strain = run_pipeline_step(
            load_gw_data,
            "Loading GW data",
            event=GW_EVENT,
            detector=DETECTOR
        )
        overall.update(1)

        # Step 2: Waveform processing
        waveform = run_pipeline_step(
            preprocess_waveform,
            "Processing waveform",
            strain
        )
        overall.update(1)

        # Step 3: Lens modeling
        lens_model = run_pipeline_step(
            create_lens_model,
            "Creating lens model",
            einstein_radius=LENS_PARAMETERS["einstein_radius"],
            center=LENS_PARAMETERS["center"],
            ellipticity=LENS_PARAMETERS["ellipticity"],
            angle=LENS_PARAMETERS["angle"]
        )
        overall.update(1)

        # Step 4: Lensing application
        lensed_waveform = run_pipeline_step(
            apply_lensing,
            "Applying lensing effects",
            waveform,
            lens_model
        )
        overall.update(1)

        # Step 5: Visualization
        run_pipeline_step(
            plot_waveforms,
            "Generating visualizations",
            waveform,
            lensed_waveform,
            GW_EVENT
        )
        overall.update(1)

        overall.close()
        logging.info("Pipeline completed successfully")

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()