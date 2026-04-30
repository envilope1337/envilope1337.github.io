# QR Redirect Service

Сервис редиректа для физических QR-кодов на наклейках товаров. Позволяет менять
конечную ссылку (Telegram-канал, MAX, любая URL) **без перепечатки наклеек**.

## Как работает

```
QR на банке → envilope1337.github.io/p → meta refresh → t.me/pwr_supplements
                          ↑
                    меняем здесь = QR не трогаем
```

QR-код физически закодирован на короткий URL GitHub Pages. Хостинг отдаёт
HTML-страницу с автоматическим `meta http-equiv="refresh"` редиректом на нужный
канал. Когда нужно поменять цель — правим строчку в HTML, пушим в репо, через
~30 секунд GitHub Pages обновляется. QR на банках продолжает работать с новой
целью.

## Production-инфраструктура

| Что | Где |
|-----|-----|
| Хостинг | GitHub Pages (envilope1337.github.io) |
| Репозиторий | https://github.com/envilope1337/envilope1337.github.io |
| Production URL | https://envilope1337.github.io/ |

## Финальные URL для QR-кодов

| Бренд | URL | Длина |
|-------|-----|-------|
| PWR Supplements | `https://envilope1337.github.io/p` | 32 симв |
| Seauty | `https://envilope1337.github.io/s` | 32 симв |

QR-коды лежат на рабочем столе:
- `QR_PWR_FINAL.svg` / `.png` — для PWR
- `QR_SEAUTY_FINAL.svg` / `.png` — для Seauty

Параметры обоих QR: версия 4, 33×33 модулей, коррекция ошибок H (30%).

## Структура файлов

```
Tools/QR_Redirect/
├── README.md         (этот файл)
├── index.html        # https://envilope1337.github.io/
├── p/index.html      # https://envilope1337.github.io/p → t.me/pwr_supplements
└── s/index.html      # https://envilope1337.github.io/s → t.me/seauty
```

## Как сменить целевую ссылку

### Способ 1 — через Claude (самый простой)

Напиши:
> *"Поменяй редирект `/p` на ссылку https://max.ru/pwr_supplements"*

Я:
1. Правлю `Tools/QR_Redirect/p/index.html` (3 места: meta refresh, JS replace, `<a href>`)
2. `git commit + git push`
3. Через ~30 сек GitHub Pages обновляется. QR на банках продолжает работать с новой целью.

### Способ 2 — вручную через GitHub веб

1. https://github.com/envilope1337/envilope1337.github.io
2. Открыть `p/index.html` (или `s/index.html`)
3. Карандаш (Edit) → найти и заменить URL в трёх местах:
   - `<meta http-equiv="refresh" content="0; url=...">`
   - `window.location.replace("...")`
   - `<a href="...">`
4. Commit changes
5. Через 1-2 минуты обновится

### Способ 3 — локально через git

```bash
cd "C:/Users/Roman.Gapancov/Desktop/TikTok Parser/Tools/QR_Redirect"
# Отредактировать p/index.html и/или s/index.html
git add . && git commit -m "redirect: /p → max.ru/..."
git push
```

## История проекта

- **2026-04-28 (вечер):** первый деплой на Cloudflare Pages
  (`pwr-redirect.pages.dev`). Не работает в РФ — DPI Роскомнадзора режет
  `*.pages.dev` по SNI в TLS handshake. `ERR_CONNECTION_RESET`.
- **2026-04-28 (поздно):** переезд на GitHub Pages нового аккаунта
  `envilope1337` (`PurePetv2` имел user-level блокировку Actions, поэтому
  Pages не строились). Этот аккаунт работает нормально.
- **Cloudflare проект остался** как резервный — `pwr-redirect.pages.dev`. Можно
  удалить через `npx wrangler pages project delete pwr-redirect`, или оставить
  как fallback на случай если GitHub Pages начнёт резаться у российских
  провайдеров.

## Если в будущем понадобится свой `.ru` домен

Купить `.ru` домен (~200₽/год) на reg.ru → в репо добавить файл `CNAME` с
именем домена → у регистратора прописать DNS-записи:

```
A  185.199.108.153
A  185.199.109.153
A  185.199.110.153
A  185.199.111.153
```

В Settings → Pages → Custom domain → ввести домен → Save.

После активации старые QR на `envilope1337.github.io` **продолжат работать**
(GitHub Pages держит оба URL). Перепечатывать наклейки не надо.
