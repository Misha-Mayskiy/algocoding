import asyncio
import os
import random
import logging
from pathlib import Path

from dotenv import load_dotenv
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# ===================== Конфиг =====================
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GODVILLE_LOGIN = os.getenv('GODVILLE_LOGIN')
GODVILLE_PASSWORD = os.getenv('GODVILLE_PASSWORD')

HEADLESS_MODE = os.getenv('HEADLESS', '0').lower() in ('1', 'true', 'yes', 'y')
LOG_PAGE_CONSOLE = os.getenv('LOG_PAGE_CONSOLE', '0').lower() in ('1', 'true', 'yes', 'y')  # логи из консоли страницы
FILTER_CONSOLE_NOISE = True  # фильтр шумных сообщений (GTM/GA/CSP) если LOG_PAGE_CONSOLE включен
BLOCK_TRACKERS = os.getenv('BLOCK_TRACKERS', '1').lower() in ('1', 'true', 'yes', 'y')  # блокируем трекеры

STATE_PATH = Path("state.json")

LOGIN_URL = 'https://godville.net/login'
HERO_URL = 'https://godville.net/superhero'

# Интервалы между действиями (сек)
MIN_ACTION_INTERVAL_SEC = int(os.getenv('MIN_ACTION_INTERVAL_SEC', '120'))
MAX_ACTION_INTERVAL_SEC = int(os.getenv('MAX_ACTION_INTERVAL_SEC', '300'))

# Иногда имитируем «сон»
SLEEP_PROBABILITY = float(os.getenv('SLEEP_PROBABILITY', '0.1'))
SLEEP_MIN_SEC = int(os.getenv('SLEEP_MIN_SEC', '3600'))  # 1 час
SLEEP_MAX_SEC = int(os.getenv('SLEEP_MAX_SEC', '10800'))  # 3 часа

USER_AGENT = os.getenv('USER_AGENT',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
LOCALE = os.getenv('LOCALE', 'ru-RU')

TRACKER_BLOCK_LIST = [
    '*://*.googletagmanager.com/*',
    '*://*.google-analytics.com/*',
    '*://*.doubleclick.net/*',
    '*://*.g.doubleclick.net/*',
    '*://www.google.com/ccm/*',
]


# ===================== Утилиты =====================
async def click_if_visible(page, selector: str, timeout: int = 1500) -> bool:
    try:
        loc = page.locator(selector).first
        if await loc.count() == 0:
            return False
        if await loc.is_visible():
            await loc.click(timeout=timeout)
            return True
    except Exception:
        return False
    return False


async def dismiss_cookie_banners(page):
    candidates = [
        'button:has-text("Принять")',
        'button:has-text("Соглас")',
        'button:has-text("OK")',
        'button:has-text("ОК")',
        'button:has-text("Accept")',
        'button:has-text("I agree")',
        'text=Принять',
        'text=Соглас',
        'text=Accept',
        'text=I agree',
    ]
    for sel in candidates:
        if await click_if_visible(page, sel):
            logging.info(f"Закрыл баннер по селектору: {sel}")
            await asyncio.sleep(0.2)


async def save_debug(page, prefix="debug"):
    png = f"{prefix}.png"
    html = f"{prefix}.html"
    try:
        await page.screenshot(path=png, full_page=True)
        with open(html, "w", encoding="utf-8") as f:
            f.write(await page.content())
        logging.info(f"Сохранил отладочные файлы: {png}, {html}")
    except Exception as e:
        logging.warning(f"Не удалось сохранить отладочные файлы: {e}")


def attach_console_logger(page):
    if not LOG_PAGE_CONSOLE:
        return

    noise_keywords = (
        'googletagmanager', 'google-analytics', 'doubleclick',
        'Content Security Policy', 'CSP', "Refused to connect", "Refused to frame",
        "Failed to execute 'postMessage'"
    )

    def _on_console(msg):
        try:
            text = msg.text
        except Exception:
            text = ''
        try:
            loc = msg.location
            src = loc.get('url', '')
        except Exception:
            src = ''
        if FILTER_CONSOLE_NOISE:
            if any(k in text or k in src for k in noise_keywords):
                return
        logging.info(f"[console] {msg.type}: {text}")

    page.on("console", _on_console)


async def setup_blocking_routes(context):
    if not BLOCK_TRACKERS:
        return

    async def _block(route):
        try:
            await route.abort()
        except Exception:
            pass

    for pattern in TRACKER_BLOCK_LIST:
        await context.route(pattern, _block)


# ===================== Логин/сессия =====================
async def perform_login(page, login: str, password: str) -> bool:
    logging.info("Открываю страницу логина...")
    await page.goto(LOGIN_URL, wait_until="domcontentloaded")
    await dismiss_cookie_banners(page)

    # Ждём появления формы
    await page.wait_for_selector('form[action="/login"], input[name], button[type="submit"]', timeout=20000)

    # Поля/кнопка с запасом по селекторам
    user_sel = 'input[name="username"], input[name="login"], #username, form[action="/login"] input[type="text"]'
    pass_sel = 'input[name="password"], #password, form[action="/login"] input[type="password"]'
    submit_sel = 'button:has-text("Войти"), input[type="submit"], button[type="submit"]'

    logging.info("Ввожу логин и пароль...")
    await page.locator(user_sel).first.fill(login)
    await page.locator(pass_sel).first.fill(password)

    logging.info("Жму «Войти» и жду переход...")
    try:
        async with page.expect_navigation(wait_until="domcontentloaded", timeout=15000):
            await page.locator(submit_sel).first.click()
    except PlaywrightTimeoutError:
        logging.warning("Навигации после сабмита не было — продолжаю проверку...")

    # Переходим на страницу героя и валидируем
    await page.goto(HERO_URL, wait_until="domcontentloaded")

    if "login" in page.url:
        logging.error("Похоже, логин не удался — всё ещё на /login.")
        await save_debug(page, "login_failed")
        return False

    # Ждём ключевые элементы страницы героя
    try:
        await page.wait_for_selector('#cntrl1, #god_name, #cntrl', timeout=20000)
    except PlaywrightTimeoutError:
        logging.error("Не дождался элементов страницы героя после логина.")
        await save_debug(page, "hero_wait_failed")
        return False

    logging.info("Авторизация прошла успешно.")
    return True


async def ensure_logged_in(context, page, login, password) -> bool:
    await page.goto(HERO_URL, wait_until="domcontentloaded")
    if "login" in page.url:
        logging.info("Сессии нет — логинюсь.")
        ok = await perform_login(page, login, password)
        if ok:
            try:
                await context.storage_state(path=str(STATE_PATH))
                logging.info(f"Сессия сохранена в {STATE_PATH}")
            except Exception as e:
                logging.warning(f"Не удалось сохранить сессию: {e}")
        return ok
    logging.info("Сессия активна.")
    return True


# ===================== Действия =====================
async def click_prana_action(page) -> bool:
    # Если не на странице героя — зайдём
    if "superhero" not in page.url:
        await page.goto(HERO_URL, wait_until="domcontentloaded")

    # Лёгкое обновление, чтобы подтянуть актуальное состояние
    try:
        await page.reload(wait_until="domcontentloaded")
    except Exception:
        pass

    actions = [
        ('#cntrl1 a.enc_link', 'Сделать хорошо'),
        ('#cntrl1 a.pun_link', 'Сделать плохо'),
        ('#cntrl a.enc_link', 'Сделать хорошо'),
        ('#cntrl a.pun_link', 'Сделать плохо'),
    ]

    is_good = random.choice([True, False])
    ordered = [a for a in actions if ('enc_link' in a[0]) == is_good] + [a for a in actions if
                                                                         ('enc_link' in a[0]) != is_good]

    for selector, title in ordered:
        loc = page.locator(selector).first
        if await loc.count() == 0:
            continue
        try:
            if await loc.is_visible():
                logging.info(f"Нажимаю «{title}» ({selector})")
                await loc.click()
                await asyncio.sleep(random.uniform(1.0, 2.0))
                return True
        except Exception as e:
            logging.debug(f"Не удалось нажать {title}: {e}")
            continue

    logging.info("Кнопок траты праны нет или они недоступны.")
    return False


# ===================== Основной цикл =====================
async def run_bot():
    if not GODVILLE_LOGIN or not GODVILLE_PASSWORD:
        logging.error("Не найдены GODVILLE_LOGIN / GODVILLE_PASSWORD в .env")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS_MODE)
        context_kwargs = dict(
            user_agent=USER_AGENT,
            locale=LOCALE,
            extra_http_headers={"Accept-Language": f"{LOCALE},ru;q=0.9,en;q=0.8"},
        )
        if STATE_PATH.exists():
            context_kwargs["storage_state"] = str(STATE_PATH)

        context = await browser.new_context(**context_kwargs)
        await setup_blocking_routes(context)

        page = await context.new_page()
        page.set_default_timeout(20000)
        attach_console_logger(page)

        try:
            # Авторизация/сессия
            ok = await ensure_logged_in(context, page, GODVILLE_LOGIN, GODVILLE_PASSWORD)
            if not ok:
                logging.error("Не удалось авторизоваться. Останавливаюсь.")
                return

            # Цикл действий
            while True:
                # Иногда «спим», имитируя оффлайн
                if random.random() < SLEEP_PROBABILITY:
                    nap = random.uniform(SLEEP_MIN_SEC, SLEEP_MAX_SEC)
                    logging.info(f"Имитация сна на {nap / 3600:.1f} ч.")
                    await asyncio.sleep(nap)

                wait_time = random.uniform(MIN_ACTION_INTERVAL_SEC, MAX_ACTION_INTERVAL_SEC)
                logging.info(f"Следующее действие через {wait_time:.0f} сек.")
                await asyncio.sleep(wait_time)

                # Подстрахуемся от разлогина
                if "login" in page.url:
                    logging.info("Похоже, сессия слетела — перезаход.")
                    if not await ensure_logged_in(context, page, GODVILLE_LOGIN, GODVILLE_PASSWORD):
                        logging.error("Перелогин не удался. Завершаю.")
                        return

                # Действие
                done = await click_prana_action(page)
                if not done:
                    logging.info("Действие пропущено (нет доступных кнопок).")

        except PlaywrightTimeoutError as te:
            logging.error(f"Таймаут: {te}")
            await save_debug(page, "timeout_debug")
        except asyncio.CancelledError:
            logging.info("Остановка по запросу.")
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
        logging.info("Программа остановлена пользователем.")
