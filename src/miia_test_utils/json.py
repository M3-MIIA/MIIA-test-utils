import pytest


_NO_DEFAULT = object()


def assert_field(json: dict, field: str, expected_type: type | list[type],
                 default=_NO_DEFAULT):
    """
    Check if the `json` object has the given field and that it is of the
    expected type.

    If a `default` value is given, the field is considered optional and the
    `default` value will be returned if the field is missing from the `json`
    object.
    """

    if default == _NO_DEFAULT:
        assert field in json, f'JSON object missing field "{field}"\nJSON: {json}'

    val = json.get(field, default)

    if isinstance(expected_type, type):
        expected_type = [ expected_type ]

    for t in expected_type:
        if isinstance(val, t):
            return val

    if len(expected_type) > 1:
        msg = expected_type[0].__name__
    else:
        msg = f"one of {', '.join(e.__name__ for e in expected_type)}"

    pytest.fail(
        f"Field {field} {type(val).__name__}, but should be {msg}\nJSON: {json}"
    )


def filter_fields(js: dict, fields):
    """
    Return a new object holding only the fields in `js` passed in the `fields`
    parameter.

    Useful for comparing only a subset of fields returned by an API with the
    expected response when checking the entire response is not the goal of the
    test. This makes this kind of tests less prone to fail due to future new
    fields added to the response or changes in other fields that are not
    relevant for the current test.

    E.g.:
    ```
    def test_score():
        resp = assert_response_status(api.get(…))
        data = resp.json()

        # Check only the score-related fields:
        expected_data = {
            'score': 2.5,
            'max_score': 5.0
        }

        assert filter_fields(data, expected_data) == expected_data
    ```
    """

    out = {}

    for k in fields:
        if k in js:
            out[k] = js[k]

    return out
