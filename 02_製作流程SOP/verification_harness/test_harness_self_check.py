# -*- coding: utf-8 -*-
"""test_harness_self_check.py - Comprehensive Unit & Fixture Self-Test Suite.

Validates the internal logic of the verification harness using positive and
negative synthetic fixtures, boundary conditions, and adversarial inputs.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from verify_ephemeris import EphemerisVerifier, verify_critic_astronomy_text
from verify_schemas import (
    count_english_words,
    count_chinese_syllables,
    count_chinese_card_chars,
    strip_markdown,
    validate_research_file,
    validate_critic_file,
    validate_english_draft_file,
    validate_glossary_csv,
)
from verify_sync import compute_sha256


class TestTokenizersAndCounters(unittest.TestCase):
    """Test text parsing, word counting, and syllable counting."""

    def test_english_word_counter_basic(self):
        self.assertEqual(count_english_words("One sky. The Chinese saw — a dragon."), 7)
        self.assertEqual(count_english_words("Hello world!"), 2)
        self.assertEqual(count_english_words(""), 0)
        self.assertEqual(count_english_words("-"), 0)

    def test_english_word_counter_contractions_and_hyphens(self):
        # "don't" is 1 word, "twenty-eight" is 1 word
        self.assertEqual(count_english_words("They don't know twenty-eight asterisms."), 5)

    def test_english_word_counter_unicode_diacritics_and_okina(self):
        # Arabic transliteration with macrons and ayn: Al-Thurayyā, al-Wasm, al-Murabbaʿāniyya
        text = "Al-Thurayyā rises before al-Wasm and al-Murabbaʿāniyya."
        self.assertEqual(count_english_words(text), 6)

        # Polynesian with okina and macron: ʻOkina, Māori
        text_poly = "The Māori navigators used ʻokina and kahakō."
        self.assertEqual(count_english_words(text_poly), 7)

        # Old Norse: Úlfs kjaptr
        text_norse = "Úlfs kjaptr in the night sky."
        self.assertEqual(count_english_words(text_norse), 6)

    def test_english_markdown_stripping(self):
        text = "**One sky.** The *Chinese* saw — `Xin`, [the Heart](http://example.com)."
        self.assertEqual(count_english_words(text), 8)

    def test_chinese_syllable_counter(self):
        # Punctuation does not count as spoken syllables
        vo = "同一片星空，東夷看見——青龍。"
        # 同(1) 一(1) 片(1) 星(1) 空(1) 東(1) 夷(1) 看(1) 見(1) 青(1) 龍(1) = 11 ideographs
        self.assertEqual(count_chinese_syllables(vo), 11)

        # Mixed Chinese and English
        mixed = "在 2026 年觀測 Vega 與 Altair"
        # 在(1), 2026(1), 年(1), 觀(1), 測(1), Vega(1), 與(1), Altair(1) = 8
        self.assertEqual(count_chinese_syllables(mixed), 8)

    def test_chinese_card_chars(self):
        self.assertEqual(count_chinese_card_chars("「角宿一・大角星」"), 6)
        self.assertEqual(count_chinese_card_chars("這是一張長度剛好十四字的字卡"), 14)
        self.assertEqual(count_chinese_card_chars("這是一張超過十四個字非常長非常長的字卡啊"), 20)


class TestAstronomicalEphemerisLogic(unittest.TestCase):
    """Test astronomical ephemeris algorithms with Skyfield."""

    @classmethod
    def setUpClass(cls):
        cls.verifier = EphemerisVerifier()

    def test_qixi_astronomy_separation_and_3d_distance(self):
        qixi = self.verifier.compute_qixi_astronomy(2026, 8, 19)
        # Separation between Vega and Altair is ~34.2°
        self.assertAlmostEqual(qixi["vega_altair_angular_separation_deg"], 34.2, delta=0.5)
        # True 3D distance is ~14.6 ly (often cited as 15-16 ly)
        self.assertAlmostEqual(qixi["vega_altair_true_distance_ly"], 14.63, delta=0.5)
        # Altair transit is in the evening ~21:54 CST
        self.assertTrue(qixi["altair_transit_time"].startswith("21:54"))
        # Culmination altitude ~73.9°
        self.assertAlmostEqual(qixi["altair_culmination_alt_deg"], 73.91, delta=0.5)

    def test_canopus_elevation_in_taiwan(self):
        taipei_alt = self.verifier.compute_canopus_max_elevation(25.033)
        kaohsiung_alt = self.verifier.compute_canopus_max_elevation(22.62)
        # Matches script A-13 assertions: Taipei 12.3°, Kaohsiung 14.7°
        self.assertAlmostEqual(taipei_alt, 12.27, delta=0.1)
        self.assertAlmostEqual(kaohsiung_alt, 14.68, delta=0.1)

    def test_critic_astronomy_text_verification(self):
        good_text = "台北（25.03°N, 121.56°E, UTC+8）星空對時經算，織女星中天仰角 76.2°，升落時間無誤。"
        ok, findings = verify_critic_astronomy_text(good_text)
        self.assertTrue(ok)
        self.assertEqual(len(findings), 0)

        bad_text = "這個逐字稿整體很棒，天文名詞都很優雅。"
        ok2, findings2 = verify_critic_astronomy_text(bad_text)
        self.assertFalse(ok2)
        self.assertTrue(len(findings2) >= 2)


class TestMarkdownSchemaValidators(unittest.TestCase):
    """Test validator logic against valid and invalid synthetic fixtures."""

    def test_research_report_valid(self):
        content = """# A-01 網路考據

## 一、待查核清單逐條結果
| # | 原主張 | 判定（✓ 證實／✗ 錯誤／⚠ 部分正確或需限定／？ 無法證實） | 查到的正確說法 | 出處（網址或書目＋頁碼） | 建議改寫（旁白要口語、短句） |
| 1 | 蚌塑龍虎距今 6500 年 | ✓ 證實 | 濮陽西水坡 M45 墓葬碳十四測年約前 4500 年 | 馮時《中國天文考古學》頁 120 | 距今六千五百年前的濮陽墓葬 |

## 二、清單以外發現的問題
| # | 原主張 | 判定（✓ 證實／✗ 錯誤／⚠ 部分正確或需限定／？ 無法證實） | 查到的正確說法 | 出處（網址或書目＋頁碼） | 建議改寫（旁白要口語、短句） |
| 1 | 東夷是青龍的主人 | ⚠ 部分正確或需限定 | 僅為部分學者推論，古籍無直接記載 | 顧頡剛《古史辨》第三冊 | 一說東夷部落崇拜龍 |

## 三、可以加進影片的好材料
- 1987 年濮陽西水坡出土時，考古學家驚訝發現龍虎方位與現代星圖一致。

## 四、參考資料總表
1. 馮時《中國天文考古學》，中國社會科學出版社，2001。
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name
        try:
            res = validate_research_file(temp_path)
            self.assertTrue(res.passed, f"Errors: {res.errors}")
            self.assertEqual(res.metrics["claims_audited"], 2)
        finally:
            os.remove(temp_path)

    def test_research_report_missing_section(self):
        content = """# A-01 網路考據

## 一、待查核清單逐條結果
| # | 原主張 | 判定（✓ 證實／✗ 錯誤／⚠ 部分正確或需限定／？ 無法證實） | 查到的正確說法 | 出處（網址或書目＋頁碼） | 建議改寫（旁白要口語、短句） |
| 1 | 測試主張 | ✓ 證實 | 正確說法 | 參考出處 | 建議改寫 |

## 二、清單以外發現的問題
## 三、可以加進影片的好材料
"""
        # Missing Section 4: ## 四、參考資料總表
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name
        try:
            res = validate_research_file(temp_path)
            self.assertFalse(res.passed)
            self.assertTrue(any("四、參考資料總表" in err for err in res.errors))
        finally:
            os.remove(temp_path)

    def test_critic_report_valid(self):
        content = """# A-01 審稿意見

整體評價：整體節奏流暢，四象青龍的文化意涵深刻。
最重要的三個問題：(1) 角宿一升起時刻需標明台北時間；(2) 歲差影響未說明；(3) 結尾預告缺少下一集名稱。
沒把握的地方：龍抬頭的二月二民俗確切起源年代。

| 嚴重度（🔴必改／🟡建議／⚪可選） | 位置（鏡號或段落） | 原文 | 問題 | 建議改法 | 依據 |
| 🔴 必改 | 鏡 3 | 角宿一在春分傍晚升起 | 未註明台北經緯度與對時 | 台北春分傍晚八點，角宿一由東偏南升起 | Skyfield 25.03°N, 121.56°E 經算 |
| 🟡 建議 | 鏡 7 | 二萬五千年前 | 應為二萬五千八百年歲差週期 | 二萬六千年歲差週期 | 天文學基礎手冊 |
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name
        try:
            res = validate_critic_file(temp_path, role="天文")
            self.assertTrue(res.passed, f"Errors: {res.errors}")
            self.assertEqual(res.metrics["criticisms"], 2)
            self.assertEqual(res.metrics["severity"]["🔴"], 1)
            self.assertEqual(res.metrics["severity"]["🟡"], 1)
        finally:
            os.remove(temp_path)

    def test_critic_report_missing_summary(self):
        content = """# A-01 審稿意見

| 嚴重度（🔴必改／🟡建議／⚪可選） | 位置（鏡號或段落） | 原文 | 問題 | 建議改法 | 依據 |
| 🔴 必改 | 鏡 1 | 原文 | 問題 | 建議改法 | 依據 |
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name
        try:
            res = validate_critic_file(temp_path, role="敘事")
            self.assertFalse(res.passed)
            self.assertTrue(any("3-line summary" in err for err in res.errors))
        finally:
            os.remove(temp_path)

    def test_english_draft_valid(self):
        content = """# A-01 English Adaptation Draft

## 1. Shot Table
| Shot | Sec | Voice-over | On-screen text | Words/sec |
| 1 | 5.0 | One sky. The Chinese saw — an azure dragon. | Azure Dragon | 1.6 |
| 2 | 8.0 | In early spring, the dragon's horn rises in the East. | Horn Asterism | 1.25 |
| 3 | 10.0 | Tonight, look above Taipei and see the ancient sky. | Spring Sky | 0.9 |

## 2. Totals / Summary
- Total seconds: 23.0s
- Total words: 27 words
- Average pace: 1.17 words/sec

## 3. Glossary Table
| Chinese | English used | Notes |
| 青龍 | Azure Dragon | Traditional Chinese constellation guardian |
| 角宿 | Horn | Asterism in Virgo |

## 4. Social Platform Metadata
- YouTube Title: The Azure Dragon: China's Ancient Celestial Dragon
- YouTube Description: Discover the Azure Dragon of Chinese astronomy. Sources: Han Sky.
- Facebook Caption: One sky, many cultures. Tonight we explore the Azure Dragon.

## 5. Cut & Semantic Adjustment Log
- Shot 4 from Chinese v1 was trimmed to preserve pace under 180s.
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = f.name
        try:
            res = validate_english_draft_file(temp_path)
            self.assertTrue(res.passed, f"Errors: {res.errors}")
            self.assertEqual(res.metrics["total_seconds"], 23.0)
            self.assertEqual(res.metrics["total_words"], 27)
        finally:
            os.remove(temp_path)

    def test_english_draft_boundary_exceed_limits(self):
        # 1. Test total seconds > 180s
        content_181s = """# A-01 English Draft
## 1. Shot Table
| Shot | Sec | Voice-over | On-screen text | Words/sec |
| 1 | 181.0 | One sky. The Chinese saw — a dragon. | Azure Dragon | 0.04 |
## 2. Totals
Total: 181s
## 3. Glossary
| Chinese | English used | Notes |
| a | b | c |
## 4. Social
YouTube Title: Valid Title
Description: valid
Facebook: valid
## 5. Cut Log
none
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content_181s)
            temp_path = f.name
        try:
            res = validate_english_draft_file(temp_path)
            self.assertFalse(res.passed)
            self.assertTrue(any("exceeds hard limit of 180 seconds" in err for err in res.errors))
        finally:
            os.remove(temp_path)

        # 2. Test speech rate > 2.6 words/sec
        content_fast = """# A-01 English Draft
## 1. Shot Table
| Shot | Sec | Voice-over | On-screen text | Words/sec |
| 1 | 2.0 | One sky. The Chinese saw — a dragon rising high above the northern eastern mountains now. | Dragon | 7.0 |
## 2. Totals
Total: 2s
## 3. Glossary
| Chinese | English used | Notes |
| a | b | c |
## 4. Social
YouTube Title: Valid Title
Description: valid
Facebook: valid
## 5. Cut Log
none
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content_fast)
            temp_path = f.name
        try:
            res = validate_english_draft_file(temp_path)
            self.assertFalse(res.passed)
            self.assertTrue(any("Speech rate" in err for err in res.errors))
        finally:
            os.remove(temp_path)

        # 3. Test on-screen card text > 6 English words
        content_long_card = """# A-01 English Draft
## 1. Shot Table
| Shot | Sec | Voice-over | On-screen text | Words/sec |
| 1 | 5.0 | One sky. The Chinese saw — a dragon. | This is an extremely long graphic text card that exceeds six words | 1.4 |
## 2. Totals
Total: 5s
## 3. Glossary
| Chinese | English used | Notes |
| a | b | c |
## 4. Social
YouTube Title: Valid Title
Description: valid
Facebook: valid
## 5. Cut Log
none
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content_long_card)
            temp_path = f.name
        try:
            res = validate_english_draft_file(temp_path)
            self.assertFalse(res.passed)
            self.assertTrue(any("exceeds limit of 6" in err for err in res.errors))
        finally:
            os.remove(temp_path)

        # 4. Test YouTube title > 60 chars
        content_long_title = """# A-01 English Draft
## 1. Shot Table
| Shot | Sec | Voice-over | On-screen text | Words/sec |
| 1 | 5.0 | One sky. The Chinese saw — a dragon. | Azure Dragon | 1.4 |
## 2. Totals
Total: 5s
## 3. Glossary
| Chinese | English used | Notes |
| a | b | c |
## 4. Social
YouTube Title: This Is An Extremely Long YouTube Title That Clearly Exceeds The Maximum Limit Of Sixty Characters
Description: valid
Facebook: valid
## 5. Cut Log
none
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content_long_title)
            temp_path = f.name
        try:
            res = validate_english_draft_file(temp_path)
            self.assertFalse(res.passed)
            self.assertTrue(any("YouTube title length" in err for err in res.errors))
        finally:
            os.remove(temp_path)


class TestGlossaryCsvValidator(unittest.TestCase):
    """Test CSV validation logic."""

    def test_glossary_csv_valid(self):
        content = """Chinese,English,Category,Episode,Notes
青龍,Azure Dragon,Asterism,A-01,Eastern guardian
角宿,Horn,Asterism,A-01,First mansion of Azure Dragon
心宿二,Antares,Star,A-01,Alpha Scorpii
河鼓二,Altair,Star,H-七夕,Alpha Aquilae
織女一,Vega,Star,H-七夕,Alpha Lyrae
天津四,Deneb,Star,H-七夕,Alpha Cygni
老人星,Canopus,Star,A-13,Alpha Carinae
Suhail,Suhail,Arabic Star,A-13,Arabic name for Canopus
al-Thurayyā,al-Thurayyā,Arabic Asterism,A-13,Pleiades in Arabic
Aagjuuk,Aagjuuk,Inuit Asterism,A-14,Altair and Tarazed
Aurvandilstá,Aurvandilstá,Norse Star,A-15,Toe of Aurvandil / Rigel
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".csv", delete=False) as f:
            f.write(content)
            temp_path = f.name
        try:
            res = validate_glossary_csv(temp_path)
            self.assertTrue(res.passed, f"Errors: {res.errors}")
            self.assertEqual(res.metrics["total_terms"], 11)
        finally:
            os.remove(temp_path)

    def test_glossary_csv_empty(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".csv", delete=False) as f:
            f.write("")
            temp_path = f.name
        try:
            res = validate_glossary_csv(temp_path)
            self.assertFalse(res.passed)
            self.assertTrue(any("empty" in err for err in res.errors))
        finally:
            os.remove(temp_path)


def run_self_tests() -> bool:
    """Run all self tests and return True if successful."""
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_self_tests()
    sys.exit(0 if success else 1)
