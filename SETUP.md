# Profile maintenance

The public profile in `README.md` is generated from `README.template` and
`config.yml`. Profile updates are built locally and committed manually.

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

## Manual updates only

The automatic profile-update workflow has been removed. There are no scheduled
builds or GitHub Actions bot commits. The local build script only writes files;
it does not commit or push them.

Edit `README.template` and `config.yml` for lasting changes: running the local
build will overwrite `README.md`. The neofetch panel, typing header, and wave
divider are regenerated from `config.yml` on every build. Featured projects can
take an optional `demo` URL, shown under the project name.
