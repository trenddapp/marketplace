from brownie import NFT721, NFT721Factory
from scripts.useful import get_account

ACCOUNT = get_account()


def deploy_marketplace_erc721():
    marketplace_erc721 = NFT721.deploy(
        "Dapp-z",
        "Z",
        {"from": ACCOUNT},
        publish_source=True,
    )
    return marketplace_erc721


def deploy_erc721_factory():
    erc721_factory = NFT721Factory.deploy(
        {"from": ACCOUNT},
        publish_source=True,
    )
    return erc721_factory


def main():
    marketplace_erc721 = deploy_marketplace_erc721()
    print(marketplace_erc721)
    erc721_factory = deploy_erc721_factory()
    print(erc721_factory)
