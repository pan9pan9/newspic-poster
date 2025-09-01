from workflows.workflow import run_workflow
from crawlers.newspick_crawler import NewspickCrawler
from apis.threads_api import ThreadsAPI
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

crawler = NewspickCrawler(
    user_id=os.getenv("NEWSPICK_ID"),
    password=os.getenv("NEWSPICK_PW"),
)

threads_api = ThreadsAPI(
    access_token=os.getenv("ACCESS_TOKEN"),
    user_id=os.getenv("THREADUSER_ID")
)

asyncio.run(run_workflow(crawler, threads_api))