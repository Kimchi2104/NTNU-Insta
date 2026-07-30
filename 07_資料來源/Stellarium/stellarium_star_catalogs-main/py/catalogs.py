import pathlib
import struct
import pandas as pd
import numpy as np
import tqdm


def decode_star_hip(encoded):
    # Ensure the encoded value is exactly 3 bytes
    if len(encoded) != 3:
        raise ValueError("Encoded value must be 3 bytes.")
    
    # Unpack the 3 bytes into a 24-bit integer (little-endian format)
    combined_value = struct.unpack("<I", encoded.ljust(4, b'\0'))[0]
    
    # Extract the hip (17-bit) and letter_value (5-bit)
    hip = combined_value >> 5
    letter_value = combined_value & 0x1F  # Mask to get the lower 5 bits
    
    return hip, letter_value


def read_to_dataframe(file: pathlib.Path) -> pd.DataFrame:
    f = open(file, "rb")

    # Read the header (28 bytes)
    header = struct.unpack("6if", f.read(28))
    header = dict(
        zip(
            (
                "Magic",
                "Data Type",
                "Major Version",
                "Minor Version",
                "Level",
                "Magnitude Minimum",
                "Epoch",
            ),
            header,
        )
    )
    n_zones = 20 * 4 ** header["Level"] + 1

    # Unpack the zone information
    zone_info = struct.unpack(f"{n_zones}I", f.read(n_zones * 4))
    max_records = sum(zone_info)

    # Define the header for the star data
    if header["Data Type"] == 0:
        star_header = (
            "source_id",
            "x0",
            "x1",
            "x2",
            "dx0",
            "dx1",
            "dx2",
            "b_v",
            "mag",
            "plx",
            "plx_err",
            "rv",
            "sp_int",
            "otype",
            "hip",
            "componentid",
        )
    elif header["Data Type"] == 1:
        star_header = (
            "source_id",
            "x0",
            "x1",
            "dx0",
            "dx1",
            "b_v",
            "mag",
            "plx",
            "plx_err",
        )
    else:
        star_header = (
            "source_id",
            "x0",
            "x1",
            "b_v",
            "mag",
        )

    # Create a dataframe to store the stars
    df = pd.DataFrame(columns=star_header, index=range(max_records))

    # put header in dataframe for reference with df.attrs
    for i in header:
        df.attrs[i] = header[i]

    for i in tqdm.tqdm(range(max_records), desc="Reading stars"):
        if header["Data Type"] == 0:
            star = struct.unpack("qiiiiiihhHHhHB", f.read(45))
            hip, componentid = decode_star_hip(f.read(3))
            df.loc[i] = star + (hip, componentid, )
        elif header["Data Type"] == 1:
            star = struct.unpack("qiiiihhHH", f.read(32))
            # add to dataframe
            df.loc[i] = star
        else:
            source_id = struct.unpack("q", f.read(8))[0]
            # recover uint32 from 3 bytes
            x0 = struct.unpack("<I", b"\0" + f.read(3))[0]
            x1 = struct.unpack("<I", b"\0" + f.read(3))[0]
            b_v = struct.unpack("b", f.read(1))[0]
            mag = struct.unpack("b", f.read(1))[0]
            df.loc[i] = (source_id, x0, x1, b_v, mag)

    # create zone data array
    zone_data = np.zeros(max_records, dtype=int)
    i = 0
    for idx, n in enumerate(zone_info):
        zone_data[i:i+n] = idx
        i += n
    df["zone"] = zone_data

    return df