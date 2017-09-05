-- ff.lua
-- ======
-- Contains scripts specific to Final Fantasy 1.

local consts = require('games.finalfantasy.ff_const');
local emutils = require('emutils');
local ff = {};


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

    return hex_bytes;
end


local function correct_stat_value(stat, value)
    value = tonumber(value);
    stat = stat:lower();

    if value < 0 then
        return false;
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
        return false;
    end
end


-- for future use; currently doesn't allow name-changing or status manipulation
local function change_member_stat(member, stat, value)
    member = tonumber(member);
    stat = tostring(stat):lower();
    value = correct_stat_value(stat, value);

    if not value or member < 1 or member > 4 then
        return false;
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

    return true;
end


-- returns true if player is fighting enemies
local function in_battle()
    return memory.readbyte(0x0081) == 0x68;
end


local function get_attacking_member()
    return memory.readbyte(consts.ATTACKING_MEMBER);
end


function ff.do_cheat(cheat)
    
    if cheat == 'heal' then
        ff.cure_all(true);
    elseif cheat == 'killall' then
        ff.kill_all_enemies(true);
    elseif cheat == 'showgil' then
        ff.print_gil();
    elseif cheat == 'attack' then
        ff.attack();
    elseif cheat == 'run' then
        ff.run();
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
    
    -- distributes attacks evenly between enemies
    for i = 1, living_members do
        -- moves cursor to enemy and attacks, compensating for battle animations
        emutils.advance_frames(19);
        emutils.press_button(1, 'A', 1);
        emutils.press_button(1, 'down', i-1);
        emutils.advance_frames(2);
        emutils.press_button(1, 'A', 1);
        emutils.advance_frames(19);
    end
end


-- runs with each person
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



-- used for chat cheats
function ff.spend_gil(amt)
    local p_gil_hi = consts.GIL[2];
    local p_gil_lo = consts.GIL[1];
    local gil_hi = string.format('%02x', memory.readbyte(p_gil_hi));
    local gil_lo = string.format('%02x', memory.readbyte(p_gil_lo));

    local current = tonumber(gil_hi .. gil_lo, 16);

    if current >= amt then
        local balance = current - amt;
        local balance16 = string.format('%04x', balance);

        local balance_hi = tonumber(balance16:sub(1,2), 16);
        local balance_lo = tonumber(balance16:sub(3,4), 16);

        emu.message(tostring(amt) .. 'g spent!');
        memory.writebyte(p_gil_hi, balance_hi);
        memory.writebyte(p_gil_lo, balance_lo);
        return true;
    else
        return false;
    end
end


-- prints gil amount on emulator screen
function ff.print_gil()
    p_gil = consts.GIL;
    gil_lo = string.format('%02x', memory.readbyte(p_gil[1]));
    gil_hi = string.format('%02x', memory.readbyte(p_gil[2]));

    gil = tostring(tonumber(gil_hi .. gil_lo, 16));
    emu.message('Current gil: ' .. gil);
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
