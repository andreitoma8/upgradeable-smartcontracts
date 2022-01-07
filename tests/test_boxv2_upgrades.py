from _pytest.config import exceptions
from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
import pytest


def test_proxy_upgrades():
    # Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encode_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encode_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    # Act 1
    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    # Assert 1
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    # Act 2
    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    # Assert 2
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
