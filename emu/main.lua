-- twitch.lua
-- ==========
-- Script that provides an interface to the emulator via file in same directory
-- TODO:
--  * Fix audio alternating on and off (either caused by FCEUX or avconv)
--  * Fix input reading in certain games (namely Final Fantasy 1 battles)
--      * Possibly caused by emulator issues with ALSA? This error occurs in the battles:
--          * Loading SDL sound with alsa driver...
--          * ALSA lib pcm.c:7843:(snd_pcm_recover) underrun occurred

utils = require('utils');
emutils = require('emutils');

press_duration = 20; -- default number of frames to hold for a button press


-- wipes any pre-existing input info
utils.reset_input_file();

-- main loop
while true do
    local input = utils.trim_string(utils.poll_input()); -- input is in format '[1-9]%w+'

    if input ~= nil and utils.validate_input(input) then
        print('Pressing "' .. input .. '"');
        count = input:sub(1, 1);
        button = input:sub(2, #input);

        emutils.press_button(1, button, count);
        utils.reset_input_file();
    else
        emu.frameadvance();
    end
end
