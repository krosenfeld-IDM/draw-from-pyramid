from pathlib import Path
import unittest
from pyramid_alias import AliasedDistribution
from pyramid_alias import load_pyramid_csv


class TestAliasedDistribution(unittest.TestCase):
    script_dir = Path(__file__).parent.absolute()
    def test_pyramid_alias_USA(self):
        """Test the AliasedDistribution class with USA data."""
        file = self.script_dir / "data" / "United States of America-2023.csv"
        pyramid = load_pyramid_csv(file, quiet=True)
        alias = AliasedDistribution(pyramid[:,4])
        assert alias

    def test_pyramid_alias_Nigeria(self):
        """Test the AliasedDistribution class with Nigeria data."""
        file = self.script_dir / "data" / "Nigeria-2023.csv"
        pyramid = load_pyramid_csv(file, quiet=True)
        alias = AliasedDistribution(pyramid[:,4])
        assert alias

    def test_pyramid_alias_Africa(self):
        """Test the AliasedDistribution class with Africa data."""
        file = self.script_dir / "data" / "AFRICA-2023.csv"
        pyramid = load_pyramid_csv(file, quiet=True)
        alias = AliasedDistribution(pyramid[:,4])
        assert alias

if __name__ == '__main__':
    unittest.main()
