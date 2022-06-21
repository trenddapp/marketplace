// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract Market {
    uint256 private marketItemIdCounter = 0;

    struct MarketItem {
        address nftContractAddress;
        uint256 tokenId;
        uint256 price;
        address payable seller;
        uint64 startingTimestamp;
        uint64 endingTimestamp;
        bool isSold;
        bool isCanceled;
    }
    mapping(uint256 => MarketItem) public marketItems;

    event ItemListed(uint256 itemId);

    event ItemSaleCenceled(uint256 itemId);

    event ItemSaleDurationUpdated(uint256 itemId);

    event ItemSalePriceClaimed(uint256 itemId);

    event ItemSalePriceUpdated(uint256 itemId);

    event ItemSold(uint256 itemId);

    modifier checkTimestamp(uint256 _itemId) {
        require(
            marketItems[_itemId].startingTimestamp <= block.timestamp,
            "The sale is not open!"
        );
        require(
            marketItems[_itemId].endingTimestamp >= block.timestamp,
            "The sale is over!"
        );
        _;
    }

    modifier checkValue(uint256 _itemId) {
        require(
            marketItems[_itemId].price == msg.value,
            "Value must be equal to the price!"
        );
        _;
    }

    modifier ifApprovedNft(address _nftContractAddress, uint256 _tokenId) {
        require(
            IERC721(_nftContractAddress).isApprovedForAll(
                msg.sender,
                address(this)
            ),
            "The NFT is not approved!"
        );
        _;
    }

    modifier notCanceled(uint256 _itemId) {
        require(!marketItems[_itemId].isCanceled, "Sale cancedled!");
        _;
    }

    modifier notSold(uint256 _itemId) {
        require(
            !marketItems[_itemId].isSold,
            "The item has already been sold!"
        );
        _;
    }

    modifier onlyNftOwner(
        address _nftContractAddress,
        uint256 _tokenId,
        bool _isERC1155
    ) {
        if (_isERC1155)
            require(
                IERC1155(_nftContractAddress).balanceOf(msg.sender, _tokenId) >
                    0,
                "The sender doesn't own NFT!"
            );
        else
            require(
                msg.sender == IERC721(_nftContractAddress).ownerOf(_tokenId),
                "The sender doesn't own NFT!"
            );
        _;
    }

    modifier onlySeller(uint256 _itemId) {
        require(
            msg.sender == marketItems[_itemId].seller,
            "The sender is not the seller!"
        );
        _;
    }

    function buyNow(uint256 _itemId, bool _isERC1155)
        external
        payable
        checkTimestamp(_itemId)
        notCanceled(_itemId)
        notSold(_itemId)
        checkValue(_itemId)
    {
        marketItems[_itemId].isSold = true;

        if (_isERC1155)
            IERC1155(marketItems[_itemId].nftContractAddress).safeTransferFrom(
                marketItems[_itemId].seller,
                msg.sender,
                marketItems[_itemId].tokenId,
                1,
                ""
            );
        else
            IERC721(marketItems[_itemId].nftContractAddress).safeTransferFrom(
                marketItems[_itemId].seller,
                msg.sender,
                marketItems[_itemId].tokenId
            );

        emit ItemSold(_itemId);
    }

    function cancelSale(uint256 _itemId) external onlySeller(_itemId) {
        marketItems[_itemId].isCanceled = true;

        emit ItemSaleCenceled(_itemId);
    }

    function claimSoldItemPrice(uint256 _itemId) external onlySeller(_itemId) {
        require(marketItems[_itemId].price != 0);
        uint256 price = marketItems[_itemId].price;
        marketItems[_itemId].price = 0;

        payable(msg.sender).transfer(price);

        emit ItemSalePriceClaimed(_itemId);
    }

    function putOnSale(
        address _nftContractAddress,
        uint256 _tokenId,
        uint256 _price,
        uint64 _startingTimestamp,
        uint64 _endingTimestamp,
        bool _isERC1155
    )
        external
        onlyNftOwner(_nftContractAddress, _tokenId, _isERC1155)
        ifApprovedNft(_nftContractAddress, _tokenId)
    {
        uint256 itemId = ++marketItemIdCounter;
        marketItems[itemId] = MarketItem(
            _nftContractAddress,
            _tokenId,
            _price,
            payable(msg.sender),
            _startingTimestamp,
            _endingTimestamp,
            false,
            false
        );

        emit ItemListed(itemId);
    }

    function updateSaleDuration(
        uint256 _itemId,
        uint64 _newStartingTimestamp,
        uint64 _newEndingTimestamp
    ) external onlySeller(_itemId) {
        marketItems[_itemId].startingTimestamp = _newStartingTimestamp;
        marketItems[_itemId].endingTimestamp = _newEndingTimestamp;

        emit ItemSaleDurationUpdated(_itemId);
    }

    function updateSalePrice(uint256 _itemId, uint256 _newPrice)
        external
        onlySeller(_itemId)
    {
        marketItems[_itemId].price = _newPrice;

        emit ItemSalePriceUpdated(_itemId);
    }
}
