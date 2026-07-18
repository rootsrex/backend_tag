import asyncio
from playwright.async_api import async_playwright

URL = "https://www.ecuadorlegalonline.com/consultas/registro-civil/consultar-cedulas/"

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            channel="chrome",  # usa el Chrome real instalado
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="es-EC",
            extra_http_headers={
                "Accept-Language": "es-EC,es;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "https://www.google.com/",
            }
        )
        await context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )

        page = await context.new_page()
        print("Abriendo página en modo headless con Chrome real...")
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)

        title = await page.title()
        print(f"Título: {title}")

        el = await page.query_selector("#txtName")
        print(f"#txtName encontrado: {el is not None}")
        el2 = await page.query_selector("#btnNext")
        print(f"#btnNext encontrado: {el2 is not None}")

        await browser.close()

asyncio.run(test())
