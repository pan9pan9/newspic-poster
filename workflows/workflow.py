from crawlers.newspick_crawler import NewspickCrawler
from apis.threads_api import ThreadsAPI
import asyncio

# workflows/workflow.py

async def run_workflow(crawler, threads_api, limit=20):
    """
    뉴스픽 기사 크롤링 후 Threads에 업로드 + 링크 댓글 달기
    :param crawler: NewspickCrawler 객체
    :param threads_api: ThreadsAPI 객체
    :param limit: 최대 처리할 기사 개수
    """
    print("👉 뉴스픽 기사 크롤링 시작")
    articles = await crawler.fetch_articles()
    print(f"✅ {len(articles)}개 기사 수집 완료")

    thread_ids = []

    # 1️⃣ 이미지 + 제목 업로드
    for idx, article in enumerate(articles[:limit]):
        print(f"📤 {idx+1}번째 기사 업로드 중: {article['title']}")

        # 미디어 컨테이너 생성
        media_response = threads_api.create_media(
            media_type="IMAGE",
            image_url=article["img"],
            text=article["title"]
        )
        container_id = media_response.get("id")
        if not container_id:
            print(f"⚠️ 미디어 컨테이너 생성 실패: {media_response}")
            continue

        # 미디어 발행
        publish_response = threads_api.publish_media(container_id)
        post_id = publish_response.get("id")
        if not post_id:
            print(f"⚠️ 게시물 발행 실패: {publish_response}")
            continue

        print(f"✅ {idx+1}번째 게시물 업로드 완료, post_id: {post_id}")
        thread_ids.append(post_id)

    print("📝 기사 링크 댓글 달기 시작")
    # 2️⃣ 댓글 달기 (링크)
    for idx, article in enumerate(articles[:limit]):
        if idx >= len(thread_ids):
            print(f"⚠️ 게시물이 생성되지 않아 댓글 생략: {article['title']}")
            continue

        reply_response = threads_api.reply_to_post(thread_ids[idx], article["link"])
        print(f"💬 댓글 달기 응답: {reply_response}")