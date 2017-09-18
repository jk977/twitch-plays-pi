-- Script that provides a plaintext interface to the emulator.

local utils = require('utils');
local emutils = require('emutils');

-- wipes any pre-existing input info
utils.reset_input_file();
utils.reset_cheat_file();

-- main loop
while true do
    local inputs = utils.poll_input();
    local cheat = utils.poll_cheat();

    if inputs ~= nil and #inputs ~= 0 then
        for _, input in pairs(inputs) do
            print('Pressing "' .. input .. '"');
            local count = tonumber(input:sub(1, 1));
            local button = input:sub(2, #input);
            emutils.press_button(1, button, count);
            emutils.advance_frames(10);
        end

        utils.reset_input_file();
    end

    if cheat ~= nil and cheat ~= '' then
        utils.reset_cheat_file();
    end

    emutils.advance_frames(1);
end
