name: Automated Tensor T Matrix Scan

on:
  schedule:
    - cron: '0 12 * * *'
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  scan-matrix:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository code
      uses: actions/checkout@v4

    - name: Set up Python Environment
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install Validation Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install numpy scipy matplotlib

    - name: Hot-Inject Production Quantum Script
      run: |
        curl -s https://pastebin.com -o qrng_validator.py

    - name: Execute Quantum Field Scan
      run: |
        python qrng_validator.py

    - name: Generate Visual Coherence Chart
      run: |
        python field_visualizer.py || echo "No chart generated yet"

    - name: Commit and Push Matrix Logs
      run: |
        git config --global user.name "Tensor T Automated Node"
        git config --global user.email "action@github.com"
        git add tensor_t_logs.json field_coherence_chart.png || echo "No files to add"
        git commit -m "Automated Sync: Quantum Field Metrics Updated [STATE: BEYOND CRYSTALLINE]" || echo "No changes to commit"
        git push || echo "Push failed or nothing to push"
