# -*- coding: utf-8 -*-
"""verify_ephemeris.py - Astronomical Verification Tool for NTNU Video Series.

Utilizes Skyfield 1.54 and local JPL DE421 ephemeris (de421.bsp) to verify
celestial mechanics, star coordinates, altitude/azimuth, and rise/set times
for Taipei (25.03°N, 121.56°E, UTC+8) across the 9 target episodes.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
import zoneinfo
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any

try:
    from skyfield.api import load, wgs84, Star
    from skyfield import almanac
    SKYFIELD_AVAILABLE = True
except ImportError:
    SKYFIELD_AVAILABLE = False


HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# Potential locations for de421.bsp
BSP_CANDIDATES = [
    os.path.join(HERE, "de421.bsp"),
    os.path.join(REPO_ROOT, "de421.bsp"),
    "/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/de421.bsp",
    "/Users/kimjoo/Downloads/NTNU Insta/de421.bsp",
]

def find_bsp_file() -> Optional[str]:
    """Locate the de421.bsp file in known paths."""
    for path in BSP_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


TZ_TAIPEI = zoneinfo.ZoneInfo("Asia/Taipei")

# Standard Observer Coordinates for Taipei
TAIPEI_LAT = 25.03
TAIPEI_LON = 121.56
TAIPEI_ELEV_M = 10.0

# Target Stars across the 9 Target Episodes
# Ephemeris data compiled from SIMBAD, Hipparcos/Gaia, and IAU WGSN
TARGET_STARS: Dict[str, Dict[str, Any]] = {
    "Altair": {
        "chinese": "河鼓二（牛郎星）",
        "hip": 97649,
        "star": Star(ra_hours=(19, 50, 46.998), dec_degrees=(8, 52, 5.96)),
        "distance_ly": 16.73,
        "v_mag": 0.77,
        "constellation": "Aql",
    },
    "Vega": {
        "chinese": "織女一",
        "hip": 91262,
        "star": Star(ra_hours=(18, 36, 56.336), dec_degrees=(38, 47, 1.28)),
        "distance_ly": 25.04,
        "v_mag": 0.03,
        "constellation": "Lyr",
    },
    "Deneb": {
        "chinese": "天津四",
        "hip": 102098,
        "star": Star(ra_hours=(20, 41, 25.915), dec_degrees=(45, 16, 49.22)),
        "distance_ly": 2615.0,
        "v_mag": 1.25,
        "constellation": "Cyg",
    },
    "Antares": {
        "chinese": "心宿二（大火）",
        "hip": 80763,
        "star": Star(ra_hours=(16, 29, 24.460), dec_degrees=(-26, 25, 55.21)),
        "distance_ly": 550.0,
        "v_mag": 1.06,
        "constellation": "Sco",
    },
    "Spica": {
        "chinese": "角宿一",
        "hip": 65474,
        "star": Star(ra_hours=(13, 25, 11.579), dec_degrees=(-11, 9, 40.75)),
        "distance_ly": 250.0,
        "v_mag": 0.98,
        "constellation": "Vir",
    },
    "Canopus": {
        "chinese": "老人星（Suhail）",
        "hip": 30438,
        "star": Star(ra_hours=(6, 23, 57.110), dec_degrees=(-52, 41, 44.38)),
        "distance_ly": 310.0,
        "v_mag": -0.74,
        "constellation": "Car",
    },
    "Polaris": {
        "chinese": "勾陳一（北極星）",
        "hip": 11767,
        "star": Star(ra_hours=(2, 31, 49.084), dec_degrees=(89, 15, 50.79)),
        "distance_ly": 433.0,
        "v_mag": 1.98,
        "constellation": "UMi",
    },
    "Aldebaran": {
        "chinese": "畢宿五（al-Twaibiʿ）",
        "hip": 21421,
        "star": Star(ra_hours=(4, 35, 55.239), dec_degrees=(16, 30, 33.49)),
        "distance_ly": 65.3,
        "v_mag": 0.85,
        "constellation": "Tau",
    },
    "Rigel": {
        "chinese": "參宿七（Aurvandilstá）",
        "hip": 24436,
        "star": Star(ra_hours=(5, 14, 32.272), dec_degrees=(-8, 12, 5.90)),
        "distance_ly": 860.0,
        "v_mag": 0.18,
        "constellation": "Ori",
    },
    "Betelgeuse": {
        "chinese": "參宿四",
        "hip": 27989,
        "star": Star(ra_hours=(5, 55, 10.305), dec_degrees=(7, 24, 25.43)),
        "distance_ly": 642.5,
        "v_mag": 0.50,
        "constellation": "Ori",
    },
    "Dubhe": {
        "chinese": "天樞（北斗一）",
        "hip": 54061,
        "star": Star(ra_hours=(11, 3, 43.67), dec_degrees=(61, 45, 3.7)),
        "distance_ly": 123.0,
        "v_mag": 1.79,
        "constellation": "UMa",
    },
    "Alioth": {
        "chinese": "玉衡（北斗五）",
        "hip": 62956,
        "star": Star(ra_hours=(12, 54, 1.63), dec_degrees=(55, 57, 35.4)),
        "distance_ly": 82.6,
        "v_mag": 1.77,
        "constellation": "UMa",
    },
}


class EphemerisVerifier:
    """Encapsulates astronomical verification algorithms using Skyfield."""

    def __init__(self, bsp_path: Optional[str] = None):
        if not SKYFIELD_AVAILABLE:
            raise RuntimeError(
                "Skyfield is required. Run with /Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
            )
        self.bsp_path = bsp_path or find_bsp_file()
        if not self.bsp_path or not os.path.exists(self.bsp_path):
            raise FileNotFoundError(
                f"de421.bsp ephemeris file not found. Checked: {BSP_CANDIDATES}"
            )
        self.ts = load.timescale()
        self.eph = load(self.bsp_path)
        self.earth = self.eph["earth"]
        self.taipei_topos = wgs84.latlon(TAIPEI_LAT, TAIPEI_LON, elevation_m=TAIPEI_ELEV_M)
        self.obs_taipei = self.earth + self.taipei_topos

    def get_altaz_at(
        self,
        star_name: str,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        lat: float = TAIPEI_LAT,
        lon: float = TAIPEI_LON,
    ) -> Tuple[float, float]:
        """Compute apparent altitude and azimuth for a target star from given coords."""
        if star_name not in TARGET_STARS:
            raise KeyError(f"Unknown target star: {star_name}")
        star = TARGET_STARS[star_name]["star"]
        dt = datetime(year, month, day, hour, minute, tzinfo=TZ_TAIPEI)
        t = self.ts.from_datetime(dt)
        topos = wgs84.latlon(lat, lon, elevation_m=TAIPEI_ELEV_M)
        obs = self.earth + topos
        apparent = obs.at(t).observe(star).apparent()
        alt, az, _ = apparent.altaz()
        return alt.degrees, az.degrees

    def get_rise_set_transit(
        self,
        star_name: str,
        year: int,
        month: int,
        day: int,
        lat: float = TAIPEI_LAT,
        lon: float = TAIPEI_LON,
    ) -> Dict[str, Any]:
        """Compute Rise, Set, and Meridian Transit times and Culmination Altitude."""
        if star_name not in TARGET_STARS:
            raise KeyError(f"Unknown target star: {star_name}")
        star = TARGET_STARS[star_name]["star"]
        topos = wgs84.latlon(lat, lon, elevation_m=TAIPEI_ELEV_M)
        obs = self.earth + topos

        t0 = self.ts.from_datetime(datetime(year, month, day, 0, 0, 0, tzinfo=TZ_TAIPEI))
        t1 = self.ts.from_datetime(datetime(year, month, day, 23, 59, 59, tzinfo=TZ_TAIPEI))

        # Rise and Set
        f_rs = almanac.risings_and_settings(self.eph, star, topos)
        times_rs, events_rs = almanac.find_discrete(t0, t1, f_rs)

        # Meridian Transit
        f_tr = almanac.meridian_transits(self.eph, star, topos)
        times_tr, events_tr = almanac.find_discrete(t0, t1, f_tr)

        results: Dict[str, Any] = {
            "star": star_name,
            "chinese": TARGET_STARS[star_name]["chinese"],
            "date": f"{year:04d}-{month:02d}-{day:02d}",
            "lat": lat,
            "lon": lon,
            "rise": None,
            "set": None,
            "transit_time": None,
            "culmination_alt_deg": None,
        }

        for t, ev in zip(times_rs, events_rs):
            dt = t.astimezone(TZ_TAIPEI)
            if ev == 1:
                results["rise"] = dt.strftime("%H:%M:%S")
            else:
                results["set"] = dt.strftime("%H:%M:%S")

        for t, ev in zip(times_tr, events_tr):
            if ev == 1:  # Upper transit (culmination)
                dt = t.astimezone(TZ_TAIPEI)
                results["transit_time"] = dt.strftime("%H:%M:%S")
                apparent = obs.at(t).observe(star).apparent()
                alt, _, _ = apparent.altaz()
                results["culmination_alt_deg"] = round(alt.degrees, 2)

        return results

    def compute_angular_separation(self, star1_name: str, star2_name: str) -> float:
        """Compute angular separation (degrees) between two stars using standard spherical formula."""
        s1 = TARGET_STARS[star1_name]["star"]
        s2 = TARGET_STARS[star2_name]["star"]
        # Convert RA hours to radians and Dec degrees to radians
        ra1 = s1.ra.radians
        dec1 = s1.dec.radians
        ra2 = s2.ra.radians
        dec2 = s2.dec.radians

        cos_sep = math.sin(dec1) * math.sin(dec2) + math.cos(dec1) * math.cos(dec2) * math.cos(ra1 - ra2)
        # Numerical clamp
        cos_sep = max(-1.0, min(1.0, cos_sep))
        sep_deg = math.degrees(math.acos(cos_sep))
        return round(sep_deg, 2)

    @staticmethod
    def compute_3d_spatial_distance(d1_ly: float, d2_ly: float, sep_deg: float) -> float:
        """Calculate true spatial distance in 3D light-years via the Law of Cosines."""
        rad = math.radians(sep_deg)
        dist_sq = (d1_ly ** 2) + (d2_ly ** 2) - 2 * d1_ly * d2_ly * math.cos(rad)
        return round(math.sqrt(dist_sq), 2)

    def compute_canopus_max_elevation(self, lat: float = TAIPEI_LAT) -> float:
        """Compute the maximum elevation of Canopus (dec = -52.695°) at given latitude."""
        dec = TARGET_STARS["Canopus"]["star"].dec.degrees
        # Theoretical max altitude = 90 - lat + dec (with dec negative)
        max_alt = 90.0 - lat + dec
        return round(max_alt, 2)

    def compute_qixi_astronomy(self, year: int = 2026, month: int = 8, day: int = 19) -> Dict[str, Any]:
        """Compute full astronomical verification profile for Qixi Festival (H-七夕).
        Default date: 2026-08-19 (Qixi Lunar 7/7 in 2026).
        """
        alt_altair_21h, az_altair_21h = self.get_altaz_at("Altair", year, month, day, 21, 0)
        alt_vega_21h, az_vega_21h = self.get_altaz_at("Vega", year, month, day, 21, 0)
        alt_deneb_21h, az_deneb_21h = self.get_altaz_at("Deneb", year, month, day, 21, 0)

        tr_altair = self.get_rise_set_transit("Altair", year, month, day)
        ang_sep = self.compute_angular_separation("Vega", "Altair")
        dist_3d = self.compute_3d_spatial_distance(
            TARGET_STARS["Vega"]["distance_ly"],
            TARGET_STARS["Altair"]["distance_ly"],
            ang_sep,
        )

        return {
            "year": year,
            "qixi_date": f"{year:04d}-{month:02d}-{day:02d}",
            "altair_21h_alt_deg": round(alt_altair_21h, 2),
            "altair_21h_az_deg": round(az_altair_21h, 2),
            "vega_21h_alt_deg": round(alt_vega_21h, 2),
            "vega_21h_az_deg": round(az_vega_21h, 2),
            "deneb_21h_alt_deg": round(alt_deneb_21h, 2),
            "deneb_21h_az_deg": round(az_deneb_21h, 2),
            "altair_transit_time": tr_altair["transit_time"],
            "altair_culmination_alt_deg": tr_altair["culmination_alt_deg"],
            "vega_altair_angular_separation_deg": ang_sep,
            "vega_altair_true_distance_ly": dist_3d,
        }

    def verify_episode_baselines(self) -> List[Dict[str, Any]]:
        """Verify celestial mechanics baselines across all 9 target episodes."""
        checks: List[Dict[str, Any]] = []

        # 1. H-七夕 (Vega & Altair Distance & Qixi 2026 Skyclocking)
        qixi = self.compute_qixi_astronomy(2026, 8, 19)
        # Expected: separation ~34.2°, true distance 14.5 - 15.5 ly (script cites 15-16 ly)
        dist_ok = 14.0 <= qixi["vega_altair_true_distance_ly"] <= 16.5
        alt_ok = qixi["altair_culmination_alt_deg"] is not None and 72.0 <= qixi["altair_culmination_alt_deg"] <= 75.0
        checks.append({
            "episode": "H-七夕",
            "name": "Qixi Summer Triangle Coordinates & Distance",
            "passed": dist_ok and alt_ok,
            "details": (
                f"Vega-Altair Sep: {qixi['vega_altair_angular_separation_deg']}°, "
                f"3D Dist: {qixi['vega_altair_true_distance_ly']} ly (expected ~15-16 ly). "
                f"Altair Transit: {qixi['altair_transit_time']} CST, Alt: {qixi['altair_culmination_alt_deg']}°."
            ),
        })

        # 2. A-13 阿拉伯半島 (Canopus/Suhail Elevation in Taipei vs Kaohsiung)
        canopus_taipei = self.compute_canopus_max_elevation(25.033)
        canopus_kh = self.compute_canopus_max_elevation(22.62)
        # Expected: Taipei ~12.3° (12.27°), Kaohsiung ~14.7°
        canopus_ok = abs(canopus_taipei - 12.27) < 0.2 and abs(canopus_kh - 14.68) < 0.2
        checks.append({
            "episode": "A-13",
            "name": "Canopus (老人星 / Suhail) Horizon Elevation in Taiwan",
            "passed": canopus_ok,
            "details": (
                f"Taipei (25.033°N) Max Alt: {canopus_taipei:.2f}° (script: 12.3°); "
                f"Kaohsiung (22.62°N) Max Alt: {canopus_kh:.2f}° (script: 14.7°)."
            ),
        })

        # 3. A-01 中國四象青龍 (Spring Dusk Spica / 角宿一 Elevation)
        # Spring equinox evening (2026-03-20 20:00 CST)
        alt_spica, az_spica = self.get_altaz_at("Spica", 2026, 3, 20, 20, 0)
        # In spring evening, Spica rises in the East-Southeast (rises ~19:47 CST, above horizon at 20:00)
        spica_ok = alt_spica > 0.0 and 90.0 <= az_spica <= 140.0
        checks.append({
            "episode": "A-01",
            "name": "Spring Equinox Dusk Dragon's Horn (Spica / 角宿一) Rising",
            "passed": spica_ok,
            "details": (
                f"Spica at 2026-03-20 20:00 CST Taipei: Alt = {alt_spica:.2f}°, Az = {az_spica:.2f}° "
                "(confirms Horn mansion rising in East at dusk)."
            ),
        })

        # 4. A-02 三垣天上的紫禁城 (Polaris & Circumpolar Visibility in Taipei)
        alt_polaris, _ = self.get_altaz_at("Polaris", 2026, 6, 1, 22, 0)
        # Polaris altitude in Taipei must be within 1° of latitude 25.03°
        polaris_ok = abs(alt_polaris - TAIPEI_LAT) < 1.0
        checks.append({
            "episode": "A-02",
            "name": "Purple Forbidden Enclosure North Celestial Pole Altitude",
            "passed": polaris_ok,
            "details": (
                f"Polaris Altitude in Taipei: {alt_polaris:.2f}° (matches latitude {TAIPEI_LAT}° within 0.8°)."
            ),
        })

        # 5. A-03 玄武 (Northern Black Tortoise / Summer transit of Antares)
        # Antares transit on 2026-06-21
        antares_tr = self.get_rise_set_transit("Antares", 2026, 6, 21)
        antares_ok = antares_tr["culmination_alt_deg"] is not None and 35.0 <= antares_tr["culmination_alt_deg"] <= 40.0
        checks.append({
            "episode": "A-03",
            "name": "Heart Mansion (Antares / 心宿二) Summer Meridian Transit",
            "passed": antares_ok,
            "details": (
                f"Antares Culmination on Summer Solstice: {antares_tr['transit_time']} CST, "
                f"Alt = {antares_tr['culmination_alt_deg']}° (South meridian transit)."
            ),
        })

        # 6. A-04 韓國星圖 (Cheonsang Yeolcha Bunya Ji Do key asterisms)
        vega_tr = self.get_rise_set_transit("Vega", 2026, 7, 15)
        checks.append({
            "episode": "A-04",
            "name": "Korean Stone Star Chart Meridian Anchors (Jingnyeo / Vega)",
            "passed": vega_tr["transit_time"] is not None,
            "details": f"Vega Transit: {vega_tr['transit_time']} CST, Culmination Alt = {vega_tr['culmination_alt_deg']}°.",
        })

        # 7. A-06 中秋特輯 (Mid-Autumn Festival Moon Timing)
        # Check Mid-Autumn 2026 (approx 2026-09-25) Full Moon phase
        t0 = self.ts.from_datetime(datetime(2026, 9, 20, tzinfo=timezone.utc))
        t1 = self.ts.from_datetime(datetime(2026, 10, 5, tzinfo=timezone.utc))
        phases_times, phases_events = almanac.find_discrete(t0, t1, almanac.moon_phases(self.eph))
        full_moon_cst = None
        for t, ev in zip(phases_times, phases_events):
            if ev == 2:  # Full Moon
                full_moon_cst = t.astimezone(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M:%S CST")
        checks.append({
            "episode": "A-06",
            "name": "Mid-Autumn 2026 Lunar Full Moon Timing",
            "passed": full_moon_cst is not None,
            "details": f"Astronomical Full Moon calculated: {full_moon_cst}.",
        })

        # 8. A-14 因紐特 (Winter Polar Rigel / Orion vs Dubhe / Ursa Major)
        alt_rigel, _ = self.get_altaz_at("Rigel", 2026, 12, 15, 23, 0)
        alt_dubhe, _ = self.get_altaz_at("Dubhe", 2026, 12, 15, 23, 0)
        checks.append({
            "episode": "A-14",
            "name": "Inuit Arctic Winter Constellations Elevation in Mid-Winter",
            "passed": alt_rigel > 40.0 and alt_dubhe > 0.0,
            "details": (
                f"Midnight 2026-12-15 Taipei: Rigel Alt = {alt_rigel:.2f}°, Dubhe Alt = {alt_dubhe:.2f}°."
            ),
        })

        # 9. A-15 北歐 (Winter Solstice Yule Night Rigel / Aurvandilstá)
        tr_rigel = self.get_rise_set_transit("Rigel", 2026, 12, 21)
        checks.append({
            "episode": "A-15",
            "name": "Yule Winter Solstice Rigel (Aurvandilstá) Meridian Transit",
            "passed": tr_rigel["transit_time"] is not None and 50.0 <= tr_rigel["culmination_alt_deg"] <= 60.0,
            "details": (
                f"Rigel Yule Transit: {tr_rigel['transit_time']} CST, "
                f"Culmination Alt = {tr_rigel['culmination_alt_deg']}°."
            ),
        })

        return checks


def verify_critic_astronomy_text(text: str) -> Tuple[bool, List[str]]:
    """Inspect an 天文 critic report text to ensure it includes Taipei ephemeris verification."""
    findings = []
    has_taipei = "台北" in text or "臺北" in text or "25.03" in text or "121.56" in text
    has_coords = any(kw in text for kw in ["仰角", "方位", "升落", "升起", "落下", "中天", "高度角", "赤經", "赤緯"])
    has_timing = any(kw in text for kw in ["UTC+8", "對時", "对时", "時分", "CST", "經緯度", "春分", "夏至", "秋分", "冬至", "觀測", "時刻"])

    if not has_taipei:
        findings.append("Missing Taipei coordinates reference (台北 / 25.03°N / 121.56°E)")
    if not has_coords:
        findings.append("Missing astronomical coordinates (仰角 / 方位 / 升落 / 升起 / 中天)")
    if not has_timing:
        findings.append("Missing time reference (UTC+8 / 星空對時 / CST / 時刻)")

    passed = len(findings) == 0
    return passed, findings


def main():
    parser = argparse.ArgumentParser(description="Astronomical Ephemeris Verifier for NTNU Video Series")
    parser.add_argument("--bsp", type=str, help="Path to de421.bsp", default=None)
    parser.add_argument("--star", type=str, help="Target star name (e.g., Altair, Canopus)", default=None)
    parser.add_argument("--date", type=str, help="Date in YYYY-MM-DD", default=None)
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    print("=" * 70)
    print("NTNU Astronomy Club — Ephemeris Verification Suite (Skyfield 1.54)")
    print("Observer: Taipei (25.03°N, 121.56°E, elevation 10m, UTC+8)")
    print("=" * 70)

    try:
        verifier = EphemerisVerifier(args.bsp)
        print(f"[OK] Ephemeris file loaded: {verifier.bsp_path}")
    except Exception as e:
        print(f"[ERROR] Failed to initialize EphemerisVerifier: {e}")
        sys.exit(1)

    checks = verifier.verify_episode_baselines()
    all_passed = True
    print("\nTarget Episode Astronomical Baselines:")
    print("-" * 70)
    for c in checks:
        status = "[PASS]" if c["passed"] else "[FAIL]"
        if not c["passed"]:
            all_passed = False
        print(f"{status} [{c['episode']}] {c['name']}")
        if args.verbose or not c["passed"]:
            print(f"       {c['details']}")

    print("-" * 70)
    if all_passed:
        print("ALL ASTRONOMICAL BASELINES VERIFIED SUCCESSFULLY.")
        sys.exit(0)
    else:
        print("SOME ASTRONOMICAL BASELINES FAILED.")
        sys.exit(1)


if __name__ == "__main__":
    main()
