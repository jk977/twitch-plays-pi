local chat_gui = {};

local screen_x1 = 2;
local screen_y1 = 8;
local screen_x2 = 256;
local screen_y2 = 231;

local vote_file = '../game/votes.txt';


local function map(func, tab)
    local new_table = {};

    for k, v in pairs(tab) do
        new_k, new_v = func(k, v);
        new_table[new_k] = new_v;
    end
            
    return new_table;
end


local function get_commands()
    local file = io.open(vote_file, 'r');
    commands = {};

    if file == nil then
        return;
    end

    for line in file:lines() do
        if line ~= '' and line ~= nil then
            table.insert(commands, line);
        end
    end
                
    file:close();
    return commands;
end


-- writes lines aligned with the bottom border
function chat_gui.write_lines(x_offset, bg_color, list)
    if list == nil or #list == 0 then
        return;
    end

    list = map(
        function(k,v)
            local number = v:gmatch(': (%d+)')();
            local choice = v:gmatch('(.+: )')();
            if #choice > 20 then v = v:sub(1,17)..'...: '..number end
            return k,v
        end,
        list
    );

    -- finds the max line length in list
    local max_length = math.max(unpack(map(function(k,v) return k, #v end, list))) * 6;

    -- dimensions of box
    local default_height = 36;
    local height = math.max(default_height, #list * 9);

    local default_width = screen_x2 / 2.5 + x_offset;
    local width = math.max(default_width, max_length);

    -- initial text coordinates
    local x = screen_x1 + x_offset;
    local y = screen_y2 - height;

    -- box upper left vertex
    local box_x1 = x - 2;
    local box_y1 = y - 3;

    gui.opacity(0.65)
    gui.box(box_x1, box_y1, width, screen_y2, bg_color, 'white');

    gui.text(x, y, 'Top Votes', nil, 'clear')
    y = y + 9;

    for _, line in pairs(list) do
        gui.text(x, y, line, nil, 'clear');
        y = y + 9;
    end
                
    gui.opacity(1);
end


function chat_gui.update()
    commands = get_commands();
    chat_gui.write_lines(0, 'black', commands);
end


return chat_gui;
