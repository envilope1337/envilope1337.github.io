# QR Redirect Service

Сервис редиректа для физических QR-кодов на наклейках товаров. Позволяет менять
конечную ссылку (Telegram-канал, MAX, любая URL) **без перепечатки наклеек**.

## Как работает

```
QR на банке → pwr-redirect.pages.dev/p → meta refresh → t.me/pwr_supplements
                          ↑
                    меняем здесь = QR не трогаем
```

QR-код физически закодирован на короткий URL Cloudflare Pages. Хостинг отдаёт
HTML-страницу с автоматическим `meta http-equiv="refresh"` редиректом на нужный
канал. Когда нужно поменять цель — меняем строчку в HTML-файле и редеплоим в
Cloudflare. QR на банках работает дальше, ведёт уже на новую цель.

## Production-инфраструктура

| Что | Где | Доступ |
|-----|-----|--------|
| Хостинг | Cloudflare Pages | https://dash.cloudflare.com → Workers & Pages → `pwr-redirect` |
| Account ID | `164c53dfa2c4bb19ba262792740430dd` | (видно в URL дашборда) |
| Production URL | `https://pwr-redirect.pages.dev/` | публичный |
| Аутентификация (локально) | Wrangler OAuth токен | `~/.wrangler/config/default.toml` (auto-saved) |

## Финальные URL для QR-кодов

| Бренд | URL | Длина |
|-------|-----|-------|
| PWR Supplements | `https://pwr-redirect.pages.dev/p` | 32 симв |
| Seauty | `https://pwr-redirect.pages.dev/s` | 32 симв |

QR-коды сгенерированы и лежат на рабочем столе:
- `QR_PWR_FINAL.svg` / `.png` — для PWR
- `QR_SEAUTY_FINAL.svg` / `.png` — для Seauty

Параметры обоих QR: версия 4, 33×33 модулей, коррекция ошибок H (30%).

## Структура файлов

```
Tools/QR_Redirect/
├── README.md         (этот файл)
├── index.html        # Корень — landing для https://pwr-redirect.pages.dev/
├── p/index.html      # → t.me/pwr_supplements
└── s/index.html      # → t.me/seauty
```

## Как сменить целевую ссылку

### Способ 1 — через Claude (самый простой)

Напиши:
> *"Поменяй редирект `/p` на ссылку https://max.ru/pwr_supplements"*

Я сделаю:
1. Правлю `p/index.html` (3 места: meta refresh, JS replace, `<a href>`)
2. Запущу `npx wrangler pages deploy ... --project-name=pwr-redirect`
3. Через ~5 секунд live, QR на банках продолжит работать с новой целью

### Способ 2 — вручную через Cloudflare UI

1. https://dash.cloudflare.com → Workers & Pages → `pwr-redirect`
2. Deployments → Create deployment → Upload assets
3. Перетащить заново всю папку `Tools/QR_Redirect/` (или ZIP с `index.html`, `p/`, `s/`)
4. Production deploy → автоматически

### Способ 3 — вручную через Wrangler CLI

В терминале (после `npx wrangler login`):

```bash
cd "C:/Users/Roman.Gapancov/Desktop/TikTok Parser/Tools/QR_Redirect"
# Отредактировать p/index.html и/или s/index.html
npx wrangler pages deploy . --project-name=pwr-redirect --commit-dirty=true --branch=main
```

## Если в будущем понадобится свой домен (опционально)

Купить `.ru` домен (~500р/год) на reg.ru → в Cloudflare Pages → Custom domains
→ Add custom domain → ввести домен → пройти DNS verification (Cloudflare покажет
какие записи прописать). Дополнительно можно перевести зону домена на
Cloudflare DNS — тогда настройка автоматическая.

После активации custom domain старые QR на `pwr-redirect.pages.dev` **продолжат
работать** (Cloudflare держит оба URL). Перепечатывать наклейки не надо.

## История проекта

- **Первый деплой:** 2026-04-28 через Cloudflare Pages + Wrangler CLI
- **Почему не GitHub Pages:** аккаунт `PurePetv2` имеет user-level блокировку
  GitHub Actions ("Actions has been disabled for this user"), а Pages backend
  работает через Actions. Требует обращения в GitHub Support — отложено.
- Репозиторий `PurePetv2/purepetv2.github.io` создан, но не используется.
  При желании можно либо удалить его (через GitHub UI), либо подключить позже
  если Actions разблокируют.
