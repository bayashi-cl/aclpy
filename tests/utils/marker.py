import pytest

# assert(false)はc-extension内でabortされるのでtry ~ exceptで検知できない
skip_cppassert = pytest.mark.skip(reason="cannot determine c++ assert")
