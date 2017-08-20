-- utils.lua
-- =========
-- Module with general utility functions

local utils = {};
local button_opts = {'A', 'B', 'start', 'select', 'up', 'down', 'left', 'right'};
local file_dir = '../inputs.txt';


-- removes trailing whitespace
function utils.trim_string(input)
    if input == nil then
        return nil;
    end

    return input:gsub('^%s*(.-)%s*$', '%1');
end


-- checks if there's an input from twitch and returns the input, if any
-- inputs.txt contents in format "[1-9]%w+" (letters matching a button)
function utils.poll_input()
    local contents = nil;
    local file = io.open(file_dir, 'r');

    if file ~= nil then
        io.input(file);
        contents = io.read('*a');
        io.close();
    end

    return utils.trim_string(contents);
end


-- verifies that the input button is valid
function utils.validate_input(input)
    button = input:sub(2, #input);

    for _, value in pairs(button_opts) do
        if button == value then
            return true;
        end
    end

    return false;
end


-- erases input file contents
function utils.reset_input_file()
    for i = 0, 10 do
        local file = io.open(file_dir, 'w');
        print('Opening file for writing: ' .. os.time());

        if file then
            io.input(file);
            io.close();
            print('Closing file for writing: ' .. os.time());
            break;
        else
            print('File open failed. Sleeping for 1 second.');
            os.execute('sleep 1');
        end
    end
end


return utils;
