local utils = {};
local home = os.getenv('HOME');
local input_dir = home .. '/inputs.txt';
local cheat_dir = home .. '/cheats.txt';


local function poll_file(filename)
    local file = io.open(filename, 'r');

    if file ~= nil then
        contents = file:read('*a');
        file:close();
    end

    contents = utils.trim_string(contents);
    return utils.split(contents, ' ');
end


local function reset_file(filename)
    for i = 1, 10 do
        local file = io.open(filename, 'w');

        if file ~= nil then
            file:close();
            break;
        else
            os.execute('sleep 1');
        end
    end
end


function utils.split(contents, delimiter)
    if delimiter == nil or contents == nil then
        return;
    end

    split_string = {};

    for match in string.gmatch(contents, '([^' .. delimiter .. ']+)') do
        table.insert(split_string, match);
    end

    return split_string;
end


-- removes trailing whitespace
function utils.trim_string(input)
    if input == nil then
        return nil;
    end

    return tostring(input):gsub('^%s*(.-)%s*$', '%1');
end


-- checks if there's an input from twitch and returns the input, if any
function utils.poll_input()
    return poll_file(input_dir);
end


-- same as poll_input for cheat file
function utils.poll_cheat()
    return poll_file(cheat_dir);
end


-- erases input file contents
function utils.reset_input_file()
    reset_file(input_dir);
end


-- erases cheat file contents
function utils.reset_cheat_file()
    reset_file(cheat_dir);
end


return utils;
