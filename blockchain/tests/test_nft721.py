import brownie
from brownie import NFT721
import pytest
from scripts.useful import get_account

ACCOUNT = get_account(0)


@pytest.fixture
def deploy_nft721():
    return NFT721.deploy("Dapp-z", "Z", {"from": ACCOUNT})


def test_mint(deploy_nft721):
    nft721 = deploy_nft721
    token_uri = "ipfs://sample"

    nft721.mint(token_uri, 250, {"from": ACCOUNT})

    assert nft721.tokenURI(1819) == token_uri

    with brownie.reverts():
        nft721.tokenURI(1900) == token_uri
