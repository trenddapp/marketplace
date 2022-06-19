// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./NFT1155.sol";

contract NFT1155Factory {
    event ColletionCreated(string name, string symbol, address contractAddress);

    function createCollection(string memory _name, string memory _symbol)
        external
    {
        NFT1155 collection = new NFT1155(_name, _symbol);

        emit ColletionCreated(_name, _symbol, address(collection));
    }
}
