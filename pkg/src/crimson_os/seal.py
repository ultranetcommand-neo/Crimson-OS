"""T112 seal. Integers only. HOLD or FAIL. No epsilon."""
from __future__ import annotations


class Seal:
    T73 = 73 * 74 // 2  # 2701
    JOHN_IOTA_ON = 3627
    JOHN_IOTA_OFF = 3617
    T112 = 112 * 113 // 2  # 6328
    KEY = 54

    @classmethod
    def verify(cls, iota_on: bool = True) -> str:
        john = cls.JOHN_IOTA_ON if iota_on else cls.JOHN_IOTA_OFF
        total = cls.T73 + john
        if total != cls.T112:
            return "FAIL"
        disc = 8 * total + 1
        root = int(disc**0.5)
        if root * root != disc:
            return "FAIL"
        return "HOLD"

    @classmethod
    def lerp_trap(cls) -> float:
        return cls.KEY + 0.5 * (cls.T112 - cls.KEY)
