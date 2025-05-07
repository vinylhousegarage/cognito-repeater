import logging
import subprocess
from mangum import Mangum
from app import create_app

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_package_versions():
    logger.info('log_package_versions() was called!')
    try:
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
        logger.info('Installed packages:\n%s', result.stdout)
    except Exception as e:
        logger.error('Failed to run pip freeze: %s', str(e))

app = create_app()

log_package_versions()

handler = Mangum(app)
