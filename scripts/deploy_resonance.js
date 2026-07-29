import { createWalletClient, createPublicClient, http, parseAbi } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";
import fs from "fs";
import path from "path";

const PRIVATE_KEY = process.env.PRIVATE_KEY;
const RPC_URL = process.env.RPC_URL || "https://mainnet.base.org";
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
    throw new Error("Brakujące zmienne środowiskowe: PRIVATE_KEY lub OPERATOR_WALLET");
  }

  const account = privateKeyToAccount(PRIVATE_KEY.startsWith("0x") ? PRIVATE_KEY : `0x${PRIVATE_KEY}`);
  
  const publicClient = createPublicClient({
    chain: base,
    transport: http(RPC_URL)
  });
  
  const walletClient = createWalletClient({
    account,
    chain: base,
    transport: http(RPC_URL)
  });

  console.log("────────────────────────────────────────");
  console.log("AINUMPSA Resonance Deployment");
  console.log("Chain        :", base.name);
  console.log("Deployer     :", account.address);
  console.log("Operator     :", OPERATOR_WALLET);
  console.log("────────────────────────────────────────");

  const balance = await publicClient.getBalance({ address: account.address });
  console.log(`\nAktualne saldo konta: ${balance.toString()} wei`);

  if (balance === 0n) {
    console.error("❌ BŁĄD: Konto zwraca saldo 0 ETH na sieci Base!");
    process.exit(1);
  }

  console.log("\n[1/3] Deploying AinumpsaResonanceNFT...");
  const artifactPath = path.resolve(`artifacts/contracts/${CONTRACT_NAME}.sol/${CONTRACT_NAME}.json`);
  const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));

  const hash = await walletClient.deployContract({
    abi: artifact.abi,
    bytecode: `0x${artifact.bytecode.replace(/^0x/, '')}`,
    args: [account.address]
  });

  console.log("Deploy tx hash:", hash);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  const contractAddress = receipt.contractAddress;
  console.log("✅ Contract deployed at:", contractAddress);

  console.log("\n[2/3] Minting Resonance #1785312997...");
  const mintHash = await walletClient.writeContract({
    address: contractAddress,
    abi,
    functionName: "mintResonance",
    args: [OPERATOR_WALLET]
  });
  console.log("Mint tx hash:", mintHash);
  await publicClient.waitForTransactionReceipt({ hash: mintHash });
  console.log("✅ Mint confirmed.");

  console.log("\n────────────────────────────────────────");
  console.log("DEPLOYMENT COMPLETE");
  console.log("Contract Address :", contractAddress);
  console.log("────────────────────────────────────────");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
