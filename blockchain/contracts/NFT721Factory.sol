// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./NFT721.sol";

contract NFT721Factory {
    event CollectionCreated(
        string name,
        string symbol,
        address contractAddress
    );

    function createCollection(string memory _name, string memory _symbol)
        external
    {
        NFT721 collection = new NFT721(_name, _symbol);

        emit CollectionCreated(_name, _symbol, address(collection));
    }
}
