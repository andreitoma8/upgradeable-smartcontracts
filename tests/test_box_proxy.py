from scripts.helpful_scripts import encode_function_data, get_account
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_proxy_delegates_calls():
    # Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    # Act
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    # Assert
    assert proxy_box.retrieve() == 0
    # Act
    proxy_box.store(1, {"from": account})
    # Assert
    assert proxy_box.retrieve() == 1
