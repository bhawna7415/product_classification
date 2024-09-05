import logging
from enum import Enum

from os import environ
from dotenv import load_dotenv
from constants import EnvironmentEnum

# Load environment variables from .env file
load_dotenv(dotenv_path=".env", verbose=True)

# Serverless
SLS_STACK_NAME = environ.get("SLS_STACK_NAME")

# Core App Settings
APP_NAME = environ.get("APP_NAME", "kintsugi-product-classification")

# Environment Settings
ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.to_enum(
    environ.get("ENVIRONMENT", "dev")
)
ENV_IS_PROD: bool = ENVIRONMENT == EnvironmentEnum.PROD
ENV_IS_LOCAL: bool = ENVIRONMENT in [
    EnvironmentEnum.LOCAL,
    EnvironmentEnum.TEST,
]
ENV_IS_DEV: bool = ENVIRONMENT == EnvironmentEnum.DEV

# OPENAI Config
OPENAI_API_KEY = environ.get("OPENAI_API_KEY", "sk_test")

# MODEL Config
MODEL_NAME = environ.get("MODEL_NAME", "ft:gpt-3.5-turbo-0613:kintsugi::8pa5WI2v")

# Logging configuration
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Sentry initialization
def init_sentry():
    """Initialize Sentry SDK. Sentry is only initialized for deployed environments."""
    if ENVIRONMENT in [
        EnvironmentEnum.TEST,
        EnvironmentEnum.LOCAL,
    ]:
        return

    import sentry_sdk
    from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

    sample_rate = 0.2 if ENV_IS_PROD else 0.1

    sentry_sdk.init(
        dsn="https://aed50300b3b805cda9f531f9cc0c4860@o4505647854583808.ingest.us.sentry.io/4506900105854976",
        environment=ENVIRONMENT.value,
        traces_sample_rate=sample_rate,
        integrations=[
            AwsLambdaIntegration(timeout_warning=True),
        ],
    )
