describe("UKPrices", function()
    local fillTypes

    setup(function()
        -- Stub FS25 globals referenced by PriceOverride.lua at load/apply time.
        Mission00 = {}

        Utils = {
            appendedFunction = function(base, appended)
                if base == nil then
                    return appended
                end
                return function(...)
                    base(...)
                    return appended(...)
                end
            end,
        }

        Logging = {
            warning = function(...) end,
        }

        fillTypes = {
            WHEAT = { pricePerLiter = 0, startPricePerLiter = 0 },
            BARLEY = { pricePerLiter = 0, startPricePerLiter = 0 },
            CANOLA = { pricePerLiter = 0, startPricePerLiter = 0 },
            POTATO = { pricePerLiter = 0, startPricePerLiter = 0 },
            SUGARBEET = { pricePerLiter = 0, startPricePerLiter = 0 },
            OAT = { pricePerLiter = 0, startPricePerLiter = 0 },
            MAIZE = { pricePerLiter = 0, startPricePerLiter = 0 },
            SUNFLOWER = { pricePerLiter = 0, startPricePerLiter = 0 },
            SOYBEAN = { pricePerLiter = 0, startPricePerLiter = 0 },
            MILK = { pricePerLiter = 0, startPricePerLiter = 0 },
            STRAW = { pricePerLiter = 0, startPricePerLiter = 0 },
            GRASS_WINDROW = { pricePerLiter = 0, startPricePerLiter = 0 },
            DRYGRASS_WINDROW = { pricePerLiter = 0, startPricePerLiter = 0 },
            SILAGE = { pricePerLiter = 0, startPricePerLiter = 0 },
            -- WOOL intentionally omitted to exercise the "missing fillType" branch.
        }

        g_fillTypeManager = {
            getFillTypeByName = function(_, name)
                return fillTypes[name]
            end,
        }

        require("PriceOverride")
    end)

    it("defines only positive numeric prices", function()
        for name, price in pairs(UKPrices.PRICES_PER_LITER) do
            assert.is_number(price)
            assert.is_true(price > 0, "price for " .. name .. " should be > 0")
        end
    end)

    it("uses upper-case, space-free fillType-style keys", function()
        for name in pairs(UKPrices.PRICES_PER_LITER) do
            assert.matches("^[A-Z0-9_]+$", name)
        end
    end)

    it("sets pricePerLiter and startPricePerLiter on a known fillType", function()
        UKPrices.apply()

        assert.are.equal(UKPrices.PRICES_PER_LITER.WHEAT, fillTypes.WHEAT.pricePerLiter)
        assert.are.equal(UKPrices.PRICES_PER_LITER.WHEAT, fillTypes.WHEAT.startPricePerLiter)
    end)

    it("logs a warning for a fillType missing from the manager", function()
        spy.on(Logging, "warning")

        UKPrices.apply()

        assert.spy(Logging.warning).was_called()
        assert.spy(Logging.warning).was_called_with("UKPrices: could not override price for fillType '%s'", "WOOL")
    end)

    it("does not error when applied against the stub fillType manager", function()
        assert.has_no.errors(function()
            UKPrices.apply()
        end)
    end)
end)
