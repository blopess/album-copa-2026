"""
Álbum de Figurinhas Copa 2026 — v9 (Flet 0.85+)
=================================================
CORREÇÃO ESTRUTURAL v9:
  O álbum Panini Copa 2026 NÃO usa numeração sequencial 1-600.
  Cada seleção tem seu próprio prefixo (BRA, ARG, FRA...) e conta de 1 a 20.
  Seção especial FWC tem 9 figurinhas (00 + FWC1..FWC8).
  Seção FIFA Museum tem 11 figurinhas (MUS1..MUS11).
  Total: 980 figurinhas (9 + 11 + 48×20).

  Modelo de dados: ID = "BRA1", "BRA2"... "FWC3", "MUS7" etc.
  Armazenamento: {"stickers": {"BRA1": 0, "BRA2": 1, "BRA3": 2, ...}}

SETOR/GRUPO por continente:
  Especiais: FWC (abertura) + MUS (FIFA Museum)
  Américas:  MEX, CAN, USA, BRA, ARG, URU, COL, CHI, PAR, ECU, HAI, CUW, VEN, PER
  Europa:    GER, FRA, ENG, ESP, POR, ITA, NED, BEL, CRO, SUI, CZE, SCO, TUR,
             SWE, POL, DEN, SRB, BIH, ROU, UKR, GRE, SVN, SVK, HUN, AUT, WAL, IRL
  África:    MAR, SEN, NGA, GHA, CMR, CIV, RSA, EGY, TUN, MLI, ANG
  Ásia/Oceania: JPN, KOR, IRN, KSA, AUS, CHN, THA, QAT, IDN, UZB
"""

import flet as ft
import json
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Paleta global — tema infantil claro
# ─────────────────────────────────────────────────────────────────────────────
C_BG       = "#EEF6FF"
C_SURFACE  = "#FFFFFF"
C_SURFACE2 = "#E8F0FB"
C_WHITE    = "#FFFFFF"
C_GRAY     = "#B8D0E8"
C_GRAY_LT  = "#5A7A96"
C_YELLOW   = "#FFD600"
C_ORANGE   = "#FF6D00"
C_DANGER   = "#E53935"

# ─────────────────────────────────────────────────────────────────────────────
# Paleta por SETOR
# ─────────────────────────────────────────────────────────────────────────────
PALETA = {
    "Especiais":    {"btn_has": "#F9A825", "btn_no": "#FFF9C4", "accent": "#F57F17",
                     "shadow": "#F9A82544", "chip_sel": "#F9A825",
                     "txt_has": "#1A2744", "txt_no": "#E65100"},
    "Américas":     {"btn_has": "#2E7D32", "btn_no": "#C8E6C9", "accent": "#1B5E20",
                     "shadow": "#2E7D3244", "chip_sel": "#43A047",
                     "txt_has": "#FFFFFF", "txt_no": "#2E7D32"},
    "Europa":       {"btn_has": "#6A1B9A", "btn_no": "#E1BEE7", "accent": "#4A148C",
                     "shadow": "#6A1B9A44", "chip_sel": "#7B1FA2",
                     "txt_has": "#FFFFFF", "txt_no": "#6A1B9A"},
    "África":       {"btn_has": "#E65100", "btn_no": "#FFE0B2", "accent": "#BF360C",
                     "shadow": "#E6510044", "chip_sel": "#F4511E",
                     "txt_has": "#FFFFFF", "txt_no": "#E65100"},
    "Ásia/Oceania": {"btn_has": "#AD1457", "btn_no": "#FCE4EC", "accent": "#880E4F",
                     "shadow": "#AD145744", "chip_sel": "#C2185B",
                     "txt_has": "#FFFFFF", "txt_no": "#AD1457"},
}

SETOR_EMOJI = {
    "Todos": "📋", "Especiais": "⭐", "Américas": "🌎",
    "Europa": "🏰", "África": "🌍", "Ásia/Oceania": "🌏",
}
SETORES = ["Todos", "Especiais", "Américas", "Europa", "África", "Ásia/Oceania"]

# ─────────────────────────────────────────────────────────────────────────────
# Estrutura completa do álbum Panini Copa 2026 (980 figurinhas)
# Cada entrada: prefixo → {nome, emoji, setor, qtd}
# qtd=9 para FWC (00+FWC1..FWC8), qtd=11 para MUS, qtd=20 para todas as seleções
# ─────────────────────────────────────────────────────────────────────────────
SECOES = [
    # prefixo,  nome_pt,               emoji,  setor,          qtd
    ("FWC",  "Copa 2026",             "🌍",   "Especiais",    9),
    ("MUS",  "FIFA Museum",           "🏆",   "Especiais",   11),
    ("MEX",  "México",                "🇲🇽",  "Américas",    20),
    ("RSA",  "África do Sul",         "🇿🇦",  "África",      20),
    ("KOR",  "Coreia do Sul",         "🇰🇷",  "Ásia/Oceania",20),
    ("CZE",  "Tchéquia",              "🇨🇿",  "Europa",      20),
    ("CAN",  "Canadá",                "🇨🇦",  "Américas",    20),
    ("BIH",  "Bósnia-Herz.",          "🇧🇦",  "Europa",      20),
    ("QAT",  "Qatar",                 "🇶🇦",  "Ásia/Oceania",20),
    ("SUI",  "Suíça",                 "🇨🇭",  "Europa",      20),
    ("BRA",  "Brasil",                "🇧🇷",  "Américas",    20),
    ("MAR",  "Marrocos",              "🇲🇦",  "África",      20),
    ("HAI",  "Haiti",                 "🇭🇹",  "Américas",    20),
    ("SCO",  "Escócia",               "🏴",   "Europa",      20),
    ("USA",  "EUA",                   "🇺🇸",  "Américas",    20),
    ("PAR",  "Paraguai",              "🇵🇾",  "Américas",    20),
    ("AUS",  "Austrália",             "🇦🇺",  "Ásia/Oceania",20),
    ("TUR",  "Turquia",               "🇹🇷",  "Europa",      20),
    ("GER",  "Alemanha",              "🇩🇪",  "Europa",      20),
    ("CUW",  "Curaçao",               "🇨🇼",  "Américas",    20),
    ("CIV",  "Costa do Marfim",       "🇨🇮",  "África",      20),
    ("ECU",  "Equador",               "🇪🇨",  "Américas",    20),
    ("NED",  "Holanda",               "🇳🇱",  "Europa",      20),
    ("JPN",  "Japão",                 "🇯🇵",  "Ásia/Oceania",20),
    ("SWE",  "Suécia",                "🇸🇪",  "Europa",      20),
    ("ARG",  "Argentina",             "🇦🇷",  "Américas",    20),
    ("ENG",  "Inglaterra",            "🏴",   "Europa",      20),
    ("ESP",  "Espanha",               "🇪🇸",  "Europa",      20),
    ("FRA",  "França",                "🇫🇷",  "Europa",      20),
    ("POR",  "Portugal",              "🇵🇹",  "Europa",      20),
    ("ITA",  "Itália",                "🇮🇹",  "Europa",      20),
    ("BEL",  "Bélgica",               "🇧🇪",  "Europa",      20),
    ("CRO",  "Croácia",               "🇭🇷",  "Europa",      20),
    ("SEN",  "Senegal",               "🇸🇳",  "África",      20),
    ("NGA",  "Nigéria",               "🇳🇬",  "África",      20),
    ("CMR",  "Camarões",              "🇨🇲",  "África",      20),
    ("GHA",  "Gana",                  "🇬🇭",  "África",      20),
    ("URU",  "Uruguai",               "🇺🇾",  "Américas",    20),
    ("COL",  "Colômbia",              "🇨🇴",  "Américas",    20),
    ("IRN",  "Irã",                   "🇮🇷",  "Ásia/Oceania",20),
    ("KSA",  "Arábia Saudita",        "🇸🇦",  "Ásia/Oceania",20),
    ("POL",  "Polônia",               "🇵🇱",  "Europa",      20),
    ("DEN",  "Dinamarca",             "🇩🇰",  "Europa",      20),
    ("SRB",  "Sérvia",                "🇷🇸",  "Europa",      20),
    ("ROU",  "Romênia",               "🇷🇴",  "Europa",      20),
    ("GRE",  "Grécia",                "🇬🇷",  "Europa",      20),
    ("SVN",  "Eslovênia",             "🇸🇮",  "Europa",      20),
    ("UKR",  "Ucrânia",               "🇺🇦",  "Europa",      20),
    ("NZL",  "Nova Zelândia",         "🇳🇿",  "Ásia/Oceania",20),
    ("SVK",  "Eslováquia",             "🇸🇰",  "Europa",      20),
]

# ─────────────────────────────────────────────────────────────────────────────
# Gerar lista de todos os IDs na ordem do álbum
# FWC especial: IDs são "00", "FWC1"..."FWC8"
# Demais:       IDs são "PREFIX1"..."PREFIX20"
# ─────────────────────────────────────────────────────────────────────────────
def _gerar_ids_secao(prefixo: str, qtd: int) -> list[str]:
    if prefixo == "FWC":
        return ["00"] + [f"FWC{i}" for i in range(1, 9)]   # 00 + FWC1..FWC8
    return [f"{prefixo}{i}" for i in range(1, qtd + 1)]

# Dicionário global: ID → {secao_prefixo, secao_nome, emoji, setor, numero}
STICKER_INFO: dict[str, dict] = {}
TODOS_IDS: list[str] = []

for prefixo, nome, emoji, setor, qtd in SECOES:
    ids = _gerar_ids_secao(prefixo, qtd)
    for i, sid in enumerate(ids, 1):
        STICKER_INFO[sid] = {
            "prefixo": prefixo,
            "nome":    nome,
            "emoji":   emoji,
            "setor":   setor,
            "numero":  i,
        }
    TODOS_IDS.extend(ids)

TOTAL = len(TODOS_IDS)  # 980

# índice inverso: prefixo → lista de IDs (na ordem)
SECAO_IDS: dict[str, list[str]] = {}
for prefixo, nome, emoji, setor, qtd in SECOES:
    SECAO_IDS[prefixo] = _gerar_ids_secao(prefixo, qtd)

# ─────────────────────────────────────────────────────────────────────────────
# Persistência
# ─────────────────────────────────────────────────────────────────────────────

def get_data_path() -> Path:
    storage = os.environ.get("FLET_APP_STORAGE_DATA", ".")
    return Path(storage) / "stickers_2026.json"

def load_data() -> dict:
    path = get_data_path()
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            data = raw.get("stickers", {})
            for sid in TODOS_IDS:
                data.setdefault(sid, 0)
            return data
        except Exception:
            pass
    return {sid: 0 for sid in TODOS_IDS}

def save_data(stickers: dict) -> None:
    path = get_data_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"stickers": stickers}, f)

# ─────────────────────────────────────────────────────────────────────────────
# Contagens
# ─────────────────────────────────────────────────────────────────────────────

def count_owned(s):  return sum(1 for v in s.values() if v >= 1)
def count_dupes(s):  return sum(max(0, v - 1) for v in s.values())
def get_dupes_list(s):
    return sorted([(sid, v - 1) for sid, v in s.items() if v >= 2],
                  key=lambda x: TODOS_IDS.index(x[0]) if x[0] in TODOS_IDS else 9999)

def ids_do_setor(setor: str) -> list[str]:
    if setor == "Todos": return TODOS_IDS
    return [sid for sid in TODOS_IDS if STICKER_INFO[sid]["setor"] == setor]

def ids_da_secao(prefixo: str) -> list[str]:
    return SECAO_IDS.get(prefixo, [])

def progress_secao(s: dict, prefixo: str):
    ids = ids_da_secao(prefixo)
    return sum(1 for sid in ids if s.get(sid, 0) >= 1), len(ids)

def get_paleta(sid: str) -> dict:
    setor = STICKER_INFO.get(sid, {}).get("setor", "Especiais")
    return PALETA.get(setor, PALETA["Especiais"])

# ─────────────────────────────────────────────────────────────────────────────
# Botão wide com cor por setor — label = código (ex: "BRA7")
# ─────────────────────────────────────────────────────────────────────────────

def _btn_inner(sid: str, value: int) -> ft.Row:
    has   = value >= 1
    reps  = value - 1 if value > 1 else 0
    cores = get_paleta(sid)
    badge = ft.Container(
        content=ft.Text(f"+{reps}", size=7, weight=ft.FontWeight.BOLD,
                        color="#1A2744"),
        bgcolor=C_ORANGE,
        border_radius=4,
        padding=ft.Padding(left=3, top=1, right=3, bottom=1),
        visible=(reps > 0),
    )
    return ft.Row(
        controls=[
            ft.Text(sid, size=10, weight=ft.FontWeight.BOLD,
                    color=cores["txt_has"] if has else cores["txt_no"],
                    text_align=ft.TextAlign.CENTER, expand=True),
            badge,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=2,
    )

def make_sticker_btn(sid: str, value: int, on_tap, on_long_press) -> ft.Container:
    has   = value >= 1
    cores = get_paleta(sid)
    return ft.Container(
        content=_btn_inner(sid, value),
        bgcolor=cores["btn_has"] if has else cores["btn_no"],
        border_radius=8,
        padding=ft.Padding(left=6, top=0, right=4, bottom=0),
        shadow=[ft.BoxShadow(blur_radius=4,
                             color=cores["shadow"] if has else "#00000022",
                             offset=ft.Offset(0, 2))],
        border=ft.Border.all(width=1,
                             color=cores["accent"] if has else "transparent"),
        on_click=lambda e, s=sid: on_tap(s),
        on_long_press=lambda e, s=sid: on_long_press(s),
    )

def refresh_btn(btn: ft.Container, sid: str, value: int):
    has   = value >= 1
    cores = get_paleta(sid)
    btn.content = _btn_inner(sid, value)
    btn.bgcolor = cores["btn_has"] if has else cores["btn_no"]
    btn.shadow  = [ft.BoxShadow(blur_radius=4,
                                color=cores["shadow"] if has else "#00000022",
                                offset=ft.Offset(0, 2))]
    btn.border  = ft.Border.all(width=1, color=cores["accent"] if has else "transparent")
    btn.update()

# ─────────────────────────────────────────────────────────────────────────────
# App
# ─────────────────────────────────────────────────────────────────────────────

def main(page: ft.Page):
    page.title      = "⚽ Álbum Copa 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor    = C_BG
    page.padding    = 0
    page.spacing    = 0

    stickers: dict                    = load_data()
    btn_refs: dict[str, ft.Container] = {}
    filtro_setor  = ["Todos"]
    filtro_secao  = [None]        # None = todas do setor | prefixo = seção específica
    filtro_status = ["todos"]
    filtro_busca  = [""]
    current_tab   = [0]

    # Criar todos os botões uma única vez
    for sid in TODOS_IDS:
        btn_refs[sid] = make_sticker_btn(sid, stickers[sid], None, None)

    # ── Header refs ────────────────────────────────────────────────────────
    lbl_owned = ft.Text("", size=22, weight=ft.FontWeight.BOLD, color=C_WHITE)
    lbl_dupes = ft.Text("", size=22, weight=ft.FontWeight.BOLD, color=C_YELLOW)
    progress  = ft.ProgressBar(value=0, color=C_YELLOW, bgcolor="rgba(255,255,255,0.3)",
                               border_radius=6, height=8)
    lbl_pct   = ft.Text("", size=11, color=C_WHITE)

    def update_header():
        owned = count_owned(stickers)
        dupes = count_dupes(stickers)
        lbl_owned.value = f"{owned}/{TOTAL}"
        lbl_dupes.value = str(dupes)
        progress.value  = owned / TOTAL
        lbl_pct.value   = f"{owned / TOTAL * 100:.1f}% completo 🏆"
        for w in [lbl_owned, lbl_dupes, progress, lbl_pct]:
            if w.page: w.update()

    # ── GridView wide auto-fit ─────────────────────────────────────────────
    grid_view = ft.GridView(
        controls=[],
        max_extent=90,
        child_aspect_ratio=2.8,
        spacing=4,
        run_spacing=4,
        expand=True,
        padding=ft.Padding(left=8, top=8, right=8, bottom=8),
    )

    def get_ids_visiveis() -> list[str]:
        setor  = filtro_setor[0]
        secao  = filtro_secao[0]
        status = filtro_status[0]
        busca  = filtro_busca[0].strip().upper()

        ids = ids_da_secao(secao) if secao else ids_do_setor(setor)

        if status == "faltam":
            ids = [s for s in ids if stickers.get(s, 0) == 0]
        elif status == "tenho":
            ids = [s for s in ids if stickers.get(s, 0) >= 1]
        elif status == "repetidas":
            ids = [s for s in ids if stickers.get(s, 0) >= 2]

        if busca:
            ids = [s for s in ids if busca in s]

        return ids

    def rebuild_grid():
        ids = get_ids_visiveis()
        grid_view.controls = [btn_refs[s] for s in ids]
        if not ids:
            grid_view.controls = [ft.Container(
                content=ft.Column(controls=[
                    ft.Text("🔍", size=40, text_align=ft.TextAlign.CENTER),
                    ft.Text("Nenhuma figurinha encontrada", size=14,
                            color=C_GRAY_LT, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=40, alignment=ft.Alignment(x=0, y=0),
            )]
        if grid_view.page: grid_view.update()

    # ── Chips de setor ─────────────────────────────────────────────────────
    setor_chips_row = ft.ListView(
        controls=[], horizontal=True, height=44, spacing=6,
        padding=ft.Padding(left=10, top=2, right=10, bottom=2),
    )

    def rebuild_setor_chips():
        setor_chips_row.controls.clear()
        for nome in SETORES:
            emoji   = SETOR_EMOJI.get(nome, "")
            cor_sel = PALETA.get(nome, {}).get("btn_has", C_YELLOW) if nome != "Todos" else C_YELLOW
            setor_chips_row.controls.append(ft.Chip(
                label=ft.Text(f"{emoji} {nome}", size=11, weight=ft.FontWeight.BOLD),
                selected=(filtro_setor[0] == nome),
                bgcolor="#E8F0FB", selected_color=cor_sel,
                show_checkmark=False,
                on_select=lambda e, s=nome: set_setor(s),
            ))
        if setor_chips_row.page: setor_chips_row.update()

    # ── Chips de seção ─────────────────────────────────────────────────────
    secao_chips_row = ft.ListView(
        controls=[], horizontal=True, height=44, spacing=6,
        padding=ft.Padding(left=10, top=2, right=10, bottom=2),
    )

    def rebuild_secao_chips():
        secao_chips_row.controls.clear()
        setor = filtro_setor[0]
        secao_chips_row.controls.append(ft.Chip(
            label=ft.Text("Todas", size=11, weight=ft.FontWeight.BOLD),
            selected=(filtro_secao[0] is None),
            bgcolor="#F0F4F8", selected_color=C_GRAY_LT,
            show_checkmark=False,
            on_select=lambda e: set_secao(None),
        ))
        # Filtrar seções do setor ativo
        secoes_ativas = [(p, n, em, st, q) for p, n, em, st, q in SECOES
                         if st == setor or setor == "Todos"]
        for prefixo, nome, emoji, _, _ in secoes_ativas:
            coladas, total_s = progress_secao(stickers, prefixo)
            cor_sel = PALETA.get(STICKER_INFO.get(ids_da_secao(prefixo)[0], {}).get("setor",""), {}).get("btn_has", C_YELLOW)
            secao_chips_row.controls.append(ft.Chip(
                label=ft.Text(f"{emoji} {nome}  {coladas}/{total_s}", size=11),
                selected=(filtro_secao[0] == prefixo),
                bgcolor="#F0F4F8", selected_color=cor_sel,
                show_checkmark=False,
                on_select=lambda e, p=prefixo: set_secao(p),
            ))
        if secao_chips_row.page: secao_chips_row.update()

    def set_setor(nome):
        filtro_setor[0] = nome
        filtro_secao[0] = None
        rebuild_setor_chips(); rebuild_secao_chips(); rebuild_grid()

    def set_secao(prefixo):
        filtro_secao[0] = prefixo
        rebuild_secao_chips(); rebuild_grid()

    # ── Filtros status + busca ─────────────────────────────────────────────
    dd_status = ft.Dropdown(
        value="todos",
        options=[
            ft.dropdown.Option(key="todos",     text="📋 Todos"),
            ft.dropdown.Option(key="faltam",    text="❌ Faltam"),
            ft.dropdown.Option(key="tenho",     text="✅ Tenho"),
            ft.dropdown.Option(key="repetidas", text="🔄 Repetidas"),
        ],
        border_radius=16, text_size=12, width=145,
        bgcolor=C_SURFACE, border_color=C_GRAY,
    )
    dd_status.on_change = lambda e: (
        filtro_status.__setitem__(0, e.control.value), rebuild_grid()
    )[-1]

    tf_busca = ft.TextField(
        hint_text="🔍  código (ex: BRA7)",
        border_radius=16, text_size=12, height=40,
        bgcolor=C_SURFACE, border_color=C_GRAY,
        content_padding=ft.Padding(left=12, top=4, right=8, bottom=4),
        expand=True,
    )
    tf_busca.on_change = lambda e: (
        filtro_busca.__setitem__(0, e.control.value), rebuild_grid()
    )[-1]

    filter_bar = ft.Container(
        content=ft.Row(
            controls=[dd_status, ft.Container(width=6), tf_busca],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#F0F7FF",
        padding=ft.Padding(left=10, top=6, right=10, bottom=6),
        border=ft.Border(bottom=ft.BorderSide(width=1, color=C_GRAY)),
    )

    # ── Diálogos ───────────────────────────────────────────────────────────
    def show_options_dialog(sid: str):
        value = stickers[sid]
        reps  = value - 1
        info  = STICKER_INFO.get(sid, {})
        cores = get_paleta(sid)

        def do_add(e):    page.pop_dialog(); on_add_repeat(sid)
        def do_remove(e): page.pop_dialog(); show_remove_confirm(sid)
        def do_cancel(e): page.pop_dialog()

        page.show_dialog(ft.AlertDialog(
            modal=True, bgcolor=C_SURFACE,
            title=ft.Row(controls=[
                ft.Text(info.get("emoji", "⚽"), size=22),
                ft.Text(f" {sid} — {info.get('nome','')}", size=15,
                        weight=ft.FontWeight.BOLD, color="#1A2744"),
            ]),
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("✅ Já colada!", size=13,
                                        color=cores["btn_has"],
                                        weight=ft.FontWeight.BOLD),
                        bgcolor=C_SURFACE2, border_radius=8,
                        padding=ft.Padding(left=12, top=8, right=12, bottom=8),
                    ),
                    ft.Text(
                        f"🔄 Repetidas: {reps}" if reps > 0 else "Sem repetidas ainda",
                        size=13, color=C_GRAY_LT,
                    ),
                ],
                spacing=8, tight=True,
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cancelar", color=C_GRAY_LT),
                              on_click=do_cancel),
                ft.TextButton(content=ft.Text("🗑 Remover", color=C_DANGER),
                              on_click=do_remove),
                ft.Button(content=ft.Text("+1 Repetida", color="#1A2744",
                                          weight=ft.FontWeight.BOLD),
                          bgcolor=C_YELLOW, on_click=do_add),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            open=True,
        ))

    def show_remove_confirm(sid: str):
        value = stickers[sid]
        reps  = value - 1
        info  = STICKER_INFO.get(sid, {})

        def do_confirm(e):
            page.pop_dialog()
            stickers[sid] = 0
            save_data(stickers)
            refresh_btn(btn_refs[sid], sid, 0)
            update_header(); rebuild_secao_chips(); rebuild_repeats_col()
            page.show_dialog(ft.SnackBar(
                content=ft.Text(f"Figurinha {sid} removida 🗑", color=C_WHITE),
                bgcolor=C_DANGER, duration=1500, open=True,
            ))

        def do_cancel(e): page.pop_dialog()

        extra = f" e {reps} repetida{'s' if reps > 1 else ''}" if reps > 0 else ""
        page.show_dialog(ft.AlertDialog(
            modal=True, bgcolor=C_SURFACE,
            title=ft.Text("⚠️ Confirmar remoção", size=16, color=C_DANGER),
            content=ft.Text(
                f"Remover {info.get('emoji','')} {sid}{extra}?\nVoltará para cinza.",
                color=C_GRAY_LT, size=13,
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cancelar", color=C_GRAY_LT),
                              on_click=do_cancel),
                ft.Button(content=ft.Text("Remover", color=C_WHITE,
                                          weight=ft.FontWeight.BOLD),
                          bgcolor=C_DANGER, on_click=do_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            open=True,
        ))

    # ── Handlers ───────────────────────────────────────────────────────────
    def on_tap(sid: str):
        if stickers[sid] == 0:
            stickers[sid] = 1
            save_data(stickers)
            refresh_btn(btn_refs[sid], sid, 1)
            update_header(); rebuild_secao_chips()
        else:
            show_options_dialog(sid)

    def on_long_press(sid: str):
        if stickers[sid] > 0:
            show_remove_confirm(sid)

    def on_add_repeat(sid: str):
        stickers[sid] += 1
        save_data(stickers)
        refresh_btn(btn_refs[sid], sid, stickers[sid])
        update_header(); rebuild_repeats_col()

    def on_remove_one_repeat(sid: str):
        if stickers[sid] > 1:
            stickers[sid] -= 1
            save_data(stickers)
            refresh_btn(btn_refs[sid], sid, stickers[sid])
            update_header(); rebuild_repeats_col()

    # Injetar handlers
    for sid in TODOS_IDS:
        btn_refs[sid].on_click      = lambda e, s=sid: on_tap(s)
        btn_refs[sid].on_long_press = lambda e, s=sid: on_long_press(s)

    # ── Aba Repetidas ──────────────────────────────────────────────────────
    repeats_col = ft.Column(controls=[], expand=True,
                            scroll=ft.ScrollMode.AUTO, spacing=8)

    def rebuild_repeats_col():
        repeats_col.controls.clear()
        dupes = get_dupes_list(stickers)

        if not dupes:
            repeats_col.controls.append(ft.Container(
                content=ft.Column(controls=[
                    ft.Text("✅", size=52, text_align=ft.TextAlign.CENTER),
                    ft.Text("Nenhuma repetida ainda!", size=18,
                            weight=ft.FontWeight.BOLD, color="#2E7D32",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Continue colando! 😄", size=13,
                            color=C_GRAY_LT, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                   alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                expand=True, alignment=ft.Alignment(x=0, y=0), padding=40,
            ))
        else:
            repeats_col.controls.append(ft.Container(
                content=ft.Row(controls=[
                    ft.Text("🔄", size=20),
                    ft.Text(f"{len(dupes)} figurinha(s) · "
                            f"{count_dupes(stickers)} cópia(s)",
                            size=13, color=C_GRAY_LT, weight=ft.FontWeight.BOLD),
                ], spacing=8),
                padding=ft.Padding(left=4, top=0, right=4, bottom=4),
            ))
            for sid, reps in dupes:
                info  = STICKER_INFO.get(sid, {})
                cores = get_paleta(sid)
                card = ft.Container(
                    content=ft.Row(controls=[
                        ft.Container(
                            content=ft.Text(sid, size=13, weight=ft.FontWeight.BOLD,
                                            color=cores["txt_has"],
                                            text_align=ft.TextAlign.CENTER),
                            bgcolor=cores["btn_has"], border_radius=10,
                            width=62, height=40,
                            alignment=ft.Alignment(x=0, y=0),
                        ),
                        ft.Container(width=8),
                        ft.Column(controls=[
                            ft.Text(f"+{reps} para trocar", size=13,
                                    weight=ft.FontWeight.BOLD, color=C_ORANGE),
                            ft.Text(f"{info.get('emoji','⚽')} {info.get('nome','')}",
                                    size=10, color=C_GRAY_LT),
                        ], spacing=2, expand=True),
                        ft.Container(
                            content=ft.Column(controls=[
                                ft.Icon(ft.Icons.REMOVE_CIRCLE, color=C_DANGER, size=22),
                                ft.Text("−1", size=9, color=C_DANGER),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
                            on_click=lambda e, s=sid: on_remove_one_repeat(s),
                            border_radius=8,
                            padding=ft.Padding(left=8, top=6, right=8, bottom=6),
                            bgcolor=C_SURFACE2,
                        ),
                    ], alignment=ft.MainAxisAlignment.START,
                       vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=C_SURFACE, border_radius=14,
                    padding=ft.Padding(left=12, top=10, right=12, bottom=10),
                    shadow=[ft.BoxShadow(blur_radius=4, color=cores["shadow"],
                                        offset=ft.Offset(0, 2))],
                    border=ft.Border(left=ft.BorderSide(width=4, color=cores["btn_has"])),
                )
                repeats_col.controls.append(card)

        if repeats_col.page: repeats_col.update()

    # ── Header ─────────────────────────────────────────────────────────────
    header = ft.Container(
        content=ft.Column(controls=[
            ft.Row(controls=[
                ft.Text("⚽", size=20),
                ft.Text("Álbum Copa 2026", size=16,
                        weight=ft.FontWeight.BOLD, color=C_WHITE),
                ft.Text("🏆", size=20),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            ft.Row(controls=[
                ft.Container(content=ft.Column(controls=[
                    ft.Text("✅", size=15, text_align=ft.TextAlign.CENTER),
                    lbl_owned,
                    ft.Text("coladas", size=10, color="rgba(255,255,255,0.7)"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    bgcolor="rgba(255,255,255,0.15)", border_radius=12,
                    padding=ft.Padding(left=14, top=8, right=14, bottom=8),
                    expand=True),
                ft.Container(width=8),
                ft.Container(content=ft.Column(controls=[
                    ft.Text("🔄", size=15, text_align=ft.TextAlign.CENTER),
                    lbl_dupes,
                    ft.Text("para trocar", size=10, color="rgba(255,255,255,0.7)"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    bgcolor="rgba(255,255,255,0.15)", border_radius=12,
                    padding=ft.Padding(left=14, top=8, right=14, bottom=8),
                    expand=True),
            ]),
            ft.Column(controls=[progress, lbl_pct], spacing=4,
                      horizontal_alignment=ft.CrossAxisAlignment.END),
        ], spacing=10),
        bgcolor="#1565C0",
        padding=ft.Padding(left=16, top=12, right=16, bottom=12),
        border=ft.Border(bottom=ft.BorderSide(width=3, color=C_YELLOW)),
    )

    # ── Views ──────────────────────────────────────────────────────────────
    album_view = ft.Container(
        content=ft.Column(controls=[
            ft.Container(content=setor_chips_row, bgcolor="#E8F0FB",
                         border=ft.Border(bottom=ft.BorderSide(width=1, color=C_GRAY))),
            ft.Container(content=secao_chips_row, bgcolor=C_SURFACE,
                         border=ft.Border(bottom=ft.BorderSide(width=1, color=C_GRAY))),
            filter_bar,
            ft.Container(content=grid_view, expand=True),
        ], spacing=0, expand=True),
        expand=True, visible=True,
    )

    repeats_view = ft.Container(
        content=ft.Column(controls=[
            ft.Container(content=ft.Text("🔄 Figurinhas para trocar", size=15,
                                         weight=ft.FontWeight.BOLD, color=C_ORANGE),
                         padding=ft.Padding(left=16, top=12, right=16, bottom=8)),
            ft.Container(content=repeats_col,
                         padding=ft.Padding(left=12, top=0, right=12, bottom=8),
                         expand=True),
        ], spacing=0, expand=True),
        expand=True, visible=False,
    )

    def on_nav(e):
        idx = e.control.selected_index
        current_tab[0] = idx
        if idx == 0:
            album_view.visible = True; repeats_view.visible = False
        else:
            album_view.visible = False; repeats_view.visible = True
            rebuild_repeats_col()
        album_view.update(); repeats_view.update()

    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.GRID_VIEW,  label="Álbum"),
            ft.NavigationBarDestination(icon=ft.Icons.SWAP_HORIZ, label="Repetidas"),
        ],
        selected_index=0, bgcolor="#FFFFFF",
        indicator_color=C_YELLOW, on_change=on_nav,
    )

    page.add(ft.Column(controls=[
        header,
        ft.Stack(controls=[album_view, repeats_view], expand=True),
        nav,
    ], spacing=0, expand=True))

    update_header()
    rebuild_setor_chips()
    rebuild_secao_chips()
    rebuild_grid()


if __name__ == "__main__":
    ft.app(target=main)
