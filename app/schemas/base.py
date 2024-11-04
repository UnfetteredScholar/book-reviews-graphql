from typing import Annotated, Optional

from pydantic import BeforeValidator

PyObjectId = Annotated[Optional[str], BeforeValidator(str)]
