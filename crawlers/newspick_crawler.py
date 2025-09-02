import asyncio
from playwright.async_api import async_playwright
from locators import LoginPageLocators, ArticlePageLocators


class NewspickCrawler:
    def __init__(self, user_id: str, password: str):
        self.user_id = user_id
        self.password = password

    async def fetch_articles(self, limit: int = 20):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            page.on("dialog", lambda dialog: dialog.accept())
            
            context = await browser.new_context(
                permissions=["clipboard-read", "clipboard-write"]
            )
            
            # 로그인
            await page.goto("https://partners.newspic.kr/main/index")
            await page.fill(LoginPageLocators.ID_INPUT, self.user_id)
            await page.fill(LoginPageLocators.PASSWORD_INPUT, self.password)
            await page.click(LoginPageLocators.LOGIN_BUTTON)
            await asyncio.sleep(3)
            
            # 이미지 목록
            img_src_list = await page.locator(ArticlePageLocators.IMAGE).evaluate_all(
                "imgs => imgs.map(img => img.src)"
            )
            img_src_list = img_src_list[1:limit+1]  # 첫 번째 제거 + 제한 적용

            # 제목 목록
            title_list = await page.locator(ArticlePageLocators.TITLE).all_inner_texts()
            title_list = [
                t.replace(" …", "").replace("'", " ").replace('"', " ")
                for t in title_list[1:limit+1]
            ]

            # 링크 목록
            buttons = await page.locator(ArticlePageLocators.COPY_BUTTON).all()
            thumbs = await page.locator(ArticlePageLocators.THUMB).all()

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

            await browser.close()

        return [
            {"title": t, "img": i, "link": l}
            for t, i, l in zip(title_list, img_src_list, links)
        ]