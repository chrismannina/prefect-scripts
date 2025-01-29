"""
Quick Prefect Deployment Script
------------------------------

PREREQUISITES:
1. Make sure your Prefect environment variables are set. Either:
   - Source the environment variables:
     $ source set_prefect_env.sh
   OR
   - Export them directly:
     $ export PREFECT_API_URL="your-api-url"
     $ export PREFECT_API_KEY="your-api-key"

2. Edit the variables below to configure your deployment

3. Run the script:
   $ python quick_deploy.py

Note: The SCHEDULE variable uses cron syntax. Common patterns:
- "0 9 * * *"        = Daily at 9 AM
- "0 9 * * 1-5"      = Weekdays at 9 AM
- "0 */2 * * *"      = Every 2 hours
- "0 9-17 * * 1-5"   = Hourly 9 AM-5 PM on weekdays
"""

##################### EDIT THESE VARIABLES #####################
# Required
FLOW_PATH = "genai/src/orchestration/workqueues/prior_auth/flows/cmm_check_status_flow.py"
FLOW_NAME = "cmm_status_check_flow"
DEPLOYMENT_NAME = "cmm-status-check"

# Optional (comment out or set to None if not needed)
WORK_POOL = "genai Pool"
WORK_QUEUE = "queue_processing"
SCHEDULE = "0 8-18 * * 1-5"  # Cron expression (this example: 8am-6pm on weekdays)
TAGS = ["prod", "prior_auth", "cmm"]  # List of tags

##################### DEPLOYMENT SCRIPT #####################
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

def create_deployment():
    # Build deployment parameters
    deployment_params = {
        "flow_path": FLOW_PATH,
        "name": DEPLOYMENT_NAME,
    }

    # Add optional parameters if specified
    if WORK_POOL:
        deployment_params["work_pool_name"] = WORK_POOL
    if WORK_QUEUE:
        deployment_params["work_queue_name"] = WORK_QUEUE
    if SCHEDULE:
        deployment_params["schedule"] = CronSchedule(cron=SCHEDULE, timezone="America/Detroit")
    if TAGS:
        deployment_params["tags"] = TAGS

    # Create and apply deployment
    deployment = Deployment.build_from_flow(**deployment_params)
    deployment.apply()

    # Print success message
    print("\n✨ Deployment created successfully!")
    print(f"   Flow: {FLOW_NAME}")
    print(f"   Deployment: {DEPLOYMENT_NAME}")
    print(f"   Work Pool: {WORK_POOL}")
    if WORK_QUEUE:
        print(f"   Work Queue: {WORK_QUEUE}")
    if SCHEDULE:
        print(f"   Schedule: {SCHEDULE}")
    if TAGS:
        print(f"   Tags: {', '.join(TAGS)}")

if __name__ == "__main__":
    create_deployment()
