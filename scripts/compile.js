import fs from 'fs';
import path from 'path';
import solc from 'solc';

const contractFileName = 'AinumpsaResonanceNFT.sol';
const contractPath = path.resolve('contracts', contractFileName);
const source = fs.readFileSync(contractPath, 'utf8');

// Szukanie importów OpenZeppelin w node_modules
function findImports(importPath) {
  try {
    const fullPath = path.resolve('node_modules', importPath);
    return { contents: fs.readFileSync(fullPath, 'utf8') };
  } catch (e) {
    return { error: 'File not found' };
  }
}

const input = {
  language: 'Solidity',
  sources: {
    [contractFileName]: {
      content: source,
    },
  },
  settings: {
    optimizer: {
      enabled: true,
      runs: 200,
    },
    outputSelection: {
      '*': {
        '*': ['abi', 'evm.bytecode.object'],
      },
    },
  },
};

console.log('Kompilowanie AinumpsaResonanceNFT.sol za pomocą solc-js...');
const output = JSON.parse(solc.compile(JSON.stringify(input), { import: findImports }));

if (output.errors) {
  output.errors.forEach((err) => {
    if (err.severity === 'error') {
      console.error(err.formattedMessage);
    } else {
      console.warn(err.formattedMessage);
    }
  });
}

const contract = output.contracts[contractFileName]['AinumpsaResonanceNFT'];

const artifactDir = path.resolve('artifacts/contracts', `${contractFileName}`);
fs.mkdirSync(artifactDir, { recursive: true });

const artifactPath = path.join(artifactDir, 'AinumpsaResonanceNFT.json');
fs.writeFileSync(
  artifactPath,
  JSON.stringify({ abi: contract.abi, bytecode: contract.evm.bytecode.object }, null, 2)
);

console.log(`\n✅ Kompilacja zakończona sukcesem! Artefakt zapisano w:\n${artifactPath}`);
