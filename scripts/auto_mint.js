import { createWalletClient, createPublicClient, http, parseAbi } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";
import fs from "fs";
import path from "path";

const PRIVATE_KEY = process.env.PRIVATE_KEY;
const RPC_URL = process.env.RPC_URL || "https://mainnet.base.org";
const OPERATOR_WALLET = process.env.OPERATOR_WALLET;
const CONTRACT_ADDRESS = "0x8606add4c3adcdf4c07bc2d18780b1c0f20567fd";

const abi = parseAbi([
  "function mintResonance(address to) external"
]);

async function main() {
  if (!PRIVATE_KEY || !OPERATOR_WALLET) {
    throw new Error("Brak PRIVATE_KEY lub OPERATOR_WALLET");
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

  console.log(`[AutoMint] Uruchamianie mintowania na adres: ${OPERATOR_WALLET}`);

  const hash = await walletClient.writeContract({
    address: CONTRACT_ADDRESS,
    abi,
    functionName: "mintResonance",
    args: [OPERATOR_WALLET]
  });

  console.log("Tx Hash:", hash);
  await publicClient.waitForTransactionReceipt({ hash });
  console.log("✅ Sukces! Token został wyemitowany automatycznie.");
}

main().catch((err) => {
  console.error("❌ Błąd automatycznego mintu:", err);
  process.exit(1);
});
