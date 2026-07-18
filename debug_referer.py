import asyncio
from playwright.async_api import async_playwright

URL = "https://www.ecuadorlegalonline.com/consultas/registro-civil/consultar-cedulas/"

async def debug():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            channel="chrome",
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
            # SIN Referer fijo — dejar que el navegador lo maneje solo
            extra_http_headers={
                "Accept-Language": "es-EC,es;q=0.9,en;q=0.8",
            }
        )
        await context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )

        page = await context.new_page()

        # Capturar POST a la API
        post_info = {}
        async def handle_request(req):
            if "consultar-cedula.php" in req.url:
                post_info["post_data"] = req.post_data
                post_info["referer"] = req.headers.get("referer", "")
        async def handle_response(res):
            if "consultar-cedula.php" in res.url:
                post_info["status"] = res.status
                post_info["body"] = await res.text()

        page.on("request", handle_request)
        page.on("response", handle_response)

        # Navegar primero a Google para tener un referer natural
        print("Navegando a Google primero...")
        await page.goto("https://www.google.com", wait_until="load", timeout=20000)
        await asyncio.sleep(1)

        print("Navegando a la página objetivo...")
        await page.goto(URL, wait_until="load", timeout=30000)
        await asyncio.sleep(2)

        title = await page.title()
        print(f"Título: {title}")

        await page.select_option("#Opcion", "N")
        await asyncio.sleep(0.3)
        await page.fill("#txtName", "1710034065")
        await asyncio.sleep(0.3)
        await page.click("#btnNext")
        print("Clic enviado...")

        await asyncio.sleep(10)

        print(f"\nPost data enviado: {post_info.get('post_data')}")
        print(f"Referer en el XHR: {post_info.get('referer')}")
        print(f"Status: {post_info.get('status')}")
        print(f"Body: '{post_info.get('body', '(vacío)')}'")

        await browser.close()

asyncio.run(debug())
