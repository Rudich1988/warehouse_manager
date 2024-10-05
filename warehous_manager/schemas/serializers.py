from typing_extensions import Annotated
from decimal import Decimal

from pydantic import PlainSerializer


CustomDecimal = Annotated[
    Decimal, PlainSerializer(
        lambda x: float(x),
        return_type=float, when_used='json'
    )
]
