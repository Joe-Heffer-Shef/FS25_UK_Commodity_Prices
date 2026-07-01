# FS25 UK Commodity Prices

[![Build](https://github.com/Joe-Heffer-Shef/FS25_UK_Commodity_Prices/actions/workflows/build.yml/badge.svg)](https://github.com/Joe-Heffer-Shef/FS25_UK_Commodity_Prices/actions/workflows/build.yml)

A [Farming Simulator 25](https://www.farming-simulator.com/) mod that adjusts in-game crop sell prices to approximate real UK agricultural commodity market values. Built for the Moss Valley FS25 workshop project.

## What it does

The mod overrides the base game's `pricePerLitre` economy values for key arable commodities so that in-game prices track approximate UK market rates:

| Commodity | Fill Type | Approx. UK Price |
|---|---|---|
| Feed wheat | `WHEAT` | ~£175/t |
| Feed barley | `BARLEY` | ~£165/t |
| Oilseed rape (canola) | `CANOLA` | ~£380/t |
| Ware potatoes | `POTATO` | ~£175/t |
| Sugar beet | `SUGARBEET` | AHDB contract reference price |
| Milling oats | `OAT` | ~£220/t |
| Feed maize | `MAIZE` | ~£180/t |
| Sunflower seed | `SUNFLOWER` | ~£375/t (EU/import reference; not widely grown in the UK) |
| Soybean | `SOYBEAN` | ~£400/t (EU/import reference; minimal UK production) |
| Milk | `MILK` | ~40 ppl (UK farmgate average; highly volatile) |
| Straw | `STRAW` | ~£100/t (GB big bale reference) |
| Grass silage | `GRASS_WINDROW` | ~£32/t (on-farm feed value) |
| Hay | `DRYGRASS_WINDROW` | ~£120/t |
| Silage | `SILAGE` | ~£32/t (on-farm feed value) |
| Wool | `WOOL` | ~75p/kg (2025 UK clip average) |

Prices are defined in `FS25_UKPrices/data/fillTypes/fillTypes.xml`. Fill type names and `massPerLiter` densities used for the `pricePerLitre` conversions were verified against the base game's `data/maps/maps_fillTypes.xml`.

## Installation

1. Download `FS25_UKPrices.zip` from the [Releases page](../../releases) (or zip the `FS25_UKPrices` folder yourself for a local dev build).
2. Copy the zip file into your Farming Simulator 25 `mods` folder, e.g.:
   - Windows: `Documents\My Games\FarmingSimulator2025\mods`
3. Launch Farming Simulator 25 and enable **UK Commodity Prices** in the mod selection screen when starting or loading a savegame.

## Development

The mod source lives in `FS25_UKPrices/`:

- `modDesc.xml` — mod metadata (title, description, version).
- `data/fillTypes/fillTypes.xml` — commodity price overrides.

To update prices, edit `pricePerLitre` in `fillTypes.xml` and re-zip the `FS25_UKPrices` folder as `FS25_UKPrices.zip` for distribution.

## Licence

Released under the [MIT Licence](LICENSE).
