      - name: Run Hyper Version 2.14 Engine & VIP Media Injector
        run: |
          mkdir -p inputs/media Knowledge_base
          python vip_media_injector.py
          python hyper_version_2_14.py
