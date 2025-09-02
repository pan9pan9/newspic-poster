import logging
from crawlers.newspick_crawler import NewspickCrawler
from apis.threads_api import ThreadsAPI
import asyncio

# 로깅 설정
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

async def run_workflow(crawler, threads_api, limit=20):
    logger.info("👉 뉴스픽 기사 크롤링 시작")
    articles = await crawler.fetch_articles()
    logger.info(f"✅ {len(articles)}개 기사 수집 완료")

    thread_ids = []

    # 1️⃣ 이미지 + 제목 업로드
    for idx, article in enumerate(articles[:limit]):
        logger.info(f"📤 {idx+1}번째 기사 업로드 중")

        media_response = threads_api.create_media(
            media_type="IMAGE",
            image_url=article["img"],
            text=article["title"]
        )
        container_id = media_response.get("id")
        if not container_id:
            logger.warning(f"⚠️ 미디어 컨테이너 생성 실패: {media_response}")
            continue

        publish_response = threads_api.publish_media(container_id)
        post_id = publish_response.get("id")
        if not post_id:
            logger.warning(f"⚠️ 게시물 발행 실패: {publish_response}")
            continue

        logger.info(f"✅ {idx+1}번째 게시물 업로드 완료, post_id: {post_id}")
        thread_ids.append(post_id)

    logger.info("📝 기사 링크 댓글 달기 시작")

    # 2️⃣ 댓글 달기
    for idx, article in enumerate(articles[:limit]):
        if idx >= len(thread_ids):
            logger.warning(f"⚠️ 게시물이 생성되지 않아 댓글 생략: {article['title']}")
            continue

        reply_container = threads_api.create_media(
            media_type="TEXT",
            text=article["link"],
            reply_to_id=thread_ids[idx]
        )
        container_id = reply_container.get("id")
        if not container_id:
            logger.warning(f"⚠️ 댓글 컨테이너 생성 실패: {reply_container}")
            continue

        publish_reply = threads_api.publish_media(container_id)
        reply_id = publish_reply.get("id")
        if reply_id:
            logger.info(f"💬 댓글 발행 완료: {reply_id}")
        else:
            logger.warning(f"⚠️ 댓글 발행 실패: {article['title']}")