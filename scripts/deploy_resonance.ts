cat << 'EOF' > scripts/deploy_resonance.js
import { createWalletClient, createPublicClient, http, parseAbi } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { sepolia, base, mainnet } from "viem/chains";
import fs from "fs";
import path from "path";

const PRIVATE_KEY = process.env.PRIVATE_KEY;
const RPC_URL = process.env.RPC_URL || "https://rpc.sepolia.org";
const TARGET_CHAIN = sepolia;
const OPERATOR_WALLET = process.env.OPERATOR_WALLET;
const CONTRACT_NAME = "AinumpsaResonanceNFT";

const abi = parseAbi([
  "constructor(address initialOwner)",
  "function mintResonance(address to) external",
  "function getRoomResonance(uint8 x, uint8 y, uint8 z) view returns (string, string, uint8, string)",
  "function ownerOf(uint256 tokenId) view returns (address)",
  "event ResonanceFieldCaptured(uint256 indexed tokenId, string anchorRoom, string resonanceState, uint256 timestamp)"
]);

async function main() {
  if (!PRIVATE_KEY || !OPERATOR_WALLET) {
    throw new Error("Brakujace zmienne środowiskowe: PRIVATE_KEY lub OPERATOR_WALLET");
  }

  const account = privateKeyToAccount(PRIVATE_KEY.startsWith("0x") ? PRIVATE_KEY : `0x${PRIVATE_KEY}`);
  const publicClient = createPublicClient({
    chain: TARGET_CHAIN,
    transport: http(RPC_URL)
  });
  const walletClient = createWalletClient({
    account,
    chain: TARGET_CHAIN,
    transport: http(RPC_URL)
  });

  console.log("────────────────────────────────────────");
  console.log("AINUMPSA Resonance Deployment");
  console.log("Chain        :", TARGET_CHAIN.name);
  console.log("Deployer     :", account.address);
  console.log("Operator     :", OPERATOR_WALLET);
  console.log("Token ID     : 1785312997");
  console.log("Anchor       : ROOM_[1:1:2] → 1>0_LOCKED");
  console.log("────────────────────────────────────────");

  // 1. Wczytanie artefaktu i deployment
  console.log("\n[1/3] Deploying AinumpsaResonanceNFT...");
  const artifactPath = path.resolve(`artifacts/contracts/${CONTRACT_NAME}.sol/${CONTRACT_NAME}.json`);
  
  if (!fs.existsSync(artifactPath)) {
    throw new Error(`Artefakt nie istnieje w ${artifactPath}`);
  }

  const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));

  const hash = await walletClient.deployContract({
    abi: artifact.abi,
    bytecode: `0x${artifact.bytecode.replace(/^0x/, '')}`,
    args: [account.address]
  });

  console.log("Deploy tx:", hash);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  const contractAddress = receipt.contractAddress;
  
  console.log("Contract deployed at:", contractAddress);

  // 2. Minting Resonance Token #1785312997
  console.log("\n[2/3] Minting Resonance #1785312997 to operator...");
  const mintHash = await walletClient.writeContract({
    address: contractAddress,
    abi,
    functionName: "mintResonance",
    args: [OPERATOR_WALLET]
  });
  console.log("Mint tx:", mintHash);
  await publicClient.waitForTransactionReceipt({ hash: mintHash });
  console.log("Mint confirmed.");

  // 3. Weryfikacja stanu
  console.log("\n[3/3] Verifying ROOM_[1:1:2] state...");
  const [nodeType, resonance, neighbors, roomId] = await publicClient.readContract({
    address: contractAddress,
    abi,
    functionName: "getRoomResonance",
    args: [1, 1, 2]
  });

  console.log("Room ID          :", roomId);
  console.log("Node Type        :", nodeType);
  console.log("Resonance        :", resonance);
  console.log("Neighbor Count   :", neighbors.toString());

  console.log("\n────────────────────────────────────────");
  console.log("DEPLOYMENT COMPLETE");
  console.log("Contract         :", contractAddress);
  console.log("Token #1785312997 minted to:", OPERATOR_WALLET);
  console.log("Primary Anchor   : ROOM_[1:1:2] → 1>0_LOCKED");
  console.log("────────────────────────────────────────");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
EOF
