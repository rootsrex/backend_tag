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

        # Capturar requests de red
        requests_log = []
        async def on_request(req):
            if "ecuadorlegal" in req.url or "registro" in req.url.lower():
                requests_log.append(f"REQ: {req.method} {req.url}")

        async def on_response(res):
            if "ecuadorlegal" in res.url:
                requests_log.append(f"RES {res.status}: {res.url}")

        page = await context.new_page()
        page.on("request", on_request)
        page.on("response", on_response)

        await page.goto(URL, wait_until="load", timeout=30000)
        await asyncio.sleep(2)

        # Seleccionar cédula y escribir
        await page.select_option("#Opcion", "N")
        await asyncio.sleep(0.5)
        await page.fill("#txtName", "1710034065")
        await asyncio.sleep(0.5)

        # Estado antes del clic
        resultado_display = await page.eval_on_selector("#resultado", "el => el.style.display")
        print(f"#resultado display ANTES del clic: '{resultado_display}'")

        await page.screenshot(path="before_click.png")
        print("Screenshot guardado: before_click.png")

        # Clic
        await page.click("#btnNext")
        print("Clic en #btnNext ejecutado")

        # Esperar y tomar screenshots periódicos
        for i in range(10):
            await asyncio.sleep(2)
            try:
                display = await page.eval_on_selector("#resultado", "el => el.style.display")
                loading = await page.eval_on_selector("#loading", "el => el.style.display")
                print(f"  t={i*2+2}s -> #resultado display='{display}' | #loading display='{loading}'")
                if display != "none" and display != "":
                    print("  -> Resultados visibles!")
                    break
            except Exception as e:
                print(f"  t={i*2+2}s -> error: {e}")

        await page.screenshot(path="after_click.png")
        print("Screenshot guardado: after_click.png")

        # Mostrar requests de red capturados
        print("\n--- Requests de red hacia ecuadorlegal ---")
        for r in requests_log:
            print(" ", r)

        # Revisar el HTML actual del área de resultados y loading
        try:
            msg_html = await page.inner_html("#message")
            print(f"\n#message HTML: {msg_html[:500]}")
        except Exception:
            pass

        await browser.close()

asyncio.run(debug())
