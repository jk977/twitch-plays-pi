-- ff.lua
-- ======
-- Contains scripts specific to Final Fantasy 1.

local consts = require('ff_const');
local ff = {};


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


-- used for chat cheats
local function spend_gil(amt)
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


-- makes next hit a critical hit
function ff.do_crit(require_gil)
    if not in_battle() then
        emu.message('Not in battle!');
        return;
    end

    if not require_gil or spend_gil(50) then
        memory.writebyte(consts.CRIT, 0x1);
    else
        emu.message('Not enough gil!');
    end
end


-- cures all party members, including dead ones
function ff.cure_all(require_gil)
    if not require_gil or spend_gil(50) then
        for i = 1, 4 do
            p_member = consts.PARTY_MEMBERS[i];
            p_hp = consts.MEMBER_INFO['HP'];
            p_max_hp = consts.MEMBER_INFO['MAX_HP'];

            hp_lo = memory.readbyte(p_member + p_max_hp[1]);
            hp_hi = memory.readbyte(p_member + p_max_hp[2]);

            memory.writebyte(p_member + consts.MEMBER_INFO['STATUS'], 0);
            memory.writebyte(p_member + p_hp[1], hp_lo);
            memory.writebyte(p_member + p_hp[2], hp_hi);
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

    if not require_gil or spend_gil(50) then
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
