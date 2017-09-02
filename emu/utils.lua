-- utils.lua
-- =========
-- Module with general utility functions

local utils = {};
local input_dir = '../inputs.txt';
local cheat_dir = '../cheats.txt';


-- removes trailing whitespace
function utils.trim_string(input)
    if input == nil then
        return nil;
    end

    return tostring(input):gsub('^%s*(.-)%s*$', '%1');
end


-- checks if there's an input from twitch and returns the input, if any
-- inputs.txt contents in format "[1-9]%w+" (letters matching a button)
function utils.poll_input()
    local file = io.open(input_dir, 'r');

    if file ~= nil then
        io.input(file);
        contents = io.read('*a');
        io.close();
    end

    return utils.trim_string(contents);
end


-- same as poll_input for cheat file
-- TODO refactor with less redundancy
function utils.poll_cheat()
    local file = io.open(cheat_dir, 'r');

    if file ~= nil then
        io.input(file);
        contents = io.read('*a');
        io.close();
    end

    return utils.trim_string(contents);
end


-- erases input file contents
function utils.reset_input_file()
    for i = 1, 10 do
        local file = io.open(input_dir, 'w');

        if file then
            io.input(file);
            io.close();
            break;
        else
            print('Failed to overwrite input file. Sleeping for 1 second.');
            os.execute('sleep 1');
        end
    end
end


-- erases cheat file contents
-- TODO refactor with less redundancy
function utils.reset_cheat_file()
    for i = 1, 10 do
        local file = io.open(cheat_dir, 'w');

        if file then
            io.input(file);
            io.close();
            break;
        else
            print('Failed to overwrite cheat file. Sleeping for 1 second.');
            os.execute('sleep 1');
        end
    end
end


return utils;
