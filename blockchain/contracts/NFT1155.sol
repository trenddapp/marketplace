// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/common/ERC2981.sol";
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract NFT1155 is ERC2981, ERC1155 {
    uint256 private tokenIdCounter = 1818;
    mapping(uint256 => string) private tokenURIs;

    string public name;
    string public symbol;

    constructor(string memory _name, string memory _symbol) ERC1155("") {
        name = _name;
        symbol = _symbol;
    }

    function uri(uint256 _tokenId)
        public
        view
        override
        returns (string memory)
    {
        return tokenURIs[_tokenId];
    }

    /// @param _royalties Any number * 100
    function mint(
        string memory _tokenURI,
        uint256 amount,
        uint96 _royalties,
        bytes memory data
    ) public {
        uint256 _tokenId = ++tokenIdCounter;
        _mint(msg.sender, _tokenId, amount, data);
        tokenURIs[_tokenId] = _tokenURI;
        _setTokenRoyalty(_tokenId, msg.sender, _royalties);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC2981, ERC1155)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
