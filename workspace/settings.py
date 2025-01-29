from pathlib import Path

# Workspace name: only used for naming cloud resources
WS_NAME = "agno-demo-app"

# Path to the workspace root
WS_ROOT = Path(__file__).parent.parent.resolve()

# Environment names
DEV_ENV = "dev"
PRD_ENV = "prd"

# Dev key is used for naming development resources
DEV_KEY = f"{WS_NAME}-{DEV_ENV}"
# Production key is used for naming production resources
PRD_KEY = f"{WS_NAME}-{PRD_ENV}"

# AWS settings
# Region for AWS resources
AWS_REGION = "us-east-1"
# AWS profile for the ai-demos account
AWS_PROFILE = "ai-demos"

# Availability Zones for AWS resources
AWS_AZ1 = "us-east-1a"
AWS_AZ2 = "us-east-1b"

# Subnet IDs in the aws_region
SUBNET_IDS = ["subnet-067b9140c018160f6", "subnet-0f3ba3094301af603"]

# Image Settings
# Repository for images
IMAGE_REPO = "agnohq"

# Build images locally
BUILD_IMAGES = True
