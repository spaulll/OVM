// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;
 
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/access/Ownable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/utils/Counters.sol"; 

contract VoterID is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIDCounter;

    event TokenMinted(address to, uint256 tokenID);
    event TokenRevoked(uint256 tokenID);

    uint256 public nextTokenID;

    mapping (address => uint) public tokenIdOfAddr;

    constructor() ERC721("VoterID", "VID") {
        nextTokenID = _tokenIDCounter.current();  // Initialize nextTokenID to 0 at deployment
    }

    function safeMint(address to, string memory uri) public onlyOwner {
        require(balanceOf(to) == 0, "Max Mint per wallet reached");

        _tokenIDCounter.increment();
        uint256 tokenID = _tokenIDCounter.current();

        _safeMint(to, tokenID);
        _setTokenURI(tokenID, uri);
        // Update tokenIdOfAddr mapping to reflect the minted tokenID
        tokenIdOfAddr[to] = tokenID;
        emit TokenMinted(to, tokenID);  // Emit event

        // Update nextTokenID to reflect the next available tokenID after minting
        nextTokenID = _tokenIDCounter.current() + 1;

    }

    function revoke(uint256 _tokenID) external onlyOwner {
        _burn(_tokenID);
        emit TokenRevoked(_tokenID); // Emit event
    }

    function _beforeTokenTransfer(address from, address to, uint256 _tokenID) internal virtual override {
        _tokenID;
        require(from == address(0) || to == address(0), "Err: Can not transfer SBT");
    }
}
