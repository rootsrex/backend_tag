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
            extra_http_headers={"Accept-Language": "es-EC,es;q=0.9,en;q=0.8"}
        )
        await context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )

        page = await context.new_page()

        await page.goto("https://www.google.com", wait_until="load", timeout=20000)
        await asyncio.sleep(0.5)
        await page.goto(URL, wait_until="load", timeout=30000)
        await asyncio.sleep(2)

        await page.select_option("#Opcion", "N")
        await asyncio.sleep(0.3)
        await page.fill("#txtName", "1710034065")
        await asyncio.sleep(0.3)

        # Inyectar MutationObserver antes del clic para capturar cambios en el DOM
        await page.evaluate("""
            window._domChanges = [];
            const observer = new MutationObserver(mutations => {
                mutations.forEach(m => {
                    const el = m.target;
                    const id = el.id || el.className || el.tagName;
                    const change = {
                        type: m.type,
                        target: id,
                        attr: m.attributeName,
                        oldVal: m.oldValue,
                        newVal: el.getAttribute ? el.getAttribute(m.attributeName) : null,
                        innerText: el.innerText ? el.innerText.substring(0, 100) : null,
                        time: Date.now()
                    };
                    window._domChanges.push(change);
                });
            });
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeOldValue: true,
                characterData: true
            });
        """)

        await page.click("#btnNext")
        print("Clic enviado, monitoreando DOM por 15 segundos...")
        await asyncio.sleep(15)

        # Leer los cambios capturados
        changes = await page.evaluate("window._domChanges")
        print(f"\nTotal cambios DOM detectados: {len(changes)}")
        for c in changes:
            print(f"  [{c.get('type')}] target='{c.get('target')}' attr='{c.get('attr')}' "
                  f"old='{c.get('oldVal')}' new='{c.get('newVal')}' text='{c.get('innerText', '')[:60]}'")

        # HTML completo de la zona calculadora
        zona_html = await page.inner_html("#ZonaCalculadora")
        print(f"\n--- HTML de #ZonaCalculadora ---\n{zona_html[:2000]}")

        await page.screenshot(path="after_click_dom.png")
        await browser.close()

asyncio.run(debug())
