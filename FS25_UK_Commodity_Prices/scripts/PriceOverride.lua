-- Overrides base-game fillType sell prices with UK market approximations.
-- XML-only fillType overrides are not applied by the game for non-map mods,
-- so prices must be set at runtime once the economy has finished loading.

UKPrices = {}

UKPrices.PRICES_PER_LITER = {
    WHEAT = 0.130,             -- Feed wheat ~£175/t
    BARLEY = 0.123,            -- Feed barley ~£165/t
    CANOLA = 0.355,            -- Oilseed rape (canola) ~£380/t
    POTATO = 0.164,            -- Ware potatoes ~£175/t
    SUGARBEET = 0.042,         -- Sugar beet, AHDB contract reference price
    OAT = 0.110,               -- Milling oats ~£220/t (density 0.50 kg/L)
    MAIZE = 0.144,             -- Feed maize ~£180/t (density 0.80 kg/L)
    SUNFLOWER = 0.131,         -- Sunflower seed ~£375/t, EU/import reference (density 0.35 kg/L)
    SOYBEAN = 0.280,           -- Soybean ~£400/t, EU/import reference (density 0.70 kg/L)
    MILK = 0.400,              -- UK farmgate milk price ~40 ppl (density 1.03 kg/L)
    STRAW = 0.006,             -- Wheat/barley straw, GB big bale ~£100/t (density 0.06 kg/L)
    GRASS_WINDROW = 0.010,     -- Grass silage feed value, on-farm nominal ~£32/t (density 0.30 kg/L)
    DRYGRASS_WINDROW = 0.008,  -- Baled hay ~£120/t (density 0.07 kg/L)
    SILAGE = 0.014,            -- Maize/grass silage, on-farm nominal ~£32/t (density 0.45 kg/L)
    WOOL = 0.570,              -- UK wool, 2025 clip average ~75p/kg clean (density 0.76 kg/L)
}

function UKPrices.apply()
    local fillTypeManager = g_fillTypeManager

    for fillTypeName, pricePerLiter in pairs(UKPrices.PRICES_PER_LITER) do
        local fillType = fillTypeManager:getFillTypeByName(fillTypeName)

        if fillType ~= nil then
            fillType.pricePerLiter = pricePerLiter
            fillType.startPricePerLiter = pricePerLiter
        else
            Logging.warning("UKPrices: could not override price for fillType '%s'", fillTypeName)
        end
    end
end

Mission00.loadMission00Finished = Utils.appendedFunction(Mission00.loadMission00Finished, UKPrices.apply)
