from brownie import NFT1155Factory
import pytest
from scripts.useful import get_account

ACCOUNT = get_account(0)


@pytest.fixture
def deploy_nft1155_factory():
    return NFT1155Factory.deploy({"from": ACCOUNT})


def test_collection_creation(deploy_nft1155_factory):
    nft1155_factory = deploy_nft1155_factory
    name = "TrendDapp"
    symbol = "TD"

    tx = nft1155_factory.createCollection(name, symbol, {"from": ACCOUNT})
    tx.wait(1)

    assert tx.events["CollectionCreated"] is not None

    assert tx.events["CollectionCreated"]["name"] == name

    assert tx.events["CollectionCreated"]["symbol"] == symbol
