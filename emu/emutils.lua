-- emutils.lua
-- ===========
-- Module with emulator utility functions

local emutils = {};


-- advances emulation by <count> frames
local function advance_frames(count)
    for i = 1, count do
        emu.message(tostring(emu.lagged()));
        emu.frameadvance();
    end
end


-- presses specified button <count> times
function emutils.press_button(player, button, count)
    for i = 1, count do
        -- loops until emu isn't lagged and button is registered  
        while emu.lagged() or not joypad.get(1)[button] do
            joypad.set(player, {[button]=true});
            emu.frameadvance();
        end

        -- makes sure button isn't held through to the next press 
        joypad.set(player, {[button]=false});
        emu.frameadvance();

        -- if there are still button presses to do, advance until no lag
        while emu.lagged() and i < tonumber(count) do
            emu.frameadvance();
        end
    end
end


return emutils;
