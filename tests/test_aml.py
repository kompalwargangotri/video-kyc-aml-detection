import numpy as np

from backend import aml


class FakeModel:
    def __init__(self, score):
        self.score = score

    def decision_function(self, features):
        assert features.shape == (1, 6)
        return np.array([self.score])


def test_normal_transaction_is_allowed(monkeypatch):
    monkeypatch.setattr(aml, "model", FakeModel(-0.4))

    result = aml.check_aml(
        amount=1000,
        old_balance=50000,
        new_balance=49000,
        transaction_date="2026-07-13T12:00:00",
        transaction_type=3,
    )

    assert result["status"] == "ALLOW"
    assert result["risk_score"] == 10.0
    assert result["transaction_type"] == 3


def test_night_transaction_requires_review(monkeypatch):
    monkeypatch.setattr(aml, "model", FakeModel(-0.4))

    result = aml.check_aml(
        amount=1000,
        old_balance=50000,
        new_balance=49000,
        transaction_date="2026-07-13T02:00:00",
        transaction_type=3,
    )

    assert result["status"] == "REVIEW"
    assert result["risk_score"] == 72
    assert "UNUSUAL_HOUR" in result["reason_codes"]


def test_large_transaction_is_blocked(monkeypatch):
    monkeypatch.setattr(aml, "model", FakeModel(-0.4))

    result = aml.check_aml(
        amount=250000,
        old_balance=300000,
        new_balance=50000,
        transaction_date="2026-07-13T12:00:00",
        transaction_type=3,
    )

    assert result["status"] == "BLOCK"
    assert result["risk_score"] == 95
    assert "AMOUNT_SPIKE" in result["reason_codes"]
    assert "RULE_LIMIT_BREACH" in result["reason_codes"]