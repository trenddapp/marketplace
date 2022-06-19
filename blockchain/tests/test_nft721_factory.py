from brownie import NFT721Factory
import pytest
from scripts.useful import get_account

ACCOUNT = get_account(0)


@pytest.fixture
def deploy_nft721_factory():
    return NFT721Factory.deploy({"from": ACCOUNT})


def test_collection_creation(deploy_nft721_factory):
    nft721_factory = deploy_nft721_factory
    name = "TrendDapp"
    symbol = "TD"

    tx = nft721_factory.createCollection(name, symbol, {"from": ACCOUNT})
    tx.wait(1)

    assert tx.events["CollectionCreated"] is not None

    assert tx.events["CollectionCreated"]["name"] == name

    assert tx.events["CollectionCreated"]["symbol"] == symbol
