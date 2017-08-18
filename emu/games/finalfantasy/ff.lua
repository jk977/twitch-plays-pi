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


function ff.do_crit()
    memory.writebyte(consts.CRIT, 0x1);
    return true;
end


-- currently doesn't allow name-changing
function ff.change_member_stat(member, stat, value)
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


return ff;
