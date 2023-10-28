from typing import Optional

from .base import Base
from .config import StripeConfig
from .direct import Stripe
from .tiny import Tiny


def stripe_from_config(config: Optional[StripeConfig]) -> Optional[Base]:
    if config is None:
        return None
    elif config.pin >= 0:
        return Stripe(config)
    elif config.bus >= 0:
        return Tiny(config)
    else:
        raise RuntimeError('invalid config')
