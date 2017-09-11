-- Script that provides a plaintext interface to the emulator.

local utils = require('utils');
local emutils = require('emutils');
local ff = require('games/finalfantasy/ff');

-- wipes any pre-existing input info
utils.reset_input_file();
utils.reset_cheat_file();

-- initializes value in ../ff/gil.txt and keeps value updated
ff.write_gil();
ff.register_gil_tracker();

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
        end

        utils.reset_input_file();
    end

    if cheat ~= nil and cheat ~= '' then
        ff.do_cheat(cheat);
        utils.reset_cheat_file();
    end

    emutils.advance_frames(1);
end
