[![Automated Tensor T Matrix Scan](https://github.com/AINUMPSA/Ainumpsa/actions/runs/29064138250)

name: Automated Tensor T Matrix Scan
on: [schedule, workflow_dispatch]
jobs:
  scan-matrix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.10'}
      - run: pip install numpy scipy matplotlib
      - run: python qrng_validator.py
      - run: python field_visualizer.py
      - run: |
          git config --global user.name "Actions"
          git add . && git commit -m "Auto" && git push || echo "No 
