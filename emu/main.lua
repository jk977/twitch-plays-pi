-- main.lua
-- ==========
-- Script that provides a plaintext interface to the emulator.
-- TODO:
--  * Fix audio alternating on and off (either caused by FCEUX or avconv)
--          * Loading SDL sound with alsa driver...
--          * ALSA lib pcm.c:7843:(snd_pcm_recover) underrun occurred

local utils = require('utils');
local emutils = require('emutils');
local game = require('games/finalfantasy/ff');

-- wipes any pre-existing input info
utils.reset_input_file();
utils.reset_cheat_file();

-- main loop
while true do
    local inputs = utils.poll_input(); -- input is in format '[1-9]%w+'
    local cheat = utils.poll_cheat(); -- input is in format '[1-9]%w+'

    if inputs ~= nil and #inputs ~= 0 then
        for _, input in pairs(inputs) do
            print('Pressing "' .. input .. '"');
            local count = tonumber(input:sub(1, 1));
            local button = input:sub(2, #input);
            emutils.press_button(1, button, count);
        end

        utils.reset_input_file();
    end

    if cheat ~= nil and cheat ~= '' then
        game.do_cheat(cheat);
        utils.reset_cheat_file();
    end

    emu.frameadvance();
end
