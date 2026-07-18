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

        # Interceptar la respuesta del endpoint de consulta
        api_response_body = {}
        async def handle_response(response):
            if "consultar-cedula.php" in response.url:
                try:
                    body = await response.text()
                    api_response_body["url"] = response.url
                    api_response_body["status"] = response.status
                    api_response_body["body"] = body
                except Exception as e:
                    api_response_body["error"] = str(e)

        page.on("response", handle_response)

        await page.goto(URL, wait_until="load", timeout=30000)
        await asyncio.sleep(2)

        await page.select_option("#Opcion", "N")
        await asyncio.sleep(0.3)
        await page.fill("#txtName", "1710034065")
        await asyncio.sleep(0.3)
        await page.click("#btnNext")
        print("Clic enviado, esperando respuesta de la API...")

        await asyncio.sleep(10)

        if api_response_body:
            print(f"\nAPI URL: {api_response_body.get('url')}")
            print(f"Status: {api_response_body.get('status')}")
            print(f"\nRespuesta de la API:\n{api_response_body.get('body', '')}")
        else:
            print("No se capturó respuesta de la API")

        # Estado del DOM después
        try:
            resultado_display = await page.eval_on_selector("#resultado", "el => el.style.display")
            message_html = await page.inner_html("#message")
            loading_display = await page.eval_on_selector("#loading", "el => el.style.display")
            print(f"\n#resultado display: '{resultado_display}'")
            print(f"#loading display: '{loading_display}'")
            print(f"#message HTML: '{message_html[:500]}'")
        except Exception as e:
            print(f"Error leyendo DOM: {e}")

        await browser.close()

asyncio.run(debug())
