import brownie
from brownie import Market, Nft1155, Nft721, accounts
import pytest
import time

TOKEN_ID = 18
PRICE = 200000000000000000  # 2 ether


@pytest.fixture
def deploy_nft1155():
    return Nft1155.deploy({"from": accounts[0]})


@pytest.fixture
def deploy_nft721():
    return Nft721.deploy({"from": accounts[0]})


@pytest.fixture
def deploy_market():
    return Market.deploy({"from": accounts[0]})


def test_can_put_on_sale(deploy_market, deploy_nft1155, deploy_nft721):
    market = deploy_market
    nft721 = deploy_nft721
    nft1155 = deploy_nft1155
    starting_timestamp = int(time.time())
    ending_timestamp = int(time.time()) + 30

    nft721.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft721, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, False, {"from": accounts[0]})

    assert market.marketItems(1)[1] == TOKEN_ID
    assert market.marketItems(1)[2] == PRICE
    assert market.marketItems(1)[3] == accounts[0]

    nft1155.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft1155, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, True, {"from": accounts[0]})

    assert market.marketItems(1)[1] == TOKEN_ID
    assert market.marketItems(1)[2] == PRICE
    assert market.marketItems(1)[3] == accounts[0]


def test_cant_put_on_sale_not_approved(deploy_market, deploy_nft1155, deploy_nft721):
    market = deploy_market
    nft721 = deploy_nft721
    nft1155 = deploy_nft1155
    starting_timestamp = int(time.time())
    ending_timestamp = int(time.time()) + 30

    with brownie.reverts("The NFT is not approved!"):
        market.putOnSale(nft721, TOKEN_ID, PRICE,
                         starting_timestamp, ending_timestamp, False, {"from": accounts[0]})

    with brownie.reverts("The NFT is not approved!"):
        market.putOnSale(nft1155, TOKEN_ID, PRICE,
                         starting_timestamp, ending_timestamp, True, {"from": accounts[0]})


def test_cant_put_on_sale_not_owner(deploy_market, deploy_nft1155, deploy_nft721):
    market = deploy_market
    nft721 = deploy_nft721
    nft1155 = deploy_nft1155
    starting_timestamp = int(time.time())
    ending_timestamp = int(time.time()) + 30

    nft721.setApprovalForAll(market, True, {"from": accounts[0]})

    with brownie.reverts("The sender doesn't own NFT!"):
        market.putOnSale(nft721, TOKEN_ID, PRICE,
                         starting_timestamp, ending_timestamp, False, {"from": accounts[1]})

    nft1155.setApprovalForAll(market, True, {"from": accounts[0]})

    with brownie.reverts("The sender doesn't own NFT!"):
        market.putOnSale(nft1155, TOKEN_ID, PRICE,
                         starting_timestamp, ending_timestamp, True, {"from": accounts[1]})


def test_buy_now(deploy_market, deploy_nft1155, deploy_nft721):
    market = deploy_market
    nft721 = deploy_nft721
    nft1155 = deploy_nft1155
    starting_timestamp = int(time.time())
    ending_timestamp = int(time.time()) + 30

    nft721.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft721, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, False, {"from": accounts[0]})

    market.buyNow(1, False, {"from": accounts[1], "value": PRICE})

    assert market.marketItems(1)[6] == True

    nft1155.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft1155, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, True, {"from": accounts[0]})

    market.buyNow(2, True, {"from": accounts[1], "value": PRICE})

    assert market.marketItems(1)[6] == True


def test_cant_buy_now_sold(deploy_market, deploy_nft1155, deploy_nft721):
    market = deploy_market
    nft721 = deploy_nft721
    nft1155 = deploy_nft1155
    starting_timestamp = int(time.time())
    ending_timestamp = int(time.time()) + 30

    nft721.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft721, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, False, {"from": accounts[0]})

    market.buyNow(1, False, {"from": accounts[1], "value": PRICE})

    with brownie.reverts("The item has already been sold!"):
        market.buyNow(1, False, {"from": accounts[1], "value": PRICE})

    nft1155.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft1155, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, True, {"from": accounts[0]})

    market.buyNow(2, True, {"from": accounts[1], "value": PRICE})

    with brownie.reverts("The item has already been sold!"):
        market.buyNow(2, True, {"from": accounts[1], "value": PRICE})


def test_cant_buy_now_canceled(deploy_market, deploy_nft1155, deploy_nft721):
    market = deploy_market
    nft721 = deploy_nft721
    nft1155 = deploy_nft1155
    starting_timestamp = int(time.time())
    ending_timestamp = int(time.time()) + 30

    nft721.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft721, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, False, {"from": accounts[0]})

    market.cancelSale(1, {"from": accounts[0]})

    with brownie.reverts("The sale canceled!"):
        market.buyNow(1, False, {"from": accounts[1], "value": PRICE})

    nft1155.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft1155, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, True, {"from": accounts[0]})

    market.cancelSale(2, {"from": accounts[0]})

    with brownie.reverts("The sale canceled!"):
        market.buyNow(2, True, {"from": accounts[1], "value": PRICE})


def test_cant_buy_now_wrong_value(deploy_market, deploy_nft1155, deploy_nft721):
    market = deploy_market
    nft721 = deploy_nft721
    nft1155 = deploy_nft1155
    starting_timestamp = int(time.time())
    ending_timestamp = int(time.time()) + 30
    wrong_amount = 100

    nft721.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft721, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, False, {"from": accounts[0]})

    with brownie.reverts("Value must be equal to the price!"):
        market.buyNow(1, False, {"from": accounts[1], "value": wrong_amount})

    nft1155.setApprovalForAll(market, True, {"from": accounts[0]})

    market.putOnSale(nft1155, TOKEN_ID, PRICE,
                     starting_timestamp, ending_timestamp, True, {"from": accounts[0]})

    with brownie.reverts("Value must be equal to the price!"):
        market.buyNow(2, True, {"from": accounts[1], "value": wrong_amount})
