-- emutils.lua
-- ===========
-- Module with emulator utility functions

local emutils = {};


-- advances emulation by <count> frames
local function advance_frames(count)
    for i = 1, count do
        emu.frameadvance();
    end
end


-- presses specified button <count> times
function emutils.press_button(player, button, count)
    print('Button to press: ' .. button);
    for i = 1, count do
        joypad.set(player, {[button]=true});
        advance_frames(press_duration);
        joypad.set(player, {[button]=false});
    end
end


return emutils;
