"""Temalar ve ASCII logo."""

LOGO = r"""
                  -`
                 .o+`
                `ooo/
               `+oooo:
              `+oooooo:
              -+oooooo+:
            `/:-:++oooo+:
           `/++++/+++++++:
          `/++++++++++++++:
         `/+++ooooooooooooo/`
        ./ooosssso++osssssso+`
       .oossssso-````/ossssss+`
      -osssssso.      :ssssssso.
     :osssssss/        osssso+++.
    /ossssssss/        +ssssooo/-
  `/ossssso+/:-        -:/+osssso+-
 `+sso+:-`                 `.-/+oso:
`++:.                           `-/+/
.`                                 `/
""".strip("\n")

# Her tema: gradient duraklari (RGB). Gradient dongusel olarak kullanilir.
THEMES = {
    "aurora":     [(0, 255, 200), (0, 170, 255), (140, 90, 255)],
    "sunset":     [(255, 94, 98), (255, 153, 102), (255, 206, 84)],
    "cyberpunk":  [(255, 0, 200), (120, 0, 255), (0, 240, 255)],
    "catppuccin": [(245, 194, 231), (203, 166, 247), (137, 180, 250), (148, 226, 213)],
    "nord":       [(136, 192, 208), (129, 161, 193), (94, 129, 172)],
    "dracula":    [(255, 121, 198), (189, 147, 249), (139, 233, 253)],
    "matrix":     [(0, 90, 30), (0, 255, 70), (180, 255, 190)],
    "gruvbox":    [(251, 73, 52), (254, 128, 25), (250, 189, 47), (184, 187, 38)],
}
DEFAULT_THEME = "aurora"
