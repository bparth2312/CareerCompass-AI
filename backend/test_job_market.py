import asyncio

from app.job_market_client import (
    analyze_live_job_market
)


async def main():
    result = await analyze_live_job_market(
        role="HR Generalist",
        location="Mumbai"
    )

    print(result)


asyncio.run(main())