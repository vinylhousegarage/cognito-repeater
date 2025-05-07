import logging
import subprocess
from mangum import Mangum
from app import create_app

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_package_versions():
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
    logger.info('Installed packages:\n%s', result.stdout)

app = create_app()

log_package_versions()

handler = Mangum(app)
