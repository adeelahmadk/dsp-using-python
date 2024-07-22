import numpy as np

def read_uint12(data_chunk):
    """
    unpacks 12-bit little endian data into numpy array
    """
    data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, mid_uint8, lst_uint8 = np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint16).T
    fst_uint12 = ((mid_uint8 & 0x0F) << 8) | fst_uint8
    snd_uint12 = (lst_uint8 << 4) | ((mid_uint8 & 0xF0) >> 4)
    return np.reshape(np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1), 2 * fst_uint12.shape[0])


def read_uint16(data_chunk):
    """
    unpacks 16-bit little endian data into numpy array
    """
    data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, snd_uint8 = np.reshape(data, (data.shape[0] // 2, 2)).astype(np.uint16).T
    num_uint16 = (snd_uint8 << 8) | fst_uint8
    return num_uint16


