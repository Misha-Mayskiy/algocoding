import asyncio
import os
import random
import logging
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# ===================== Конфигурация =====================
load_dotenv()


def _env_flag(name: str, default: str = '0') -> bool:
    return os.getenv(name, default).strip().lower() in ('1', 'true', 'yes', 'y', 'on')


LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

GODVILLE_LOGIN = os.getenv('GODVILLE_LOGIN')
GODVILLE_PASSWORD = os.getenv('GODVILLE_PASSWORD')

# Экономия ресурсов по умолчанию
HEADLESS = _env_flag('HEADLESS', '1')
BLOCK_TRACKERS = _env_flag('BLOCK_TRACKERS', '1')
BLOCK_MEDIA = _env_flag('BLOCK_MEDIA', '1')  # режем image/font/media
SAVE_STATE = _env_flag('SAVE_STATE', '1')  # хранить state.json (куки и пр.)

STATE_PATH = Path(os.getenv('STATE_PATH', 'state.json'))

USER_AGENT = os.getenv('USER_AGENT',
                       'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
LOCALE = os.getenv('LOCALE', 'ru-RU')
VIEWPORT_W = int(os.getenv('VIEWPORT_W', '960'))
VIEWPORT_H = int(os.getenv('VIEWPORT_H', '600'))

LOGIN_URL = 'https://godville.net/login'
HERO_URL = 'https://godville.net/superhero'

# Режим действий: random | good | bad
ACTION_MODE_RAW = os.getenv('ACTION_MODE', 'random').strip().lower()
ALIASES = {
    'rand': 'random', 'rnd': 'random', 'случайно': 'random',
    'good-only': 'good', 'enc': 'good', 'encour': 'good', 'хорошо': 'good',
    'bad-only': 'bad', 'pun': 'bad', 'punish': 'bad', 'плохо': 'bad'
}
ACTION_MODE = ALIASES.get(ACTION_MODE_RAW, ACTION_MODE_RAW)
if ACTION_MODE not in ('random', 'good', 'bad'):
    ACTION_MODE = 'random'
ACTION_FALLBACK = _env_flag('ACTION_FALLBACK', '0')

# Интервалы между попытками действий
MIN_ACTION_INTERVAL_SEC = int(os.getenv('MIN_ACTION_INTERVAL_SEC', '5'))
MAX_ACTION_INTERVAL_SEC = int(os.getenv('MAX_ACTION_INTERVAL_SEC', '20'))

# Когда кнопок нет N раз подряд — «спим»
NO_BUTTONS_GRACE_CHECKS = int(os.getenv('NO_BUTTONS_GRACE_CHECKS', '3'))
SHORT_RETRY_DELAY_SEC = float(os.getenv('SHORT_RETRY_DELAY_SEC', '1.5'))

SLEEP_MIN_SEC = int(os.getenv('SLEEP_MIN_SEC', '3600'))
SLEEP_MAX_SEC = int(os.getenv('SLEEP_MAX_SEC', '7200'))

# Если не видим кнопки несколько раз — делаем мягкое обновление/переход
RELOAD_ON_MISS = int(os.getenv('RELOAD_ON_MISS', '2'))  # после скольких промахов делать page.reload
NAVIGATE_ON_MISS = int(os.getenv('NAVIGATE_ON_MISS', '4'))  # после скольких промахов делать goto(HERO_URL)

# Тайминги
CLICK_TIMEOUT_MS = int(os.getenv('CLICK_TIMEOUT_MS', '1500'))
DETECT_TIMEOUT_MS = int(os.getenv('DETECT_TIMEOUT_MS', '7000'))

# Хосты-трекеры (отрежем для экономии трафика и шума)
TRACKER_HOST_SUBSTR = (
    'googletagmanager.com', 'google-analytics.com', 'doubleclick.net',
    'g.doubleclick.net', 'www.google.com/ccm'
)

# Селекторы кнопок
GOOD_SELECTORS = [
    '#cntrl1 a.enc_link', '#cntrl a.enc_link', 'a.enc_link',
    'a:has-text("Сделать хорошо")', 'button:has-text("Сделать хорошо")',
    '[onclick*="encour"]', 'a[href*="encour"]',
]
BAD_SELECTORS = [
    '#cntrl1 a.pun_link', '#cntrl a.pun_link', 'a.pun_link',
    'a:has-text("Сделать плохо")', 'button:has-text("Сделать плохо")',
    '[onclick*="punish"]', 'a[href*="punish"]',
]


# ===================== Маршрутизация запросов =====================
async def setup_routing(context):
    if not (BLOCK_TRACKERS or BLOCK_MEDIA):
        return

    async def route_all(route):
        try:
            req = route.request
            url = req.url
            rtype = req.resource_type

            if BLOCK_MEDIA and rtype in ('image', 'media', 'font'):
                return await route.abort()

            if BLOCK_TRACKERS and any(h in url for h in TRACKER_HOST_SUBSTR):
                return await route.abort()

            return await route.continue_()
        except Exception:
            try:
                await route.continue_()
            except Exception:
                pass

    await context.route("**/*", route_all)


# ===================== Утилиты =====================
async def dismiss_cookie_banners(page):
    candidates = (
        'button:has-text("Принять")', 'button:has-text("Соглас")',
        'button:has-text("OK")', 'button:has-text("ОК")',
        'button:has-text("Accept")', 'button:has-text("I agree")',
        'text=Принять', 'text=Соглас', 'text=Accept', 'text=I agree',
    )
    for sel in candidates:
        try:
            loc = page.locator(sel).first
            if await loc.count() and await loc.is_visible():
                await loc.click()
                await asyncio.sleep(0.2)
        except Exception:
            pass


async def save_debug(page, prefix="debug"):
    try:
        await page.screenshot(path=f"{prefix}.png", full_page=True)
        with open(f"{prefix}.html", "w", encoding="utf-8") as f:
            f.write(await page.content())
        logging.info(f"Сохранил {prefix}.png / {prefix}.html")
    except Exception as e:
        logging.debug(f"Не удалось сохранить отладку: {e}")


async def _first_visible(page, selectors) -> Tuple[Optional[object], Optional[str]]:
    """Первый видимый локатор из набора селекторов."""
    for sel in selectors:
        loc = page.locator(sel).first
        try:
            if await loc.count():
                try:
                    await loc.scroll_into_view_if_needed(timeout=300)
                except Exception:
                    pass
                if await loc.is_visible():
                    return loc, sel
        except Exception:
            continue
    return None, None


async def wait_prana_controls(page, which='any', timeout_ms=DETECT_TIMEOUT_MS) -> bool:
    """Ждём появления кнопок 'Сделать хорошо/плохо'. which: any|good|bad"""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + (timeout_ms / 1000.0)
    while loop.time() < deadline:
        good_loc, _ = await _first_visible(page, GOOD_SELECTORS)
        bad_loc, _ = await _first_visible(page, BAD_SELECTORS)
        if which == 'good' and good_loc:
            return True
        if which == 'bad' and bad_loc:
            return True
        if which == 'any' and (good_loc or bad_loc):
            return True
        await asyncio.sleep(0.25)
    return False


async def find_action_buttons(page):
    good_loc, good_sel = await _first_visible(page, GOOD_SELECTORS)
    bad_loc, bad_sel = await _first_visible(page, BAD_SELECTORS)
    return good_loc, bad_loc, {"good": good_sel, "bad": bad_sel}


# ===================== Логин/сессия =====================
async def perform_login(page, login: str, password: str) -> bool:
    logging.info("Открываю страницу логина...")
    await page.goto(LOGIN_URL, wait_until="domcontentloaded")

    await dismiss_cookie_banners(page)
    await page.wait_for_selector('form[action="/login"], input[name], button[type="submit"]', timeout=20000)

    user_sel = 'input[name="username"], input[name="login"], #username, form[action="/login"] input[type="text"]'
    pass_sel = 'input[name="password"], #password, form[action="/login"] input[type="password"]'
    submit_sel = 'button:has-text("Войти"), input[type="submit"], button[type="submit"]'

    await page.locator(user_sel).first.fill(login)
    await page.locator(pass_sel).first.fill(password)

    try:
        async with page.expect_navigation(wait_until="domcontentloaded", timeout=15000):
            await page.locator(submit_sel).first.click()
    except PlaywrightTimeoutError:
        logging.warning("Навигации после сабмита не было — проверяю вручную...")

    await page.goto(HERO_URL, wait_until="domcontentloaded")

    if "login" in page.url:
        logging.error("Логин не удался — всё ещё на /login.")
        await save_debug(page, "login_failed")
        return False

    try:
        await page.wait_for_selector('#cntrl1, #cntrl, #god_name', timeout=20000)
    except PlaywrightTimeoutError:
        logging.error("Не дождался признаков страницы героя.")
        await save_debug(page, "hero_wait_failed")
        return False

    logging.info("Авторизация прошла успешно.")
    return True


async def ensure_logged_in(context, page, login, password) -> bool:
    await page.goto(HERO_URL, wait_until="domcontentloaded")
    if "login" in page.url:
        logging.info("Сессии нет — логинюсь.")
        ok = await perform_login(page, login, password)
        if ok and SAVE_STATE:
            try:
                await context.storage_state(path=str(STATE_PATH))
                logging.info(f"Сессия сохранена в {STATE_PATH}")
            except Exception as e:
                logging.debug(f"Не удалось сохранить сессию: {e}")
        return ok
    return True


# ===================== Клик по действию =====================
async def click_prana_action(page) -> bool:
    """Кликает good/bad по режиму. Возвращает True, если кликнули."""
    if "superhero" not in page.url:
        await page.goto(HERO_URL, wait_until="domcontentloaded")

    which = 'any' if ACTION_MODE == 'random' else ACTION_MODE
    if not await wait_prana_controls(page, which=which, timeout_ms=DETECT_TIMEOUT_MS):
        return False

    good_loc, bad_loc, _ = await find_action_buttons(page)

    candidates = []
    if ACTION_MODE == 'random':
        if random.choice([True, False]):
            if good_loc: candidates.append(("Сделать хорошо", good_loc))
            if bad_loc:  candidates.append(("Сделать плохо", bad_loc))
        else:
            if bad_loc:  candidates.append(("Сделать плохо", bad_loc))
            if good_loc: candidates.append(("Сделать хорошо", good_loc))
    elif ACTION_MODE == 'good':
        if good_loc:
            candidates.append(("Сделать хорошо", good_loc))
        elif ACTION_FALLBACK and bad_loc:
            candidates.append(("Сделать плохо", bad_loc))
    else:  # ACTION_MODE == 'bad'
        if bad_loc:
            candidates.append(("Сделать плохо", bad_loc))
        elif ACTION_FALLBACK and good_loc:
            candidates.append(("Сделать хорошо", good_loc))

    for title, loc in candidates:
        try:
            await loc.click(timeout=CLICK_TIMEOUT_MS)
            await asyncio.sleep(random.uniform(0.6, 1.2))  # мягкая пауза после клика
            logging.info(f"Нажал: {title}")
            return True
        except Exception:
            continue

    return False


# ===================== Основной цикл =====================
async def run_bot():
    if not GODVILLE_LOGIN or not GODVILLE_PASSWORD:
        logging.error("Не найдены GODVILLE_LOGIN / GODVILLE_PASSWORD в .env")
        return

    launch_args = [
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--disable-gpu",
        "--mute-audio",
        "--js-flags=--max-old-space-size=128",
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS, args=launch_args)
        context_kwargs = dict(
            user_agent=USER_AGENT,
            locale=LOCALE,
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            extra_http_headers={"Accept-Language": f"{LOCALE},ru;q=0.9,en;q=0.8"},
        )
        if SAVE_STATE and STATE_PATH.exists():
            context_kwargs["storage_state"] = str(STATE_PATH)

        context = await browser.new_context(**context_kwargs)
        await setup_routing(context)

        # На всякий случай гасим любые диалоги/алерты
        page = await context.new_page()
        page.set_default_timeout(20000)
        page.on("dialog", lambda d: asyncio.create_task(d.dismiss()))

        try:
            if not await ensure_logged_in(context, page, GODVILLE_LOGIN, GODVILLE_PASSWORD):
                logging.error("Не удалось авторизоваться. Останавливаюсь.")
                return

            logging.info(
                f"Режим действий: {ACTION_MODE}{' + fallback' if ACTION_FALLBACK else ''}. Headless={HEADLESS}.")
            miss_streak = 0

            while True:
                # Пауза между действиями (минимальная для экономии CPU)
                await asyncio.sleep(random.uniform(MIN_ACTION_INTERVAL_SEC, MAX_ACTION_INTERVAL_SEC))

                # Если разлогинило — перелогин
                if "login" in page.url:
                    if not await ensure_logged_in(context, page, GODVILLE_LOGIN, GODVILLE_PASSWORD):
                        logging.error("Перелогин не удался. Завершаю.")
                        return

                # Периодически подстраховываемся лёгким обновлением, но не каждую итерацию
                if miss_streak == RELOAD_ON_MISS:
                    try:
                        await page.reload(wait_until="domcontentloaded")
                    except Exception:
                        pass
                elif miss_streak >= NAVIGATE_ON_MISS:
                    try:
                        await page.goto(HERO_URL, wait_until="domcontentloaded")
                    except Exception:
                        pass

                clicked = await click_prana_action(page)
                if clicked:
                    miss_streak = 0
                    continue

                # Кнопок нет — короткий ретрай
                miss_streak += 1
                logging.info(f"Кнопок нет (#{miss_streak}). Повторная проверка через {SHORT_RETRY_DELAY_SEC:.1f} сек.")
                await asyncio.sleep(SHORT_RETRY_DELAY_SEC)

                clicked_retry = await click_prana_action(page)
                if clicked_retry:
                    miss_streak = 0
                    continue

                if miss_streak >= NO_BUTTONS_GRACE_CHECKS:
                    # Кажется, прану потратили — уходим в сон
                    nap = random.uniform(SLEEP_MIN_SEC, SLEEP_MAX_SEC)
                    logging.info(f"Кнопок нет {miss_streak} раз подряд — сон на {nap / 60:.0f} мин.")
                    miss_streak = 0
                    await asyncio.sleep(nap)

        except PlaywrightTimeoutError as te:
            logging.error(f"Таймаут: {te}")
            await save_debug(page, "timeout_debug")
        except Exception as e:
            logging.error(f"Необработанная ошибка: {e}")
            await save_debug(page, "crash_debug")
        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logging.info("Остановлено пользователем.")
