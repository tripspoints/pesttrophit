import os, asyncio, aiohttp, datetime as dt
from src.db import get_session
from src.model import load_latest_params, dixon_coles_grid
from src.kelly import kelly_stake

TOKEN   = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL     = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

async def send(text: str):
    async with aiohttp.ClientSession() as s:
        await s.post(URL, json={"chat_id": CHAT_ID, "text": text})

def format_msg(row):
    home, away = row.home_team, row.away_team
    grid = dixon_coles_grid(load_latest_params(), home, away)
    p1, pX, p2 = grid.home_win, grid.draw, grid.away_win
    kelly = kelly_stake(p1, (1/p1)*0.98)  # 2 % exchange commission
    return (
        f"{home}  vs  {away}\n"
        f"1X2  :  {p1:.1%}  ‑  {pX:.1%}  ‑  {p2:.1%}\n"
        f"Kelly:  {abs(kelly):.2f}u on  {'home' if kelly>0 else 'away'}"
    )

async def notify_today():
    today = dt.date.today()
    session = get_session()
    fixtures = session.query(Fixture).filter(Fixture.date == today).all()
    for f in fixtures:
        await send(format_msg(f))

if __name__ == "__main__":
    asyncio.run(notify_today())
