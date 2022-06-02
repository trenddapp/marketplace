// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";

contract NFT721 is ERC721Royalty {
    uint256 private tokenIdCounter = 1818;
    mapping(uint256 => string) private tokenURIs;

    constructor(string memory _name, string memory _symbol)
        ERC721(_name, _symbol)
    {}

    /// @param _royalties Any number * 100
    function mint(string memory _tokenURI, uint96 _royalties) external {
        uint256 _tokenId = ++tokenIdCounter;
        _safeMint(msg.sender, _tokenId);
        tokenURIs[_tokenId] = _tokenURI;
        _setTokenRoyalty(_tokenId, msg.sender, _royalties);
    }

    function tokenURI(uint256 _tokenId)
        public
        view
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
