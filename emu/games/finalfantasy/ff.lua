-- ff.lua
-- ======
-- Contains scripts specific to Final Fantasy 1.

local consts = require('games.finalfantasy.ff_const');
local emutils = require('emutils');
local ff = {};

local gil_file = '../game/gil.txt';


-- returns value (an int) as a big-endian table of bytes
local function split_to_bytes(value, byte_count)
    str_len = 2*byte_count;
    hex_full = string.format('%0' .. tostring(str_len) .. 'x', value);
    hex_bytes = {};

    -- iterate over bytes in hex_full
    for i = 1, str_len, 2 do
        byte = tonumber(hex_full:sub(i, i+1), 16);
        table.insert(hex_bytes, byte);
    end

    return unpack(hex_bytes);
end


local function correct_stat_value(stat, value)
    value = tonumber(value);
    stat = stat:lower();

    if value < 0 then
        return;
    elseif stat == 'str' or stat == 'agl' or stat == 'int' or stat == 'vit' or stat == 'luck' then
        return value % 0x64;
    elseif stat == 'level' then
        return value % 0x63;
    elseif stat == 'xp' or stat == 'xp_next' then
        return value % 0x10000;
    elseif stat == 'hp' or stat == 'max_hp' then
        return value % 0x3E8;
    elseif stat == 'damage' or stat == 'hit' or stat == 'absorb' or stat == 'evade' then
        return value % 0x100;
    elseif stat == 'weapon_1' or stat == 'weapon_2' or stat == 'weapon_3' or stat == 'weapon_4' then
        return value % 0x29;
    elseif stat == 'armor_1' or stat == 'armor_2' or stat == 'armor_3' or stat == 'armor_4' then
        return value % 0xA2;
    else
        return;
    end
end


-- for future use; currently doesn't allow name-changing or status manipulation
local function change_member_stat(member, stat, value)
    member = tonumber(member);
    stat = tostring(stat):lower();
    value = correct_stat_value(stat, value);

    if value == nil or member < 1 or member > 4 then
        return;
    end

    local p_member = consts.PARTY_MEMBERS[member];

    if stat == 'hp' or stat == 'max_hp' or stat == 'xp' or stat == 'xp_next' then
        value = string.format('%04x', value);
        local offsets = consts.MEMBER_INFO[stat:upper()];
        local low = value:sub(3,4);
        local high = value:sub(1,2);

        memory.writebyte(p_member + offsets[1], low);
        memory.writebyte(p_member + offsets[2], high);
    else
        local offset = consts.MEMBER_INFO[stat:upper()];
        local p_stat = p_member + offset;

        memory.writebyte(p_stat, value);
    end
end


-- returns true if player is fighting enemies
local function in_battle()
    return memory.readbyte(0x0081) == 0x68;
end


local function get_attacking_member()
    return memory.readbyte(consts.ATTACKING_MEMBER);
end


-- returns player gil
local function get_gil()
    local p_gil_lo, p_gil_md, p_gil_hi = unpack(consts.GIL);

    local gil_lo = string.format('%02x', memory.readbyte(p_gil_lo));
    local gil_md = string.format('%02x', memory.readbyte(p_gil_md));
    local gil_hi = string.format('%02x', memory.readbyte(p_gil_hi));

    return tonumber(gil_hi .. gil_md .. gil_lo, 16);
end


function ff.do_cheat(cheat)
    if cheat == 'heal' then
        ff.cure_all(true);
    elseif cheat == 'killall' then
        ff.kill_all_enemies(true);
    elseif cheat == 'attack' then
        ff.attack();
    elseif cheat == 'run' then
        ff.run();
    end
end


-- writes amount of gil to gil_file
function ff.write_gil()
    local file = io.open(gil_file, 'w');

    if file ~= nil then
        local gil = tostring(get_gil());
        file:write(gil);
        file:close();
    end
end


-- updates gil.txt whenever gil amount changes
function ff.register_gil_tracker()
    memory.register(consts.GIL[1], 3, ff.write_gil);
end


-- used for chat cheats
function ff.spend_gil(amount)
    local p_gil_lo, p_gil_md, p_gil_hi = unpack(consts.GIL);
    local current = get_gil();

    if current >= amount then
        local balance = current - amount;
        local balance16 = string.format('%06x', balance);
        
        -- TODO fix split_to_bytes so it works here
        local balance_hi = tonumber(balance16:sub(1,2), 16);
        local balance_md = tonumber(balance16:sub(3,4), 16);
        local balance_lo = tonumber(balance16:sub(5,6), 16);

        memory.writebyte(p_gil_lo, balance_lo);
        memory.writebyte(p_gil_md, balance_md);
        memory.writebyte(p_gil_hi, balance_hi);

        emu.message(tostring(amount) .. 'g spent!');
        ff.write_gil();
        return true;
    else
        return false;
    end
end


-- spreads party attacks over all enemies
function ff.attack()
    if not in_battle() then
        emu.message('Not in battle!');
        return;
    end

    local living_members = 4;
    local last_member;
    
    -- ignore dead members
    for i = 1, 4 do
        local p_member = consts.PARTY_MEMBERS[i];
        local p_status = p_member + consts.MEMBER_INFO['STATUS'];
        if memory.readbyte(p_status) == 0x1 then
            living_members = living_members - 1;
        end
    end

    -- set cursor to first party member
    repeat
        last_member = get_attacking_member();
        emutils.press_button(1, 'B', 1);
        emutils.advance_frames(40);
    until last_member == get_attacking_member();

    -- distributes attacks evenly between enemies
    for i = 1, living_members do
        -- fixes edge case where command is entered at end of battle
        if not in_battle() then
            return;
        end

        -- moves cursor to enemy and attacks, compensating for battle animations
        emutils.advance_frames(19);
        emutils.press_button(1, 'A', 1);
        emutils.press_button(1, 'down', i-1);
        emutils.advance_frames(2);
        emutils.press_button(1, 'A', 1);
        emutils.advance_frames(19);
    end
end


-- selects run in battle with each person
function ff.run()
    if not in_battle() then
        emu.message('Not in battle!');
        return;
    end

    local living_members = 4;
    local last_member;

     -- set cursor to first party member
    repeat
        last_member = get_attacking_member();
        emutils.press_button(1, 'B', 1);
        emutils.advance_frames(40);
    until last_member == get_attacking_member();


    -- ignore dead members
    for i = 1, 4 do
        local p_member = consts.PARTY_MEMBERS[i];
        local p_status = p_member + consts.MEMBER_INFO['STATUS'];
        if memory.readbyte(p_status) == 0x1 then
            living_members = living_members - 1;
        end
    end

    for i = 1, living_members do
        -- presses run for each party member
        emutils.press_button(1, 'right', 1);
        emutils.press_button(1, 'A', 1);
    end
end


-- makes next hit a critical hit
function ff.do_crit(require_gil)
    if not in_battle() then
        emu.message('Not in battle!');
        return;
    end

    if not require_gil or ff.spend_gil(100) then
        memory.writebyte(consts.CRIT, 0x1);
    else
        emu.message('Not enough gil!');
    end
end


-- cures all party members, including dead ones
function ff.cure_all(require_gil)
    if not require_gil or ff.spend_gil(100) then
        for i = 1, 4 do
            -- HP-related stats
            local p_member = consts.PARTY_MEMBERS[i];
            local p_hp = consts.MEMBER_INFO['HP'];
            local p_max_hp = consts.MEMBER_INFO['MAX_HP'];

            local hp_lo = memory.readbyte(p_member + p_max_hp[1]);
            local hp_hi = memory.readbyte(p_member + p_max_hp[2]);

            memory.writebyte(p_member + consts.MEMBER_INFO['STATUS'], 0);
            memory.writebyte(p_member + p_hp[1], hp_lo);
            memory.writebyte(p_member + p_hp[2], hp_hi);

            -- MP-related stats
            local p_magic = consts.MEMBER_MAGIC[i];
            local p_mp = consts.MP_CURRENT;
            local p_mp_max = consts.MP_MAX;

            for lv = 1, 8 do
                local max = memory.readbyte(p_magic + p_mp_max[lv]);
                memory.writebyte(p_magic + p_mp[lv], max);
            end
        end
    else
        emu.message('Not enough gil!');
    end
end


-- kills all enemies if in a battle
-- TODO find out how to make enemies die immediately after setting dead flag
--      currently functionally identical to reducing to 1 hp
function ff.kill_all_enemies(require_gil)
    if not in_battle() then
        emu.message('Not in battle!');
        return;
    end

    if not require_gil or ff.spend_gil(100) then
        local p_hp = consts.ENEMY_INFO['HP'];
        local p_hp_lo = p_hp[1];
        local p_hp_hi = p_hp[2];

        local p_dead = consts.ENEMY_INFO['DEAD'];

        for i = 1, 9 do
            local p_enemy = consts.ENEMIES[i];
            memory.writebyte(p_enemy + p_hp_lo, 0x00);
            memory.writebyte(p_enemy + p_hp_hi, 0x00);
            memory.writebyte(p_enemy + p_dead, 0x01);
        end
    else
        emu.message('Not enough gil!');
    end
end


return ff;
