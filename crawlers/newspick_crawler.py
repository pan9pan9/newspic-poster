import asyncio
from playwright.async_api import async_playwright


class NewspickCrawler:
    def __init__(self, user_id: str, password: str):
        self.user_id = user_id
        self.password = password

    async def fetch_articles(self, limit: int = 20):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            page.on('dialog', lambda dialog: dialog.accept())

            # 로그인
            await page.goto("https://partners.newspic.kr/main/index")
            await page.fill("input[name='id']", self.user_id)
            await page.fill("input[name='password']", self.password)
            await page.click(".btn-confirm")
            await asyncio.sleep(3)

            # 이미지 목록
            img_src_list = await page.locator('img[alt="기사 대표이미지"]').evaluate_all(
                "imgs => imgs.map(img => img.src)"
            )
            del img_src_list[0]
            img_src_list = img_src_list[:limit]

            # 제목 목록
            title_list = await page.locator('span.text-overflow2').all_inner_texts()
            del title_list[0]
            title_list = [
                t.replace(" …", "").replace("'", " ").replace('"', " ")
                for t in title_list[:limit]
            ]

            # 링크 목록
            buttons = await page.locator(
                'section.section01 button[data-channel-no="1"][data-type="copyurl"]'
            ).all()
            thumb_elements = await page.locator("section.section01 div.thumb").all()

            links = []
            for idx, button in enumerate(buttons[:limit]):
                await thumb_elements[idx].hover()
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

        return [{"title": t, "img": i, "link": l} for t, i, l in zip(title_list, img_src_list, links)]