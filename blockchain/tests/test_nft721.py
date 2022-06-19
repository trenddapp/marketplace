import brownie
from brownie import NFT721
import pytest
from scripts.useful import get_account

ACCOUNT = get_account(0)


@pytest.fixture
def deploy_nft721():
    return NFT721.deploy("TrendDapp", "TD", {"from": ACCOUNT})


def test_name_and_symbol(deploy_nft721):
    nft721 = deploy_nft721
    name = "TrendDapp"
    symbol = "TD"

    assert nft721.name() == name

    assert nft721.symbol() == symbol


def test_mint(deploy_nft721):
    nft721 = deploy_nft721
    token_uri = "ipfs://sample"
    token_id = 1819
    royalty = 250

    nft721.mint(token_uri, royalty, {"from": ACCOUNT})

    assert nft721.balanceOf(ACCOUNT) == 1

    assert nft721.ownerOf(token_id) == ACCOUNT

    assert nft721.tokenURI(token_id) == token_uri

    with brownie.reverts():
        nft721.tokenURI(1900) == token_uri


def test_royalty(deploy_nft721):
    nft721 = deploy_nft721
    token_uri = "ipfs://sample"
    token_id = 1819
    royalty = 250
    sale_price = 200000000000000000  # 2 ether

    nft721.mint(token_uri, royalty, {"from": ACCOUNT})

    assert nft721.royaltyInfo(token_id, sale_price) == (
        ACCOUNT, int(sale_price*royalty/10000))
