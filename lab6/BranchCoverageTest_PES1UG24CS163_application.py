import pytest

from customs_duty import duty_rate, total_duty, clearance_channel


# duty_rate: prohibited and permitted categories
@pytest.mark.parametrize("category", ["weapons", "narcotics"])
def test_prohibited_categories_take_exception_branch(category):
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate(category, "FTA")


@pytest.mark.parametrize(
    ("category", "origin", "expected"),
    [
        ("electronics", "FTA", 0.10),
        ("electronics", "US", 0.20),
        ("clothing", "FTA", 0.05),
        ("clothing", "US", 0.12),
        ("books", "FTA", 0),
        ("furniture", "US", 0.15),
    ],
)
def test_each_duty_rate_decision(category, origin, expected):
    assert duty_rate(category, origin) == expected


# total_duty: negative values, gift exemption and low-value exemption
def test_negative_value_branch():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("electronics", -1, "US", False)


def test_gift_at_exact_exemption_boundary():
    assert total_duty("electronics", 5000, "US", True) == 0


def test_gift_just_above_exemption_boundary():
    assert total_duty("electronics", 5001, "FTA", True) == 50


def test_non_gift_at_exact_low_value_boundary():
    assert total_duty("electronics", 1000, "US", False) == 0


def test_non_gift_above_low_value_boundary():
    assert total_duty("electronics", 2000, "FTA", False) == 200


# Exercise all outcomes of the minimum-duty decision.
def test_duty_between_zero_and_fifty_gets_minimum():
    assert total_duty("clothing", 5100, "FTA", True) == 50


def test_zero_duty_does_not_get_minimum():
    assert total_duty("books", 6000, "US", True) == 0


def test_duty_of_fifty_or_more_is_not_changed():
    assert total_duty("electronics", 6000, "US", True) == 200


def test_prohibited_category_propagates_from_duty_rate():
    with pytest.raises(ValueError, match="prohibited item"):
        total_duty("narcotics", 6000, "US", False)


# clearance_channel: prohibited, high value, missing documents and green.
def test_prohibited_item_is_refused():
    assert clearance_channel(100, "weapons", True) == "refuse"


def test_value_above_100000_is_inspected():
    assert clearance_channel(100001, "electronics", True) == "inspect"


def test_value_at_100000_does_not_take_high_value_branch():
    assert clearance_channel(100000, "electronics", True) == "green"


def test_value_above_20000_without_documents_is_inspected():
    assert clearance_channel(20001, "clothing", False) == "inspect"


def test_value_above_20000_with_documents_is_green():
    assert clearance_channel(20001, "clothing", True) == "green"


def test_value_at_20000_is_green_without_documents():
    assert clearance_channel(20000, "books", False) == "green"
