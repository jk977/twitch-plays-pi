-- twitch.lua
-- ==========
-- Script that provides an interface to the emulator via file in same directory
-- TODO fix input reading in lag frames

local press_duration = 20; -- default number of frames to hold for a button press
local button_opts = {'A', 'B', 'start', 'select', 'up', 'down', 'left', 'right'};


-- advances emulation by <count> frames
function advance_frames(count)
    for i = 1, count do
        emu.frameadvance();
    end
end


function lag_wait()
    print('Waiting...');
    count = 0;

    while emu.lagged() do
        count = count + 1;
        emu.frameadvance();
        print('Frames waited: ' .. tostring(count));
        print('Lag frames: ' .. tostring(emu.lagcount()));
    end

    if count > 0 then
        print('Done waiting.');
    end
end


function print_current_inputs(player)
    local inputs = joypad.get(player);
    
    for button, state in pairs(inputs) do
        print(button .. ': ' .. tostring(state));
    end
end


-- removes all button presses
function clear_buttons(player)
    local clear = {};
    for _, value in pairs(button_opts) do
        clear[value] = false;
        print(value);
    end

    joypad.set(player, clear);
end


-- presses specified button <count> times
function press_button(player, button, count)
    print('Button to press: ' .. button);
    for i = 1, count do
        lag_wait();
        print('---');
        print_current_inputs(player);
        print('---');
        joypad.set(player, {[button]=true});
        print_current_inputs(player);
        print('---');
        advance_frames(press_duration);
        joypad.set(player, {[button]=false});
        print_current_inputs(player);
        print('---');
    end
end


-- removes trailing whitespace
function trim_string(input)
    if input == nil then
        return nil;
    end

    return input:gsub('^%s*(.-)%s*$', '%1');
end


-- checks if there's an input from twitch and returns the input, if any
-- inputs.txt contents in format "[1-9]%w+" (letters matching a button)
function poll_input()
    local contents = nil;
    local file = io.open('./inputs.txt', 'r');

    if file ~= nil then
        io.input(file);
        contents = io.read('*a');
        io.close();
    end

    return contents;
end


-- verifies that the input button is valid
function validate_input(input)
    button = input:sub(2, #input)

    for _, value in pairs(button_opts) do
        if button == value then
            return true;
        end
    end

    return false;
end


-- erases input file contents
function reset_input_file()
    for i = 0, 10 do
        local file = io.open('./inputs.txt', 'w');
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


-- wipes any pre-existing input info
reset_input_file();

-- main loop
while true do
    local input = trim_string(poll_input()); -- input is in format '[1-9]%w+'

    if input ~= nil and validate_input(input) then
        print('Pressing "' .. input .. '"');
        count = input:sub(1, 1);
        button = input:sub(2, #input);

        press_button(1, button, count);
        reset_input_file();
    else
        emu.frameadvance();
    end
end
