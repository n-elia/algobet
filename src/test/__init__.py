from typing import Callable

import pytest
from beaker import (
    sandbox
)
from beaker.sandbox import SandboxAccount

from test.conftest import logger


class TestBase:
    """
    Base class for smart contract testing routines.
    This class provides the basic fixture for retrieving accounts from sandbox and build
    application clients on top of them.
    """

    ###########################################
    # Test Accounts and Clients
    ###########################################
    @pytest.fixture(scope="class")
    def accounts(self):
        """Retrieve sandbox accounts. Accounts are re-listed for each TestBase subclass."""
        # Pop accounts from sandbox accounts
        return sandbox.get_accounts()

        # If using testnet
        # return sandbox.get_accounts(
        #     wallet_name=SANDBOX_WALLET_NAME,
        #     wallet_password=SANDBOX_WALLET_PASS
        # )

    @pytest.fixture(scope="class")
    def get_account(self, accounts) -> Callable[[], SandboxAccount]:
        """Pop an account from the list of sandbox accounts."""
        accounts_count = 0

        def _get_account():
            nonlocal accounts_count
            try:
                accounts_count += 1
                return accounts.pop()
            except IndexError:
                pytest.skip(f"Attempting to get {accounts_count} account from sandbox."
                            f"No more available accounts in sandbox!", allow_module_level=True)

        return _get_account
