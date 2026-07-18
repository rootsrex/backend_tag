import asyncio
from playwright.async_api import async_playwright

URL = "https://www.ecuadorlegalonline.com/consultas/registro-civil/consultar-cedulas/"

async def debug():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # modo visible para evitar detección
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="es-EC",
            extra_http_headers={
                "Accept-Language": "es-EC,es;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Referer": "https://www.google.com/",
            }
        )

        # Ocultar que es Playwright
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = await context.new_page()

        print(f"Navegando a {URL} ...")
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)

        print(f"\nTítulo: {await page.title()}")
        print(f"URL final: {page.url}")

        frames = page.frames
        print(f"\nTotal de frames: {len(frames)}")
        for i, frame in enumerate(frames):
            print(f"  Frame {i}: url={frame.url} | name={frame.name}")

        print("\n--- Buscando elementos en cada frame ---")
        for i, frame in enumerate(frames):
            for selector in ["#Opcion", "#txtName", "#btnNext", "#form1", "#ZonaCalculadora"]:
                try:
                    el = await frame.query_selector(selector)
                    if el:
                        print(f"  [Frame {i} | {frame.url[:80]}] ENCONTRADO: {selector}")
                except Exception:
                    pass

        html = await page.content()
        print("\n--- HTML (primeros 3000 chars) ---")
        print(html[:3000])

        await asyncio.sleep(2)
        await browser.close()

asyncio.run(debug())
