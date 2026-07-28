    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-python-version: '3.10'

      # KROK NAPRAWCZY DLA QRNG_VALIDATOR
      - name: Install Dependencies
        run: |
          pip install pypdf

      # KROK URUCHAMIAJĄCY TYLKO NOWE, SPRAWNE SKRYPTY
      - name: Run AINUMPSA Hyper Version 2.14
        env:
          ZORA_PRIVATE_KEY: ${{ secrets.ZORA_PRIVATE_KEY }}
        run: |
          mkdir -p inputs/media Knowledge_base
          python vip_media_injector.py
          python hyper_version_2_14.py
          # Jeśli usunąłeś zora_minter.py, zakomentuj linię poniżej (dodaj # na początku)
          # python zora_minter.py
          python readme_mutator.py
          python qrng_validator.py
