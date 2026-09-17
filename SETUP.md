# Profile maintenance

The public profile in `README.md` is generated from `README.template` and
`config.yml`. The workflow in `.github/workflows/update_profile.yml` rebuilds
the profile and contribution animation automatically.

## Update the content

1. Edit personal details, technology labels, or featured projects in
   `config.yml`.
2. Edit the page structure in `README.template`.
3. Replace `assets/photo.jpg` when the portrait changes.
4. Run the build locally:

   ```bash
   python -m pip install -r requirements.txt
   python scripts/build_readme.py
   ```

5. Review both the generated `README.md` and SVG assets before committing.

## Automation

The GitHub Actions workflow runs daily and on pushes to `main` or `master`.
It needs repository **Actions > General > Workflow permissions** set to
**Read and write permissions** so it can update generated files.

Do not edit `README.md` directly: the next workflow run will overwrite it.
