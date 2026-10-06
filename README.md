<h1 align="center">✦ archnova ✦</h1>
<p align="center">Arch Linux için gradient'li, canlı, göz alıcı <code>neofetch</code> alternatifi.</p>

## Özellikler

- 🌈 Truecolor (24-bit) gradient'li Arch logosu ve panel
- 📦 Yuvarlak köşeli, gradient kenarlıklı bilgi kutusu
- 📊 Canlı **CPU / RAM / Disk** barları (yeşil → sarı → kırmızı)
- ⚡ `--live` modu: gradient akar, değerler her saniye güncellenir
- 🎨 8 tema: `aurora` `sunset` `cyberpunk` `catppuccin` `nord` `dracula` `matrix` `gruvbox`
- 🐍 Sıfır bağımlılık, sadece Python standart kütüphanesi
- 🧾 `--json` çıktısı (scriptler için)

## Kurulum

```bash
git clone https://github.com/KULLANICI/archnova && cd archnova
./install.sh            # kullanıcıya kurar (~/.local/bin)
# veya
makepkg -si             # PKGBUILD ile
# veya kurmadan
python -m archnova
```

İkonlar için bir [Nerd Font](https://www.nerdfonts.com) önerilir (`ttf-jetbrains-mono-nerd`). Yoksa `--no-icons` kullan.

## Kullanım

```
archnova                  # tek seferlik
archnova -L               # canlı mod (Ctrl+C ile çık)
archnova -t cyberpunk     # tema seç
archnova -t random        # rastgele tema
archnova -l               # temaları önizle
archnova --no-logo --no-icons
archnova --json
```

Varsayılan temayı değiştirmek için: `export ARCHNOVA_THEME=sunset`

## Proje yapısı

```
archnova/
├── archnova/
│   ├── cli.py       # argümanlar + canlı mod
│   ├── render.py    # gradient, kutu, barlar, logo
│   ├── info.py      # sistem bilgisi toplayıcılar
│   └── themes.py    # temalar + ASCII logo
├── PKGBUILD · install.sh · pyproject.toml · LICENSE
```

## Yeni tema eklemek

`archnova/themes.py` içindeki `THEMES` sözlüğüne RGB durakları ekle:

```python
"benim": [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
```

## Lisans

MIT
