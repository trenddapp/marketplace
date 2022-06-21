// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract Nft721 is ERC721 {
    constructor() ERC721("TrendDapp", "TD") {
        _mint(msg.sender, 18);
    }
}

contract Nft1155 is ERC1155 {
    constructor() ERC1155("URI") {
        _mint(msg.sender, 18, 1, "");
    }
}
