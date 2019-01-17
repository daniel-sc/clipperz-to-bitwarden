# Process Clipperz offline export for Bitwarden

1. Export 'HTML + JSON' from Clipperz
2. (install lxml - e.g. `pip install lxml`)
3. run `python export-clipperz.py CLIPPERZ_EXPORT.html`
4. import generated `import-for-bitwarden.json` in https://vault.bitwarden.com