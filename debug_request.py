import asyncio
from playwright.async_api import async_playwright

URL = "https://www.ecuadorlegalonline.com/consultas/registro-civil/consultar-cedulas/"
JS_URL = "https://www.ecuadorlegalonline.com/js/cinameapi3yjs.js"

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
                "Referer": "https://www.google.com/",
            }
        )
        await context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )

        page = await context.new_page()

        # Capturar request POST completo
        post_info = {}
        async def handle_request(request):
            if "consultar-cedula.php" in request.url:
                post_info["method"] = request.method
                post_info["url"] = request.url
                post_info["headers"] = dict(request.headers)
                try:
                    post_info["post_data"] = request.post_data
                except Exception:
                    post_info["post_data"] = None

        async def handle_response(response):
            if "consultar-cedula.php" in response.url:
                try:
                    body = await response.text()
                    post_info["response_body"] = body
                    post_info["response_headers"] = dict(response.headers)
                except Exception as e:
                    post_info["response_error"] = str(e)

        page.on("request", handle_request)
        page.on("response", handle_response)

        await page.goto(URL, wait_until="load", timeout=30000)
        await asyncio.sleep(2)

        # Leer el archivo JS principal para entender el mecanismo
        js_source = {}
        async def capture_js(response):
            if "cinameapi3yjs.js" in response.url:
                try:
                    js_source["body"] = await response.text()
                except Exception:
                    pass
        page.on("response", capture_js)

        await page.select_option("#Opcion", "N")
        await asyncio.sleep(0.3)
        await page.fill("#txtName", "1710034065")
        await asyncio.sleep(0.3)
        await page.click("#btnNext")

        await asyncio.sleep(8)

        print("=== POST REQUEST ===")
        print(f"URL: {post_info.get('url')}")
        print(f"Method: {post_info.get('method')}")
        print(f"Post Data: {post_info.get('post_data')}")
        print(f"\nHeaders enviados:")
        for k, v in (post_info.get("headers") or {}).items():
            print(f"  {k}: {v}")
        print(f"\nResponse body: '{post_info.get('response_body', '(vacío)')}'")
        print(f"Response headers: {post_info.get('response_headers', {})}")

        await browser.close()

asyncio.run(debug())
