from nicegui import ui, run
import requests

BOARD = "http://10.201.48.74"

async def senda(slod):
    try:
        await run.io_bound(requests.get, BOARD + slod, timeout=5)
        ui.notify("Tókst")
    except Exception:
        ui.notify("Næ ekki sambandi við kassann", type="negative")

ui.label("Kassinn").classes("text-2xl")
ui.button("Opna", on_click=lambda: senda("/opna")).props("color=green")
ui.button("Loka", on_click=lambda: senda("/loka")).props("color=red")

ui.run()