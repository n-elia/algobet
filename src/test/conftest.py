import logging
import sys
import time
from datetime import datetime

import pytest
from beaker import sandbox
from py._xmlgen import html  # noqa

# Logger setup
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


# Add a "time" column to html output, to understand the tests execution order
@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    cells.insert(3, html.th('Time', class_='sortable time', col='time'))
    cells.pop()


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    cells.insert(3, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop()


def pytest_addoption(parser):
    parser.addoption("--sandbox", action="store_true", default=False, help="manage sandbox startup and teardown")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.sandbox
    if 'sandbox' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("enable_sandbox_management", [option_value])


# Sandbox
@pytest.fixture(scope="session")
def enable_sandbox_management(request):
    return request.config.getoption("--sandbox")


@pytest.fixture(scope="module")
def algod_client():
    """Return an `algod` client already configured for the sandbox."""
    return sandbox.get_algod_client()


@pytest.fixture(scope="session", autouse=True)
def sandbox_setup(enable_sandbox_management):
    """ Provide setup and teardown of session-scoped Algorand sandbox.
        Sandbox setup and teardown may be requested using `--sandbox` parameter.
    """
    # Shell scripts to manage the sandbox
    # Alternatively, sandbox binary with proper parameters can be used here
    setup_script_fp = 'src/test/sandbox-scripts/sandbox_setup.sh'
    teardown_script_fp = 'src/test/sandbox-scripts/sandbox_teardown.sh'

    def run_and_wait(script_filepath):
        import subprocess
        subprocess. \
            Popen(script_filepath, shell=True, stdout=sys.stdout, stderr=sys.stderr). \
            wait()

    # Start the sandbox, if --sandbox argument is provided
    if enable_sandbox_management:
        import subprocess
        logger.info("--sandbox argument provided -> starting the sandbox...")
        run_and_wait(setup_script_fp)

        # Wait a bit for sandbox containers to be reachable
        time.sleep(0.5)
    else:
        logger.info("--sandbox argument not provided -> skipping sandbox setup...")

    yield

    if enable_sandbox_management:
        import subprocess
        logger.info("--sandbox argument provided -> stopping the sandbox...")
        run_and_wait(teardown_script_fp)

    else:
        logger.info("--sandbox argument not provided -> skipping sandbox teardown...")
