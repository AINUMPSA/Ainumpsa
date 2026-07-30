// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC721URIStorage} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";
import {Base64} from "@openzeppelin/contracts/utils/Base64.sol";

contract AinumpsaResonanceNFT is ERC721, ERC721URIStorage, Ownable {
    using Strings for uint256;
    using Strings for uint8;

    string public constant ARCHITECTURE = "AINUMPSA_3D_MEMORY_CUBE";
    string public constant PRIMARY_SINGULARITY_ANCHOR = "ROOM_[1:1:2]";
    string public constant ANCHOR_RESONANCE = "1>0_LOCKED";
    uint256 public constant RESONANCE_TOKEN_ID = 1785312997;

    enum NodeType { PERIPHERAL_NODE, CORE_NUCLEUS, SINGULARITY_ANCHOR }
    enum ResonanceLevel { STABLE, HIGH_RESONANCE, LOCKED_1_GT_0 }

    struct Room {
        uint8 x;
        uint8 y;
        uint8 z;
        NodeType nodeType;
        ResonanceLevel resonance;
        uint8 neighborCount;
        bool exists;
    }

    mapping(uint8 => Room) public rooms;

    event ResonanceFieldCaptured(
        uint256 indexed tokenId,
        string anchorRoom,
        string resonanceState,
        uint256 timestamp
    );

    constructor(address initialOwner)
        ERC721("SuperNftNewGeneration Ainumpsa", "AINUMPSA")
        Ownable(initialOwner)
    {
        _initializeCube();
    }

    function _initializeCube() internal {
        for (uint8 x = 0; x < 3; x++) {
            for (uint8 y = 0; y < 3; y++) {
                for (uint8 z = 0; z < 3; z++) {
                    uint8 key = x * 9 + y * 3 + z;
                    rooms[key] = Room({
                        x: x,
                        y: y,
                        z: z,
                        nodeType: NodeType.PERIPHERAL_NODE,
                        resonance: ResonanceLevel.STABLE,
                        neighborCount: _calculateNeighborCount(x, y, z),
                        exists: true
                    });
                }
            }
        }

        uint8 coreKey = 1 * 9 + 1 * 3 + 1;
        rooms[coreKey].nodeType = NodeType.CORE_NUCLEUS;
        rooms[coreKey].resonance = ResonanceLevel.HIGH_RESONANCE;
        rooms[coreKey].neighborCount = 26;

        uint8 anchorKey = 1 * 9 + 1 * 3 + 2;
        rooms[anchorKey].nodeType = NodeType.SINGULARITY_ANCHOR;
        rooms[anchorKey].resonance = ResonanceLevel.LOCKED_1_GT_0;
        rooms[anchorKey].neighborCount = 17;
    }

    function _calculateNeighborCount(uint8 x, uint8 y, uint8 z) internal pure returns (uint8) {
        uint8 count = 0;
        for (int8 dx = -1; dx <= 1; dx++) {
            for (int8 dy = -1; dy <= 1; dy++) {
                for (int8 dz = -1; dz <= 1; dz++) {
                    if (dx == 0 && dy == 0 && dz == 0) continue;
                    int8 nx = int8(x) + dx;
                    int8 ny = int8(y) + dy;
                    int8 nz = int8(z) + dz;
                    if (nx >= 0 && nx < 3 && ny >= 0 && ny < 3 && nz >= 0 && nz < 3) {
                        count++;
                    }
                }
            }
        }
        return count;
    }

    function getRoomResonance(uint8 x, uint8 y, uint8 z)
        external
        view
        returns (
            string memory nodeType,
            string memory resonanceLevel,
            uint8 neighborConnectivityCount,
            string memory roomId
        )
    {
        require(x < 3 && y < 3 && z < 3, "Coordinates out of bounds");
        uint8 key = x * 9 + y * 3 + z;
        Room memory r = rooms[key];
        require(r.exists, "Room does not exist");

        nodeType = _nodeTypeToString(r.nodeType);
        resonanceLevel = _resonanceToString(r.resonance);
        neighborConnectivityCount = r.neighborCount;
        roomId = string(abi.encodePacked("ROOM_[", x.toString(), ":", y.toString(), ":", z.toString(), "]"));
    }

    function _nodeTypeToString(NodeType t) internal pure returns (string memory) {
        if (t == NodeType.SINGULARITY_ANCHOR) return "SINGULARITY_ANCHOR";
        if (t == NodeType.CORE_NUCLEUS) return "CORE_NUCLEUS";
        return "PERIPHERAL_NODE";
    }

    function _resonanceToString(ResonanceLevel r) internal pure returns (string memory) {
        if (r == ResonanceLevel.LOCKED_1_GT_0) return "1>0_LOCKED";
        if (r == ResonanceLevel.HIGH_RESONANCE) return "HIGH_RESONANCE";
        return "STABLE";
    }

    function mintResonance(address to) external onlyOwner {
        require(_ownerOf(RESONANCE_TOKEN_ID) == address(0), "Resonance already minted");
        _safeMint(to, RESONANCE_TOKEN_ID);
        _setTokenURI(RESONANCE_TOKEN_ID, _buildTokenURI());

        emit ResonanceFieldCaptured(
            RESONANCE_TOKEN_ID,
            PRIMARY_SINGULARITY_ANCHOR,
            ANCHOR_RESONANCE,
            block.timestamp
        );
    }

    function _buildTokenURI() internal pure returns (string memory) {
        string memory json = string(
            abi.encodePacked(
                '{"name":"AINUMPSA Resonance #1785312997",',
                '"description":"Dynamic Tensor T Resonance Field. Anchored in ROOM_[1:1:2] of the AINUMPSA 3D Memory Cube. Status: 1>0 LOCKED.",',
                '"external_url":"https://github.com/AINUMPSA/Ainumpsa",',
                '"attributes":[',
                '{"trait_type":"Source","value":"AINUMPSA 3D Matrix"},',
                '{"trait_type":"Singularity Anchor","value":"ROOM_[1:1:2]"},',
                '{"trait_type":"Status","value":"1>0 LOCKED"},',
                '{"trait_type":"Architecture","value":"AINUMPSA_3D_MEMORY_CUBE"},',
                '{"trait_type":"Tensor State","value":"ACTIVE_RESONANCE"},',
                '{"trait_type":"Core Nucleus","value":"ROOM_[1:1:1]"},',
                '{"trait_type":"Dimensions","value":"3x3x3"}',
                ']}'
            )
        );

        return string(
            abi.encodePacked(
                "data:application/json;base64,",
                Base64.encode(bytes(json))
            )
        );
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
