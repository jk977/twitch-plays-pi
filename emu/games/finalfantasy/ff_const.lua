-- ff_const.lua
-- ============
-- List of addresses and offsets pointing to various places in Final Fantasy 1's
-- memory.

local ff_const = {};

-- addresses of button press flags
ff_const.BUTTONS = {
    SELECT=0x0022,
    START=0x0023,
    A=0x0024,
    B=0x0025
};

-- party member addresses
ff_const.PARTY_MEMBERS = {
    0x6100, 0x6140,
    0x6180, 0x61C0
};

-- party member info offsets
-- NAME contains the offset for each character in the name
-- all values with a 2-length table are for low and high bytes for one hex value, in that order
-- e.g., first member's current HP is at 0x6100 + {0x0A,0x0B} = 0x610A, 0x610B
ff_const.MEMBER_INFO = {
    NAME={0x02,0x03,0x04,0x05},
    LEVEL=0x26,
    HP={0x0A,0x0B},
    MAX_HP={0x0C,0x0D},
    XP={0x07,0x08},
    XP_NEXT={0x16,0x17},
    ID=0x00,
    STATUS=0x01,
    STR=0x10,
    AGL=0x11,
    INT=0x12,
    VIT=0x13,
    LUCK=0x14,
    WEAPONS={0x18,0x19,0x1A,0x1B},
    ARMOR={0x1C,0x1D,0x1E,0x1F},
    DAMAGE=0x20,
    HIT=0x21,
    ABSORB=0x22,
    EVADE=0x23
};

-- party member magic info
-- the size for each member is 0x2F bytes, with a 0x10-byte buffer between each
-- e.g., second party member magic info goes from 0x6340 to 0x636F
ff_const.MEMBER_MAGIC = { 0x6300, 0x6340, 0x6380, 0x63C0 };

-- offsets for member spells
ff_const.SPELLS = {
    L1={0x00,0x01,0x02}, L2={0x04,0x05,0x06},
    L3={0x08,0x09,0x0A}, L4={0x0C,0x0D,0x0E},
    L5={0x10,0x11,0x12}, L6={0x14,0x15,0x16},
    L7={0x18,0x19,0x1A}, L8={0x1C,0x1D,0x1E}
};

-- offsets for member's max MP for each level
ff_const.MP_MAX = {
    L1=0x20, L2=0x21,
    L3=0x22, L4=0x23,
    L5=0x24, L6=0x25,
    L7=0x26, L8=0x27
};

-- offsets for member's current MP
ff_const.CURRENT_MP = {
    L1=0x28, L2=0x29,
    L3=0x2A, L4=0x2B,
    L5=0x2C, L6=0x2D,
    L7=0x2E, L8=0x2F,
};

-- battle-related addresses
ff_const.HIT_COUNT = 0x686A; -- number of hits in one attack
ff_const.CRIT = 0x686B; -- assign to 0x1 for critical hit

-- gear values
ff_const.GEAR = {
    NOTHING=0x00,
    WOODEN_NUNCHUCK=0x01,
    SMALL_KNIFE=0x02,
    WOODEN_STAFF=0x03,
    RAPIER=0x04,
    IRON_HAMMER=0x05,
    SHORT_SWORD=0x06,
    HAND_AXE=0x07,
    SCIMTAR=0x08,
    IRON_NUNCHUCK=0x09,
    LARGE_KNIFE=0x0A,
    IRON_STAFF=0x0B,
    SABRE=0x0C,
    LONG_SWORD=0x0D,
    GREAT_AXE=0x0E,
    FALCHON=0x0F,
    SILVER_KNIFE=0x10,
    SILVER_SWORD=0x11,
    SILVER_HAMMER=0x12,
    SILVER_AXE=0x13,
    FLAME_SWORD=0x14,
    ICE_SWORD=0x15,
    DRAGON_SWORD=0x16,
    GIANT_SWORD=0x17,
    SUN_SWORD=0x18,
    COREL_SWORD=0x19,
    WERE_SWORD=0x1A,
    RUNE_SWORD=0x1B,
    POWER_STAFF=0x1C,
    LIGHT_AXE=0x1D,
    HEAL_STAFF=0x1E,
    MAGE_STAFF=0x1F,
    DEFENSE=0x20,
    WIZARD_STAFF=0x21,
    VORPAL=0x22,
    CATCLAW=0x23,
    THOR_HAMMER=0x24,
    BANE_SWORD=0x25,
    KATANA=0x26,
    XCALBER=0x27,
    MASAMUNE=0x28,
    CLOTH=0x29,
    WOODEN_ARMOR=0x2A,
    CHAIN_ARMOR=0x2B,
    IRON_ARMOR=0x2C,
    STEEL_ARMOR=0x2D,
    SILVER_AMROR=0x2E,
    FLAME_ARMOR=0x2F,
    ICE_ARMOR=0x30,
    OPAL_ARMOR=0x31,
    DRAGON_ARMOR=0x32,
    COPPER_BRACELET=0x33,
    SILVER_BRACELET=0x34,
    GOLD_BRACELET=0x35,
    OPAL_BRACELET=0x36,
    WHITE_SHIRT=0x37,
    BLACK_SHIRT=0x38,
    WOODEN_SHIELD=0x39,
    IRON_SHIELD=0x3A,
    SILVER_SHIELD=0x3B,
    FLAME_SHIELD=0x3C,
    ICE_SHIELD=0x3D,
    OPAL_SHIELD=0x3E,
    AEGIS=0x3F,
    BUCKLER=0x40,
    PROCAPE=0x41,
    CAPE=0x42,
    WOODEN_HELMET=0x43,
    IRON_HELMET=0x44,
    SILVER_HELMET=0x45,
    OPAL_HELMET=0x46,
    HEAL_HELMET=0x47,
    RIBBON=0x48,
    GLOVES=0x49,
    COPPER_GAUNTLET=0x4A,
    IRON_GAUNTLET=0x4B,
    SILVER_GAUNTLET=0x4C,
    ZEUS_GAUNTLET=0x4D,
    POWER_GAUNTLET=0x4E,
    OPAL_GAUNTLET=0x4F,
    PRORING=0x50
};

return ff_const;
