from types import SimpleNamespace as NS

# Values and expected results as per example in documentation:
#   doc/Manuale API REST KalliopePBX V4 per CDR.pdf

credentials = NS(
    username="admin",
    password="admin",
    domain="default",
    salt="b5a8fdcf2f8d5acdad33c4a072a97d7a",
    created="2016-04-29T15:48:26Z",
    nonce="bfb79078ff44c35714af28b7412a702b",
)

expected = NS(
    digest="+PJg7Tb3v98XnL6iJVv+v5hwhYjdzQ2tIWxvJB2cE40=",
    digest_pass=(
        "dd7b0be7fa37d6cbaf0b842bf7532f22"
        "9cb79ab8d54d509c2aa7eea27a53cd5e"
        ),
    xheader_key="X-authenticate",
    xheader_value=(
        'RestApiUsernameToken Username="admin", Domain="default", '
        'Digest="+PJg7Tb3v98XnL6iJVv+v5hwhYjdzQ2tIWxvJB2cE40=", '
        'Nonce="bfb79078ff44c35714af28b7412a702b", '
        'Created="2016-04-29T15:48:26Z"'
    ),
)

expected.xheader_dict = {expected.xheader_key: expected.xheader_value}
expected.xheader_str = f"{expected.xheader_key}: {expected.xheader_value}"
