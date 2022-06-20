import brownie
from brownie import NFT1155
import pytest
from scripts.useful import get_account

ACCOUNT = get_account(0)


@pytest.fixture
def deploy_nft1155():
    return NFT1155.deploy("TrendDapp", "TD", {"from": ACCOUNT})


def test_name_and_symbol(deploy_nft1155):
    nft1155 = deploy_nft1155
    name = "TrendDapp"
    symbol = "TD"

    assert nft1155.name() == name

    assert nft1155.symbol() == symbol


def test_mint(deploy_nft1155):
    nft1155 = deploy_nft1155
    token_uri = "ipfs://sample"
    amount = 2
    token_id = 1819
    royalty = 250

    nft1155.mint(token_uri, amount, royalty, "", {"from": ACCOUNT})

    assert nft1155.balanceOf(ACCOUNT, token_id) == amount

    assert nft1155.uri(token_id) == token_uri


def test_royalty(deploy_nft1155):
    nft1155 = deploy_nft1155
    token_uri = "ipfs://sample"
    token_id = 1819
    amount = 2
    royalty = 250
    sale_price = 200000000000000000  # 2 ether

    nft1155.mint(token_uri, amount, royalty, "", {"from": ACCOUNT})

    assert nft1155.royaltyInfo(token_id, sale_price) == (
        ACCOUNT, int(sale_price*royalty/10000))
