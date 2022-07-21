// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./NFT1155.sol";

contract NFT1155Factory {
    event CollectionCreated(
        string name,
        string symbol,
        address contractAddress
    );

    function createCollection(string calldata _name, string calldata _symbol)
        external
    {
        NFT1155 collection = new NFT1155(_name, _symbol);

        emit CollectionCreated(_name, _symbol, address(collection));
    }
}
