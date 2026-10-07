import contextlib
import copy
import datetime as dt
import io
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from moteur import engine  # noqa: E402


class EngineContractTests(unittest.TestCase):
    def setUp(self):
        engine.setup_platform("freebuff")

    def load_state(self, platform="freebuff"):
        path = ROOT / "moteur" / "state" / f"{platform}.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def assert_invalid_state(self, state):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                engine.validate(state, expected_platform="freebuff")

    def test_checked_in_states_satisfy_engine_contract(self):
        for platform in ("freebuff", "opencode"):
            with self.subTest(platform=platform):
                engine.setup_platform(platform)
                engine.validate(self.load_state(platform), expected_platform=platform)
        engine.setup_platform("freebuff")

    def test_facts_require_value_and_dated_evidence(self):
        state = self.load_state()
        state["facts"]["unsourced"] = {"value": "claim"}
        self.assert_invalid_state(state)

    def test_price_and_access_combinations_are_coherent(self):
        cases = (
            ("metered", None, None),
            ("paid_only", 5, "FB/h"),
            ("full", 5, "FB/h"),
            ("unknown", 5, "FB/h"),
            ("metered", -1, "FB/h"),
        )
        for access, value, unit in cases:
            with self.subTest(access=access, value=value):
                state = self.load_state()
                model = next(m for m in state["models"] if m["id"] == "solar-pro-4")
                model["access"] = access
                model["price"].update(value=value, unit=unit, promo=False)
                self.assert_invalid_state(state)

    def test_live_model_with_unknown_access_can_remain_unpriced(self):
        state = self.load_state()
        model = next(m for m in state["models"] if m["id"] == "solar-pro-4")
        model["access"] = "unknown"
        model["price"].update(value=None, unit=None, promo=False)
        engine.validate(state, expected_platform="freebuff")

    def test_retired_date_renders_and_parses_with_year(self):
        state = self.load_state()
        model = next(m for m in state["models"] if m["id"] == "space-bunny-alpha")
        retired_at = dt.date.fromisoformat(model["retired_at"])
        cell = engine.render_price_cell(model)
        self.assertEqual(
            cell,
            f"🪦 **retiré {retired_at.day:02d}/{retired_at.month:02d}/{retired_at.year}**",
        )
        parsed = engine.parse_price_cell(cell)
        self.assertEqual(parsed[2:4], ("retired", retired_at.isoformat()))

    def test_legacy_retired_date_without_year_still_parses(self):
        yesterday = dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1)
        cell = f"🪦 **retiré {yesterday.day:02d}/{yesterday.month:02d}**"
        parsed = engine.parse_price_cell(cell)
        self.assertEqual(parsed[3], yesterday.isoformat())

    def test_positive_promo_survives_markdown_round_trip(self):
        state = self.load_state()
        model = copy.deepcopy(next(m for m in state["models"] if m["id"] == "solar-pro-4"))
        model["price"].update(value=5, unit="FB/h", promo=True)
        cell = engine.render_price_cell(model)
        self.assertIn("5 FB/h (promo)", cell)
        parsed = engine.parse_price_cell(cell)
        self.assertEqual(parsed[0], "metered")
        self.assertTrue(parsed[1]["promo"])
        self.assertEqual(parsed[1]["value"], 5)
        self.assertEqual(parsed[1]["unit"], "FB/h")
        self.assertIn("5 FB/h (promo)", engine.render_prix_line(model))

    def test_new_solar_history_uses_previous_recorded_price(self):
        state = self.load_state()
        solar = next(m for m in state["models"] if m["id"] == "solar-pro-4")
        previous = max(
            (engine.parse_datetime(h["at"]), h["to"])
            for h in solar["history"]
            if h["field"] == "price"
        )
        at = (previous[0] + dt.timedelta(seconds=1)).isoformat()
        adapter = {
            "sources": [
                {"type": "solar_promo_ts", "url": "https://example.test/solar.ts"}
            ]
        }
        observation = {
            "solar_changes": [
                {
                    "model": "solar-pro-4",
                    "at": at,
                    "price": 5,
                    "raw_model": "FREEBUFF_SOLAR_PRO_4_MODEL_ID",
                    "tagline": "test",
                }
            ],
            "solar_promo_active": False,
        }
        result = engine.compute_changes(state, observation, adapter)
        history = next(op["entry"] for op in result["auto"] if op["op"] == "history")
        self.assertEqual(history["from"], previous[1])
        self.assertEqual(history["to"], 5)


if __name__ == "__main__":
    unittest.main()
