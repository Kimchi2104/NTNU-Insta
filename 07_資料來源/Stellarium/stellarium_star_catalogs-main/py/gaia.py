import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord

# constant
MAS2RAD = 4.8481368110953594e-9


def jk_to_bprp(jmag, kmag):
    """
    Parameters
    ----------
    jmag : float
        2MASS J magnitude
    kmag : float
        2MASS K magnitude

    Returns
    -------
    bprp : float
        Estimated Gaia BP-RP color
    """
    return np.polyval([-0.8027, 2.788, -2.782, 2.581, 0.09396], jmag - kmag)


def gbprp_to_bv(gmag, bprp, red_correction=False):
    """
    Parameters
    ----------
    gmag : float
        Gaia G magnitude
    bprp : float
        Gaia BP-RP color
    red_correction : bool
        Apply red end correction for dwarfs and red giants

    Returns
    -------
    vmag : float
        Johnson V magnitude
    b-v: float
        Johnson B-V color
    """
    if len(gmag) == 1 and (np.isnan(bprp) or np.isnan(gmag)):
        raise ValueError("gmag or bprp is missing")
    # actually a good approximation for Vmag, ~0.03 mag
    vmag = gmag - np.polyval([0.01426, -0.2156, 0.01424, -0.02704], bprp)
    # Most of the time a good approximation for Bmag, ~0.03 mag except for stars with Gbp - Grp ~ 2.-3.
    # Barnard's star is a bad example
    bmag = gmag - np.polyval([-0.006061, 0.06718, -0.3604, -0.6874, 0.01448], bprp)

    # If the stars are missing bp-rp color, just assume vmag = gmag and b-v = 0.65 (like our Sun)
    # all should have gmag
    if len(gmag) > 1:
        vmag[np.isnan(bprp)] = gmag[np.isnan(bprp)]
        bmag[np.isnan(bprp)] = gmag[np.isnan(bprp)] + 0.65

    if red_correction:  # apply red end correction
        dwarfs_mask = (bprp > 2.2)
        bmag[dwarfs_mask] = gmag[dwarfs_mask] - np.polyval([-0.5,-1.6], bprp[dwarfs_mask])
    return vmag, bmag - vmag


def apply_space_motion(ra, dec, pmra_cosdec, pmdec, parallax=None, rv=None, t1=Time("2000", format="jyear"), t2=Time("2000", format="jyear")):
    """
    Use astropy to properly apply 6D space motion to a star

    Useful JD:
    J2000.0 = 2451545.0
    J2016.0 = 2457388.0

    Parameters
    ----------
    ra : float
        Right Ascension in degrees
    dec : float
        Declination in degrees
    ppmra_cosdecmra : float
        Proper motion in RA in mas/yr (including cos(dec) factor)
    pmdec : float
        Proper motion in Dec in mas/yr
    parallax : float
        Parallax in mas
    rv : float
        Radial velocity in km/s
    t1 : astropy.time.Time
        Time 1 for the epoch where the observation was made
    t2 : astropy.time.Time
        Time 2 for the new epoch you want to convert to

    Returns
    -------
    ra_new : float
        Right Ascension in degrees at the new epoch
    dec_new : float
        Declination in degrees at the new epoch
    pmra_cosdec_new : float
        Proper motion in RA in mas/yr at the new epoch (including cos(dec) factor)
    pmdec_new : float
        Proper motion in Dec in mas/yr at the new epoch
    parallax_new : float
        Parallax in mas at the new epoch
    rv_new : float
        Radial velocity in km/s at the new epoch
    """
    if parallax is None or rv is None:  # 3D without parallax and rv
        c = SkyCoord(
            ra=ra * u.deg,
            dec=dec * u.deg,
            pm_ra_cosdec=pmra_cosdec * u.mas / u.yr,
            pm_dec=pmdec * u.mas / u.yr,
            obstime=t1,
        )
        c2 = c.apply_space_motion(t2)
        return (c2.ra.deg, c2.dec.deg, c2.pm_ra_cosdec.value, c2.pm_dec.value)
    else:  # 6D
        c = SkyCoord(
            ra=ra * u.deg,
            dec=dec * u.deg,
            pm_ra_cosdec=pmra_cosdec * u.mas / u.yr,
            pm_dec=pmdec * u.mas / u.yr,
            distance=(1 / parallax) * u.kpc,
            radial_velocity=rv * u.km / u.s,
            obstime=t1,
        )
        c2 = c.apply_space_motion(t2)
        return (c2.ra.deg, c2.dec.deg, c2.pm_ra_cosdec.value, c2.pm_dec.value, 1 / c2.distance.value, c2.radial_velocity.value)
    

def change_epoch(ra, dec, pmra, pmdec, epoch, target_epoch=2000.0):
    """
    Parameters
    ----------
    ra : float
        Right ascension in degrees
    dec : float
        Declination in degrees
    pmra : float
        Proper motion in right ascension in mas/yr
    pmdec : float
        Proper motion in declination in mas/yr
    epoch : float
        Epoch of the given right ascension and declination
    target_epoch : float
        Target epoch to change the right ascension and declination to
    """
    # the observartion is J1991.25
    depoch = epoch - target_epoch
    dra = pmra / np.cos(dec / 180.0 * np.pi) / 3600000.0 * depoch
    ddec = pmdec / 3600000.0 * depoch
    return ra - dra, dec - ddec
