import unittest
import os
from eidos.system.config import settings, EidosSettings
from eidos.quant.indicators import RSI, RSIConfig
from pydantic import ValidationError

class TestModernConfig(unittest.TestCase):
    def test_settings_defaults(self):
        self.assertEqual(settings.log_level, "INFO")
        self.assertEqual(settings.default_backend, "polars")
        
    def test_env_override(self):
        # Create a new settings instance with env var overrides
        os.environ["EIDOS_LOG_LEVEL"] = "DEBUG"
        new_settings = EidosSettings()
        self.assertEqual(new_settings.log_level, "DEBUG")
        del os.environ["EIDOS_LOG_LEVEL"]

    def test_indicator_validation(self):
        # Valid
        rsi = RSI(window=14)
        self.assertEqual(rsi.config["window"], 14)
        
        # Invalid (window <= 0)
        with self.assertRaises(ValidationError):
            RSI(window=0)
            
        with self.assertRaises(ValidationError):
            RSI(window=-5)

if __name__ == "__main__":
    unittest.main()
