# Releasing

This project uses tag-triggered GitHub Releases via `.github/workflows/release.yml`.

## Versioning

Tags must follow `vMAJOR.MINOR.PATCH.BUILD` (e.g. `v1.2.0.0`) and must exactly match the `<version>` element in `FS25_UKPrices/modDesc.xml`. The release workflow fails the build if the tag and `modDesc.xml` version don't match.

## Release steps

1. Update `<version>` in `FS25_UKPrices/modDesc.xml`.
2. Commit the version bump:
   ```
   git add FS25_UKPrices/modDesc.xml
   git commit -m "Bump version to X.Y.Z.W"
   git push
   ```
3. Tag the commit and push the tag:
   ```
   git tag vX.Y.Z.W
   git push origin vX.Y.Z.W
   ```
4. Pushing the tag triggers `.github/workflows/release.yml`, which:
   - Validates all XML files are well-formed.
   - Checks the tag version matches `modDesc.xml`.
   - Zips the contents of `FS25_UKPrices/` into `FS25_UKPrices.zip`.
   - Creates a GitHub Release with auto-generated notes and the zip attached.

## Verify the release

Download `FS25_UKPrices.zip` from the new [GitHub Release](../../releases) and load it in Farming Simulator 25 to confirm it works before wider distribution.

## Optional: publishing to ModHub

The mod can also be submitted to Giants Software's [ModHub](https://www.farming-simulator.com/mods) using the same release zip. Submissions are uploaded via the [ModHub upload page](https://modhub.giants-software.com/misc.php?page=misc). ModHub has its own submission requirements (naming, screenshots, icon, description) that are managed entirely on their site — check the current requirements there at upload time, since they are outside this repository's control.
