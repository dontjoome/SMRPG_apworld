# Map randomization logic.

from .patch import Patch
from .utils import ByteField

# Vanilla map object data for node unlocks and each cardinal direction.
# Format: (Node unlock, east, south, west, north)
# If a direction is 0xff, there's nothing there.
MAP_OBJECT_DATA = (
    (0x4100, 0xff, 0xff, 0x41, 0x41),
    (0x100, 0x41, 0x41, 0xff, 0xff),
    (0x415b, 0xff, 0xff, 0x5b, 0x5b),
    (0x11b, 0x5b, 0x5b, 0x5f, 0x5f),
    (0x11b, 0x5f, 0x5f, 0x5a, 0x5d),
    (0x11d, 0xff, 0x5d, 0xff, 0xff),
    (0x415a, 0x5a, 0x5a, 0xff, 0xff),
    (0x4141, 0x41, 0x41, 0xff, 0xff),
    (0x101, 0x42, 0xff, 0x41, 0x41),
    (0x102, 0x43, 0x43, 0x42, 0xff),
    (0x103, 0x45, 0x44, 0x44, 0x43),
    (0x104, 0x44, 0xff, 0xff, 0x44),
    (0x4145, 0xff, 0xff, 0x45, 0x45),
    (0x4145, 0xff, 0x45, 0x45, 0xff),
    (0x105, 0x45, 0x46, 0x46, 0x45),
    (0x106, 0x46, 0xff, 0x47, 0x46),
    (0x107, 0x47, 0x48, 0xff, 0xff),
    (0x109, 0xff, 0xff, 0x4a, 0x48),
    (0x10a, 0x4a, 0xff, 0x4c, 0x4b),
    (0x10b, 0xff, 0x4b, 0xff, 0xff),
    (0x10c, 0x4c, 0x4d, 0x4c, 0xff),
    (0x414d, 0xff, 0xff, 0xff, 0x4d),
    (0x414c, 0x4c, 0x4c, 0xff, 0xff),
    (0x414c, 0xff, 0xff, 0x4c, 0xff),
    (0x10e, 0x4c, 0xff, 0x4e, 0xff),
    (0x10f, 0x4e, 0xff, 0x4f, 0x4f),
    (0x110, 0x4f, 0x4f, 0x50, 0xff),
    (0x11c, 0x50, 0xff, 0x5c, 0x5c),
    (0x111, 0x5c, 0x5c, 0x51, 0x51),
    (0x4151, 0x51, 0x51, 0xff, 0xff),
    (0x4151, 0xff, 0xff, 0x51, 0x51),
    (0x112, 0x51, 0xff, 0x52, 0xff),
    (0x113, 0x52, 0xff, 0x53, 0x55),
    (0x114, 0x53, 0x54, 0x54, 0xff),
    (0x115, 0x54, 0xff, 0xff, 0x54),
    (0x4155, 0xff, 0x55, 0xff, 0xff),
    (0x4155, 0xff, 0xff, 0xff, 0x55),
    (0x116, 0xff, 0x55, 0x56, 0x57),
    (0x117, 0x56, 0xff, 0xff, 0x56),
    (0x118, 0xff, 0x57, 0x5e, 0x58),
    (0x11e, 0x5e, 0xff, 0xff, 0xff),
    (0x4158, 0xff, 0x58, 0xff, 0xff),
    (0x4155, 0xff, 0xff, 0xff, 0x55),
    (0x116, 0xff, 0x55, 0x56, 0x57),
    (0x117, 0x56, 0xff, 0xff, 0x56),
    (0x118, 0xff, 0x57, 0x5e, 0x58),
    (0x11e, 0x5e, 0xff, 0xff, 0xff),
    (0x4158, 0xff, 0x58, 0xff, 0xff),
    (0x4158, 0xff, 0xff, 0xff, 0x58),
    (0x119, 0x59, 0x58, 0xff, 0x5a),
    (0x11a, 0xff, 0xff, 0x59, 0x59),
    (0x415a, 0xff, 0x5a, 0xff, 0xff),
    (0x10d, 0xff, 0xff, 0xff, 0x4d),
    (0x414d, 0xff, 0x4d, 0xff, 0xff),
    (0x140, 0xff, 0xff, 0xff, 0xff),
)


def unlock_world_map():
    """Get patch data to unlock the entire world map for testing.

    :rtype: randomizer.logic.patch.Patch
    """
    base_address = 0x3ef830
    patch = Patch()

    for i, (node_unlock, east, south, west, north) in enumerate(MAP_OBJECT_DATA):
        node_address = base_address + (i * 16)
        node_unlock &= 0xfc00
        node_unlock |= 0x100
        patch.add_data(node_address + 2, ByteField(node_unlock, num_bytes=2).as_bytes())

        for offset, direction in zip((8, 10, 12, 14), (east, south, west, north)):
            if direction != 0xff:
                direction &= 0xc0
                direction |= 1
                patch.add_data(node_address + offset, ByteField(direction).as_bytes())

    return patch
