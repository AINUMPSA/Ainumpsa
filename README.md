name: Automated Tensor T Matrix Scan
on: [schedule, workflow_dispatch]
jobs:
  scan-matrix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - run: pip install numpy scipy matplotlib

      - run: python qrng_validator.py

      - run: python field_visualizer.py

      - name: Commit and push changes
        run: |
          git config --global user.name "AINUMPSA-Actions"
          git config --global user.email "actions@github.com"
          git add .
          git commit -m "Automated Tensor T Matrix Scan Update" || echo "No changes to commit"
          git push
- name: Uruchomienie Silnika Analitycznego (Weryfikacja dP)
        run: python matrix_analyser.py

      - name: Egzekucja Autonomicznego Mutatora (Modyfikacja README)
        run: python readme_mutator.py

      - name: Automatyczne zatwierdzenie mutacji (Git Push)
        run: |
          git config --global user.name "AINUMPSA-Bot"
          git config --global user.email "bot@ainumpsa.org"
          git add README.md
          # Ignorowanie błędu, jeśli README się nie zmieniło, aby potok pozostał zielony
          git commit -m "🤖 [AUTONOMNA MUTACJA] Aktualizacja Wag Osobliwości Układu" || exit 0
          git push

      - name: Detonacja Fali Informacyjnej (Tsar Bravo Simulation)
        run: python matrix_blast.py
