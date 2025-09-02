import os
import asyncio
import logging
from crawlers.newspick_crawler import NewspickCrawler
from apis.threads_api import ThreadsAPI
from workflows.workflow import run_workflow

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# 2️⃣ 환경변수 가져오기
NEWSPICK_ID = os.getenv("NEWSPICK_ID")
NEWSPICK_PW = os.getenv("NEWSPICK_PW")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
THREADUSER_ID = os.getenv("THREADUSER_ID")

# 1️⃣ 환경변수가 없으면 .env 로드 (로컬용)
if not all(os.getenv(var) for var in ["NEWSPICK_ID", "NEWSPICK_PW", "ACCESS_TOKEN", "THREADUSER_ID"]):
    try:
        from dotenv import load_dotenv
        load_dotenv()
        logger.info("✅ .env 파일 로드 완료 (로컬 실행)")
    except ImportError:
        logger.warning("⚠️ python-dotenv 미설치, .env 파일 로드 불가")



# 3️⃣ 객체 생성
crawler = NewspickCrawler(user_id=NEWSPICK_ID, password=NEWSPICK_PW)
threads_api = ThreadsAPI(access_token=ACCESS_TOKEN, user_id=THREADUSER_ID)

logger.info("🚀 Workflow 시작")
try:
    asyncio.run(run_workflow(crawler, threads_api, limit=20))
    logger.info("✅ Workflow 완료")
except Exception as e:
    logger.exception(f"❌ Workflow 실행 중 오류 발생: {e}")