import pytest

from customs_duty import duty_rate, total_duty, clearance_channel


def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0


def test_electronics_fta_rate():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_non_fta_rate():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta_rate():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_non_fta_rate():
    assert duty_rate("clothing", "US") == 0.12


def test_other_category_rate():
    assert duty_rate("furniture", "US") == 0.15


@pytest.mark.parametrize("category", ["weapons", "narcotics"])
def test_prohibited_items_raise_error(category):
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate(category, "US")


def test_low_value_personal_import():
    assert total_duty("books", 500, "US", False) == 0


def test_negative_value_raises_error():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("electronics", -100, "US", False)


def test_gift_within_exemption_limit():
    assert total_duty("electronics", 5000, "US", True) == 0


def test_gift_above_exemption_limit():
    assert total_duty("electronics", 6000, "FTA", True) == 100


def test_non_gift_above_low_value_limit():
    assert total_duty("electronics", 2000, "FTA", False) == 200


def test_minimum_duty_is_applied():
    assert total_duty("clothing", 5100, "FTA", True) == 50


def test_zero_duty_does_not_get_minimum_applied():
    assert total_duty("books", 6000, "US", True) == 0


def test_prohibited_category_in_total_duty():
    with pytest.raises(ValueError, match="prohibited item"):
        total_duty("weapons", 6000, "US", False)


def test_prohibited_item_is_refused_by_clearance():
    assert clearance_channel(500, "weapons", True) == "refuse"


def test_high_value_item_needs_inspection():
    assert clearance_channel(100001, "electronics", True) == "inspect"


def test_item_without_documents_needs_inspection():
    assert clearance_channel(25000, "clothing", False) == "inspect"


def test_item_with_documents_uses_green_channel():
    assert clearance_channel(25000, "clothing", True) == "green"


def test_low_value_item_uses_green_channel():
    assert clearance_channel(1000, "books", False) == "green"
