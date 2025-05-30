import asyncio
from playwright.async_api import async_playwright
import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
NESPICK_ID = os.getenv("NEWSPICK_ID")
NESPICK_PW = os.getenv("NEWSPICK_PW")
threads_user_id = os.getenv("THREADUSER_ID")  #threads id
media_type = "IMAGE"    #이미지 업로드 

# 전역 변수 정의
global_title_list = []
global_img_src_list = []
global_link_list = []
global_threads_list = []

async def main():
    global global_title_list, global_img_src_list, global_link_list  # 전역 변수를 사용한다고 명시

    async with async_playwright() as p:
        # Chromium 브라우저 실행
        browser = await p.chromium.launch(headless=False)  # headless=True면 백그라운드 실행
        context = await browser.new_context()
        await context.grant_permissions(["clipboard-read", "clipboard-write"], origin="https://partners.newspic.kr/main/index1")
        page = await browser.new_page()
        page.on('dialog', lambda dialog: dialog.accept())
        
        # 웹페이지 열기
        await page.goto("https://partners.newspic.kr/main/index")

        await page.wait_for_selector(".input-m")
        await page.fill("input[name='id']", NESPICK_ID)
        await page.fill("input[name='password']", NESPICK_PW)

        await page.click(".btn-confirm")  # 버튼 클릭
        await asyncio.sleep(3)

        # 이미지 src 목록 가져오기
        img_src_list = await page.locator('img[alt="기사 대표이미지"]').evaluate_all("imgs => imgs.map(img => img.src)")
        del img_src_list[0]
        global_img_src_list = img_src_list[:20]  # 전역 변수에 저장

        # 제목 목록 가져오기
        title_list = await page.locator('span.text-overflow2').all_inner_texts()
        del title_list[0]
        global_title_list = title_list[:20]  # 전역 변수에 저장
        
        global_title_list = [title.replace(" …", "") for title in global_title_list]
        global_title_list = [title.replace("'", " ") for title in global_title_list]
        global_title_list = [title.replace('"', " ") for title in global_title_list]
        thumb_elements = await page.locator("section.section01 div.thumb").all()
        
        print(f"🔍 찾은 thumb 요소 개수: {len(thumb_elements)}")
        print(thumb_elements)

        buttons = await page.locator('section.section01 button[data-channel-no="1"][data-type="copyurl"]').all()

        num_clicks = min(len(buttons), 20)  # 최대 20개 클릭
        print(f"총 {len(buttons)}개의 버튼을 찾았습니다. {num_clicks}개만 클릭합니다.")

        for idx, button in enumerate(buttons[:num_clicks]):
            # 버튼 클릭 (강제 클릭)
            await thumb_elements[idx].hover()
            await page.mouse.down()
            print(f"버튼 {idx+1} 클릭 중...")
            await button.click()
            await page.wait_for_timeout(1000)
            await page.mouse.up()  # 마우스 버튼 떼기

            # 버튼 클릭 후 클립보드에서 링크 읽기 (async/await 사용)
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

            # 읽어온 링크를 리스트에 추가
            global_link_list.append(copied_link)

        await browser.close()

# 비동기 함수 내에서 main 실행
asyncio.run(main())
print(global_img_src_list)
print(global_title_list)
print(global_link_list)

for i in range(20):
    image_url = global_img_src_list[i]
    text = global_title_list[i]
    #media container 생성
    response = requests.post(f"https://graph.threads.net/v1.0/{threads_user_id}/threads?media_type={media_type}&image_url={image_url}&text={text}&access_token={ACCESS_TOKEN}").json()
    print(response)
    container_id = response.get('id')

    #media container 발행
    response2 = requests.post(f"https://graph.threads.net/v1.0/{threads_user_id}/threads_publish?creation_id={container_id}&access_token={ACCESS_TOKEN}").json()
    print(response2)
    media_id = response2.get('id')
    print(container_id)
    print(media_id)
    global_threads_list.append(media_id)

print(global_threads_list)


for j in range(20):
    media_type2 = "TEXT"
    text2 = global_link_list[j]
    response3 = requests.post(f"https://graph.threads.net/v1.0/me/threads?media_type={media_type2}&text={text2}&reply_to_id={global_threads_list[j]}&access_token={ACCESS_TOKEN}").json()
    print(response3)
    container_id2 = response3.get('id')

    #reply
    response4 = requests.post(f"https://graph.threads.net/v1.0/{threads_user_id}/threads_publish?creation_id={container_id2}&access_token={ACCESS_TOKEN}").json()

