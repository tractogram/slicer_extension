from nibabel import trackvis as tv
import numpy as np

class FileError(Exception):
    """ Error in  streamline file
    """
header_2_dtd = [
    ('id_string', 'S6'),
    ('dim', 'h', 3),
    ('voxel_size', 'f4', 3),
    ('origin', 'f4', 3),
    ('n_scalars', 'h'),
    ('scalar_name', 'S20', 10),
    ('n_properties', 'h'),
    ('property_name', 'S20', 10),
    ('vox_to_ras', 'f4', (4,4)), # new field for version 2
    ('reserved', 'S444'),
    ('voxel_order', 'S4'),
    ('pad2', 'S4'),
    ('image_orientation_patient', 'f4', 6),
    ('pad1', 'S2'),
    ('invert_x', 'S1'),
    ('invert_y', 'S1'),
    ('invert_z', 'S1'),
    ('swap_xy', 'S1'),
    ('swap_yz', 'S1'),
    ('swap_zx', 'S1'),
    ('n_count', 'i4'),
    ('version', 'i4'),
    ('hdr_size', 'i4'),
    ]
header_2_dtype = np.dtype(header_2_dtd)
dt = header_2_dtype
print dt
hdr = np.zeros((), dtype=dt)
print hdr.dtype