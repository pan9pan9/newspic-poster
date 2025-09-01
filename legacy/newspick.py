import asyncio
from playwright.async_api import async_playwright

class NewspickCrawler:
    def __init__(self, user_id, password, limit=20):
        self.user_id = user_id
        self.password = password
        self.limit = limit

    async def fetch_articles(self):
        title_list = []
        img_src_list = []
        link_list = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # 디버깅 시 headless=False
            context = await browser.new_context()
            await context.grant_permissions(
                ["clipboard-read", "clipboard-write"],
                origin="https://partners.newspic.kr/main/index1"
            )
            page = await context.new_page()
            page.on('dialog', lambda dialog: dialog.accept())

            # 로그인
            await page.goto("https://partners.newspic.kr/main/index")
            await page.wait_for_selector(".input-m", timeout=10000)
            await page.fill("input[name='id']", self.user_id)
            await page.fill("input[name='password']", self.password)
            await page.click(".btn-confirm")
            await asyncio.sleep(3)

            # 이미지
            img_src_list = await page.locator('img[alt="기사 대표이미지"]').evaluate_all("imgs => imgs.map(img => img.src)")
            del img_src_list[0]
            img_src_list = img_src_list[:self.limit]

            # 제목
            title_list = await page.locator('span.text-overflow2').all_inner_texts()
            del title_list[0]
            title_list = title_list[:self.limit]
            title_list = [
                t.replace(" …", "").replace("'", " ").replace('"', " ")
                for t in title_list
            ]

            # 링크 (복사 버튼 클릭 후 클립보드 읽기)
            thumb_elements = await page.locator("section.section01 div.thumb").all()
            buttons = await page.locator('section.section01 button[data-channel-no="1"][data-type="copyurl"]').all()

            num_clicks = min(len(buttons), self.limit)
            print(f"총 {len(buttons)}개의 버튼 발견, {num_clicks}개 클릭")

            for idx, button in enumerate(buttons[:num_clicks]):
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
                link_list.append(copied_link)

            await browser.close()

        return [
            {"title": t, "img": i, "link": l}
            for t, i, l in zip(title_list, img_src_list, link_list)
        ]