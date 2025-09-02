import asyncio
import logging
from playwright.async_api import async_playwright
from crawlers.locators import LoginPageLocators, ArticlePageLocators

# 로깅 설정
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class NewspickCrawler:
    def __init__(self, user_id: str, password: str):
        self.user_id = user_id
        self.password = password

    async def fetch_articles(self, limit: int = 20):
        async with async_playwright() as p:
            logger.info("🌐 브라우저 실행")
            browser = await p.chromium.launch(headless=True)

            context = await browser.new_context(
                permissions=["clipboard-read", "clipboard-write"]
            )
            page = await context.new_page()
            page.on("dialog", lambda dialog: dialog.accept())

            # 로그인
            logger.info("🔑 로그인 시도")
            await page.goto("https://partners.newspic.kr/main/index")
            await page.fill(LoginPageLocators.ID_INPUT, self.user_id)
            await page.fill(LoginPageLocators.PASSWORD_INPUT, self.password)
            await page.click(LoginPageLocators.LOGIN_BUTTON)
            await page.wait_for_timeout(3000)
            logger.info(f"✅ 로그인 완료, 현재 URL: {page.url}")

            # 이미지 로딩
            try:
                await page.wait_for_selector(ArticlePageLocators.IMAGE, timeout=10000)
            except:
                logger.warning("⚠️ 이미지 요소를 찾을 수 없음")
                await browser.close()
                return []

            # 이미지 목록
            img_elements = await page.locator(ArticlePageLocators.IMAGE).all()
            logger.info(f"🔍 이미지 요소 개수: {len(img_elements)}")
            img_src_list = await page.locator(ArticlePageLocators.IMAGE).evaluate_all(
                "imgs => imgs.map(img => img.src)"
            )
            img_src_list = img_src_list[1:limit+1]

            # 제목 목록
            title_elements = await page.locator(ArticlePageLocators.TITLE).all_inner_texts()
            logger.info(f"🔍 제목 요소 개수: {len(title_elements)}")
            title_list = [
                t.replace(" …", "").replace("'", " ").replace('"', " ")
                for t in title_elements[1:limit+1]
            ]

            # 버튼 목록
            buttons = await page.locator(ArticlePageLocators.COPY_BUTTON).all()
            thumbs = await page.locator(ArticlePageLocators.THUMB).all()
            logger.info(f"🔍 버튼 요소 개수: {len(buttons)}")

            links = []
            for idx, button in enumerate(buttons[:limit]):
                await thumbs[idx].hover()
                await page.mouse.down()
                await button.click()
                await page.wait_for_timeout(1000)
                await page.mouse.up()

                copied_link = await page.evaluate("""
                    (async () => {
                        try {
                            const text = await navigator.clipboard.readText();
                            return text;
                        } catch (err) {
                            console.error('클립보드 읽기 실패: ', err);
                            return null;
                        }
                    })()
                """)
                links.append(copied_link)
                print(f"🔗 {idx+1}번째 링크 수집: {copied_link}")
                logger.info(f"🔗 {idx+1}번째 링크 수집: {copied_link}")

            await browser.close()
            logger.info("🌐 브라우저 종료")

        return [
            {"title": t, "img": i, "link": l}
            for t, i, l in zip(title_list, img_src_list, links)
        ]