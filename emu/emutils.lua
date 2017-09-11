local emutils = {};

local chat_gui = require('chat_gui');


-- advances emulation by <count> frames
function emutils.advance_frames(count)
    for i = 1, count do
        chat_gui.update();
        emu.frameadvance();
    end
end


-- presses specified button <count> times
function emutils.press_button(player, button, count)
    for i = 1, count do
        -- loops until emu isn't lagged and button is registered  
        while emu.lagged() or not joypad.get(player)[button] do
            joypad.set(player, {[button]=true});
            emutils.advance_frames(1);
        end

        -- makes sure button isn't held through to the next press 
        joypad.set(player, {[button]=false});
        emutils.advance_frames(1);

        -- if there are still button presses to do, advance until no lag
        while emu.lagged() and i < count do
            emutils.advance_frames(1);
        end
    end
end


return emutils;
