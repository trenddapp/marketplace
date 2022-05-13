// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract ERC721Marketplace is ERC721 {
    uint256 private tokenIdCounter = 1818;
    mapping(uint256 => string) private tokenURIs;

    constructor(string memory _name, string memory _symbol)
        ERC721(_name, _symbol)
    {}

    function mint(string memory _tokenURI) external {
        uint256 _tokenId = ++tokenIdCounter;
        _safeMint(msg.sender, _tokenId);
        tokenURIs[_tokenId] = _tokenURI;
    }

    function tokenURI(uint256 _tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(
            _exists(_tokenId),
            "ERC721Metadata: URI query for nonexistent token"
        );

        return tokenURIs[_tokenId];
    }
}
