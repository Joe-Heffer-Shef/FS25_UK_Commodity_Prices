# Contributing

Contributions are welcome — bug fixes, price updates, and improvements to the mod.

## Getting started

1. Fork the repository and clone your fork.
2. Create a branch for your change.
3. Make your changes (see [Development](#development) below).
4. Commit with a clear, descriptive message.
5. Push to your fork and open a pull request against `main`.

## Development

The mod source lives in `FS25_UK_Commodity_Prices/`:

- `modDesc.xml` — mod metadata (title, description, version).
- `scripts/PriceOverride.lua` — commodity price overrides, applied at runtime once the game's economy has finished loading.

To update prices, edit the values in `UKPrices.PRICES_PER_LITER` in `PriceOverride.lua` and re-zip the `FS25_UK_Commodity_Prices` folder as `FS25_UK_Commodity_Prices.zip` for distribution.

## Guidelines

- Keep price changes grounded in a real reference (e.g. AHDB, DEFRA, or another cited UK market source) and note the source in your PR description as a comment next to the price.
- Verify fill type names and `massPerLiter` densities against the base game's `data/maps/maps_fillTypes.xml` before adding a new commodity.
- Test changes in-game before submitting a pull request.
- Keep `modDesc.xml` well-formed XML — the CI build validates this automatically.

## Releasing

Maintainers cutting a new release should follow [RELEASING.md](RELEASING.md).
