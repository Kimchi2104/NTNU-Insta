# -*- coding: utf-8 -*-
"""calc_a18_astronomy.py - Rigorous astronomical computations for Episode A-18.
"""

import math
import zoneinfo
from datetime import datetime, timezone, timedelta
from skyfield.api import load, wgs84, Star
from skyfield import almanac

# Constants
TAIPEI_LAT = 25.033
TAIPEI_LON = 121.565
TAIPEI_ELEV = 10.0
TZ_TAIPEI = zoneinfo.ZoneInfo("Asia/Taipei")

GIZA_LAT = 29.979
MEMPHIS_LAT = 29.85
CAIRO_LAT = 30.04
ASWAN_LAT = 24.09

ts = load.timescale()
eph = load("de421.bsp")
earth = eph["earth"]

# Stars HIP & proper motions / coordinates
# Sirius (HIP 32349, α CMa)
# J2000: RA 06h 45m 08.917s, Dec -16° 42' 58.02"
# pm_ra: -546.01 mas/yr, pm_dec: -1223.07 mas/yr
sirius = Star(ra_hours=(6, 45, 8.917), dec_degrees=(-16, 42, 58.02),
              ra_mas_per_year=-546.01, dec_mas_per_year=-1223.07,
              parallax_mas=379.21, radial_km_per_s=-5.5)

# Canopus (HIP 30438, α Car)
canopus = Star(ra_hours=(6, 23, 57.110), dec_degrees=(-52, 41, 44.38),
               ra_mas_per_year=19.99, dec_mas_per_year=23.67,
               parallax_mas=10.55, radial_km_per_s=20.5)

# Betelgeuse (HIP 27989, α Ori)
betelgeuse = Star(ra_hours=(5, 55, 10.305), dec_degrees=(7, 24, 25.43))

# Rigel (HIP 24436, β Ori)
rigel = Star(ra_hours=(5, 14, 32.272), dec_degrees=(-8, 12, 5.90))

# Alnitak (HIP 26727, ζ Ori)
alnitak = Star(ra_hours=(5, 40, 45.527), dec_degrees=(-1, 56, 34.26))

# Dubhe (HIP 54061, α UMa)
dubhe = Star(ra_hours=(11, 3, 43.67), dec_degrees=(61, 45, 3.7))

# Alkaid (HIP 67301, η UMa)
alkaid = Star(ra_hours=(13, 47, 32.44), dec_degrees=(49, 18, 47.8))

# Thuban (HIP 68756, α Dra)
thuban = Star(ra_hours=(14, 4, 23.35), dec_degrees=(64, 22, 33.1))

# Polaris (HIP 11767, α UMi)
polaris = Star(ra_hours=(2, 31, 49.08), dec_degrees=(89, 15, 50.8))

taipei_topos = wgs84.latlon(TAIPEI_LAT, TAIPEI_LON, elevation_m=TAIPEI_ELEV)
obs_taipei = earth + taipei_topos

print("======================================================================")
print("PART 1: TAIPEI 2027-01-22 SKYCLOCKING")
print("======================================================================")

# Rise / Set / Transit on 2027-01-22 for Sirius & Canopus & Alkaid
t0 = ts.from_datetime(datetime(2027, 1, 22, 0, 0, tzinfo=TZ_TAIPEI))
t1 = ts.from_datetime(datetime(2027, 1, 23, 0, 0, tzinfo=TZ_TAIPEI))

for s_name, s_obj in [("Sirius", sirius), ("Canopus", canopus), ("Alkaid", alkaid)]:
    f_rs = almanac.risings_and_settings(eph, s_obj, taipei_topos)
    times_rs, events_rs = almanac.find_discrete(t0, t1, f_rs)
    f_tr = almanac.meridian_transits(eph, s_obj, taipei_topos)
    times_tr, events_tr = almanac.find_discrete(t0, t1, f_tr)
    
    print(f"\n--- {s_name} ---")
    for t, ev in zip(times_rs, events_rs):
        ev_str = "Rise" if ev == 1 else "Set"
        print(f"  {ev_str}: {t.astimezone(TZ_TAIPEI).strftime('%H:%M:%S')}")
    for t, ev in zip(times_tr, events_tr):
        if ev == 1:
            alt, az, _ = (obs_taipei).at(t).observe(s_obj).apparent().altaz()
            print(f"  Upper Transit: {t.astimezone(TZ_TAIPEI).strftime('%H:%M:%S')} CST, Culmination Alt = {alt.degrees:.2f}°")

# Target times: 20:00, 22:30, 22:33
for hr, mn in [(20, 0), (22, 30), (22, 33)]:
    dt = datetime(2027, 1, 22, hr, mn, tzinfo=TZ_TAIPEI)
    t = ts.from_datetime(dt)
    print(f"\n=== Taipei {hr:02d}:{mn:02d} CST ===")
    for name, obj in [
        ("Sirius", sirius), ("Canopus", canopus), ("Betelgeuse", betelgeuse),
        ("Rigel", rigel), ("Dubhe", dubhe), ("Alkaid", alkaid), ("Polaris", polaris)
    ]:
        alt, az, _ = obs_taipei.at(t).observe(obj).apparent().altaz()
        print(f"  {name:12s}: Alt = {alt.degrees:6.2f}°, Az = {az.degrees:6.2f}°")
    
    # Moon
    moon = eph["moon"]
    alt_m, az_m, _ = obs_taipei.at(t).observe(moon).apparent().altaz()
    print(f"  {'Moon':12s}: Alt = {alt_m.degrees:6.2f}°, Az = {az_m.degrees:6.2f}°")

# Full moon time around 2027-01-22
t_m0 = ts.from_datetime(datetime(2027, 1, 20, tzinfo=timezone.utc))
t_m1 = ts.from_datetime(datetime(2027, 1, 25, tzinfo=timezone.utc))
p_times, p_events = almanac.find_discrete(t_m0, t_m1, almanac.moon_phases(eph))
for t, ev in zip(p_times, p_events):
    if ev == 2:
        print(f"\nFull Moon exact time: {t.astimezone(TZ_TAIPEI).strftime('%Y-%m-%d %H:%M:%S %Z')}")

print("\n======================================================================")
print("PART 2: ANCIENT EGYPT & PRE-2500 BCE CALCULATIONS")
print("======================================================================")
# In c. -2500 (2500 BCE):
# Coordinates of Sirius at -2500:
t_ancient = ts.tt_jd(ts.utc(-2500, 6, 21).tt)
# Observe Sirius from Earth at -2500
app_sirius_ancient = earth.at(t_ancient).observe(sirius).apparent()
ra_anc, dec_anc, _ = app_sirius_ancient.radec()
print(f"Sirius in 2500 BCE: RA = {ra_anc.hours:.3f} h, Dec = {dec_anc.degrees:.3f}°")

# Observe Thuban at -2500, -2800
for yr in [-2800, -2560, -2500, -2450]:
    t_yr = ts.tt_jd(ts.utc(yr, 6, 21).tt)
    app_thuban = earth.at(t_yr).observe(thuban).apparent()
    ra_th, dec_th, _ = app_thuban.radec()
    dist_to_np = 90.0 - dec_th.degrees
    print(f"Thuban in {yr} BCE: Dec = {dec_th.degrees:.3f}°, Dist to NCP = {dist_to_np:.3f}°")

# Observe Alnitak at -2500
t_2500 = ts.tt_jd(ts.utc(-2500, 1, 1).tt)
app_alnitak = earth.at(t_2500).observe(alnitak).apparent()
_, dec_aln, _ = app_alnitak.radec()
# Culmination altitude at Giza (29.979°N)
culm_alnitak_giza = 90.0 - GIZA_LAT + dec_aln.degrees
print(f"Alnitak in 2500 BCE: Dec = {dec_aln.degrees:.3f}°, Giza Culmination Alt = {culm_alnitak_giza:.2f}°")

print("\n======================================================================")
print("PART 3: HELIACAL RISING OF SIRIUS ACROSS EPOCHS")
print("======================================================================")
# Standard astronomical heliacal rising calculation:
# For each morning around summer, find when Sun altitude at dawn is between -12° and -9°,
# and Sirius altitude is at or above horizon (> 1°).
# Let's inspect the arc of vision (arcus visionis) for Sirius.
# Sirius has magnitude -1.46 (very bright!), so its arcus visionis is ~9.0° to 10.5°.
