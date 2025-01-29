from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from prefect.client import get_client
import asyncio

# Make sure to set the Prefect credentials in the set_prefect_env.sh script
# Run the set_prefect_env.sh script before running this script

async def list_pools_and_queues():
    async with get_client() as client:
        # Get work pools
        work_pools = await client.read_work_pools()
        print("\nAvailable Work Pools:")
        for pool in work_pools:
            print(f"- Name: {pool.name}")
            print(f"  ID: {pool.id}")
            print(f"  Type: {pool.type}")
            
        # Get work queues for each pool
        for pool in work_pools:
            queues = await client.read_work_queues(pool.name)
            if queues:
                print(f"\nQueues in {pool.name}:")
                for queue in queues:
                    print(f"- {queue.name}")

# Run the async function to list pools and queues
asyncio.run(list_pools_and_queues())
