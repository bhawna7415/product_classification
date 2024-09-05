from enum import Enum


class ProductType(Enum):
    SUBSCRIPTION = "SUBSCRIPTION"
    CHARGE = "CHARGE"

class EnvironmentEnum(Enum):
    PROD = "prod"
    DEV = "dev"
    LOCAL = "local"
    TEST = "test"

    @classmethod
    def to_enum(cls, environment: str) -> "EnvironmentEnum":
        return cls(environment.lower())