import pytest
from react_generator.naming import to_pascal_case, to_camel_case, format_name


@pytest.mark.parametrize("raw, expected", [
    ("button",         "Button"),
    ("myComponent",    "MyComponent"),
    ("my-cool_widget", "MyCoolWidget"),
    ("Button2",        "Button2"),        # bug historique : ne doit PLUS perdre le 2
    ("v2Modal",        "V2Modal"),
    ("user2Profile",   "User2Profile"),
    ("",               ""),
])
def test_pascal(raw, expected):
    assert to_pascal_case(raw) == expected


@pytest.mark.parametrize("raw, expected", [
    ("MyWidget", "myWidget"),
    ("button",   "button"),
    ("",         ""),
])
def test_camel(raw, expected):
    assert to_camel_case(raw) == expected


@pytest.mark.parametrize("raw, kind, expected", [
    ("counter",      "hook",      ("useCounter",   "Counter", "counter")),
    ("useCounter",   "hook",      ("useCounter",   "Counter", "counter")),  # préfixe déjà là
    ("data",         "service",   ("DataService",  "Data",    "data")),
    ("DataService",  "service",   ("DataService",  "Data",    "data")),     # suffixe déjà là
    ("House",        "service",   ("HouseService", "House",   "house")),    # piège: contient "use"
    ("user",         "context",   ("UserContext",  "User",    "user")),
    ("counter",      "redux",     ("counterSlice", "Counter", "counter")),
    ("counterSlice", "redux",     ("counterSlice", "Counter", "counter")),
    ("button",       "component", ("Button",       "Button",  "button")),
])
def test_format_name(raw, kind, expected):
    assert format_name(raw, kind) == expected