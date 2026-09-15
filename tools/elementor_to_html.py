#!/usr/bin/env python3
"""Converte o export JSON de uma pagina Elementor em HTML/CSS estatico.

Le tools/source/elementor-export.json e escreve index.html + assets/css/page.css.
As folhas assets/css/base.css e assets/js/app.js sao escritas a mao e replicam
o comportamento do runtime do Elementor (containers flex, carrossel, acordeao,
off-canvas, formulario).

    python3 tools/elementor_to_html.py
"""

from __future__ import annotations

import html
import json
import os
import re
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "tools", "source", "elementor-export.json")
VIDEOS = os.path.join(ROOT, "tools", "source", "presto-videos.json")
ASSET_MAP = os.path.join(ROOT, "tools", "source", "asset-map.json")
OUT_HTML = os.path.join(ROOT, "index.html")
OUT_CSS = os.path.join(ROOT, "assets", "css", "page.css")

# Breakpoints ativos no site original (os restantes estao desligados no kit).
BREAKPOINTS = OrderedDict([("", None), ("_tablet", 1024), ("_mobile", 767)])

# Icones Font Awesome usados na pagina, ja descarregados para assets/icons.
FA_FILES = {
    "far fa-times-circle": "fa-circle-xmark.svg",
    "far fa-check-circle": "fa-circle-check.svg",
    "fas fa-rocket": "fa-rocket.svg",
    "far fa-envelope": "fa-envelope.svg",
    "fas fa-times": "fa-xmark.svg",
    "far fa-chart-bar": "fa-chart-bar.svg",
    "fab fa-whatsapp": "fa-whatsapp.svg",
}


# --------------------------------------------------------------------------
# helpers de valores
# --------------------------------------------------------------------------


def _num(value):
    """Devolve o valor numerico de uma dimensao Elementor, ou None se vazia."""
    if value is None or value == "":
        return None
    return value


def size(value):
    """{'unit': 'px', 'size': 70} -> '70px'. Unidades custom trazem a expressao."""
    if not isinstance(value, dict):
        return None
    unit = value.get("unit") or "px"
    raw = _num(value.get("size"))
    if unit == "custom":
        return str(value.get("size") or "").strip() or None
    if raw is None:
        return None
    return f"{raw}{unit}"


def box(value):
    """{'unit':'px','top':'50',...} -> '50px 0px 50px 0px'."""
    if not isinstance(value, dict):
        return None
    unit = value.get("unit") or "px"
    sides = [value.get(k) for k in ("top", "right", "bottom", "left")]
    if all(s in (None, "") for s in sides):
        return None
    if unit == "custom":
        return " ".join(str(s or "0") for s in sides)
    return " ".join(f"{s if s not in (None, '') else '0'}{unit}" for s in sides)


def shadow(value):
    if not isinstance(value, dict):
        return None
    return "{h}px {v}px {b}px {s}px {c}".format(
        h=value.get("horizontal", 0),
        v=value.get("vertical", 0),
        b=value.get("blur", 0),
        s=value.get("spread", 0),
        c=value.get("color", "rgba(0,0,0,.5)"),
    )


def font_stack(family):
    if not family:
        return None
    return f'"{family}", system-ui, -apple-system, "Segoe UI", sans-serif'


def gradient(settings, prefix=""):
    """Constroi um linear/radial-gradient a partir das chaves background_* do Elementor."""
    p = prefix
    color_a = settings.get(f"{p}color") or "#ffffff"
    color_b = settings.get(f"{p}color_b") or "#f2295b"
    stop_a = size(settings.get(f"{p}color_stop")) or "0%"
    stop_b = size(settings.get(f"{p}color_b_stop")) or "100%"
    if settings.get(f"{p}gradient_type") == "radial":
        pos = settings.get(f"{p}gradient_position") or "center center"
        return f"radial-gradient(at {pos}, {color_a} {stop_a}, {color_b} {stop_b})"
    angle = size(settings.get(f"{p}gradient_angle")) or "180deg"
    return f"linear-gradient({angle}, {color_a} {stop_a}, {color_b} {stop_b})"


def local_asset(url, asset_map):
    """Troca um URL do WordPress pelo ficheiro local equivalente."""
    if not url:
        return url
    return asset_map.get(url, url)


def css_asset(url, asset_map):
    """Como local_asset, mas relativo a assets/css/ (onde a folha e servida)."""
    path = local_asset(url, asset_map)
    if path.startswith("assets/"):
        return "../" + path[len("assets/"):]
    return path



_FA_CACHE = {}


def load_fa_icon(name):
    """Le o SVG do Font Awesome em assets/icons e prepara-o para ser embutido."""
    file_name = FA_FILES.get(name)
    if not file_name:
        return None
    if file_name not in _FA_CACHE:
        path = os.path.join(ROOT, "assets", "icons", file_name)
        if not os.path.exists(path):
            _FA_CACHE[file_name] = None
        else:
            with open(path, encoding="utf-8") as fh:
                svg = fh.read()
            svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
            svg = svg.replace("<svg ", '<svg fill="currentColor" aria-hidden="true" focusable="false" ', 1)
            _FA_CACHE[file_name] = svg
    return _FA_CACHE[file_name]


# --------------------------------------------------------------------------
# recolha de CSS
# --------------------------------------------------------------------------


class Sheet:
    """Acumula regras por breakpoint, preservando a ordem de insercao."""

    def __init__(self):
        self.rules = OrderedDict((bp, OrderedDict()) for bp in BREAKPOINTS)
        self.raw = []          # custom_css com `selector` resolvido
        self.globals = []      # custom_css sem `selector` (deduplicado)
        self._seen_global = set()

    def add(self, selector, props, bp=""):
        if not props:
            return
        bucket = self.rules[bp].setdefault(selector, OrderedDict())
        for prop, value in props.items():
            if value is None or value == "":
                continue
            bucket[prop] = value

    def add_custom(self, css, element_selector):
        css = (css or "").strip()
        if not css:
            return
        if "selector" in css:
            self.raw.append(re.sub(r"\bselector\b", element_selector, css))
        else:
            key = re.sub(r"\s+", " ", css)
            if key not in self._seen_global:
                self._seen_global.add(key)
                self.globals.append(css)

    def render(self):
        out = ["/* Gerado por tools/elementor_to_html.py — nao editar a mao. */\n"]
        for bp, width in BREAKPOINTS.items():
            rules = self.rules[bp]
            if not rules:
                continue
            body = []
            for selector, props in rules.items():
                if not props:
                    continue
                decls = "".join(f"\n  {k}: {v};" for k, v in props.items())
                body.append(f"{selector} {{{decls}\n}}")
            if not body:
                continue
            if width is None:
                out.append("\n".join(body))
            else:
                inner = "\n".join(body)
                inner = "\n".join("  " + line if line else line for line in inner.split("\n"))
                out.append(f"@media (max-width: {width}px) {{\n{inner}\n}}")
        if self.globals:
            out.append("/* ---- CSS global vindo dos widgets (custom_css sem `selector`) ---- */")
            out.extend(self.globals)
        if self.raw:
            out.append("/* ---- custom_css por elemento ---- */")
            out.extend(self.raw)
        return "\n\n".join(out) + "\n"


# --------------------------------------------------------------------------
# conversor
# --------------------------------------------------------------------------


class Converter:
    def __init__(self, data, asset_map, videos):
        self.data = data
        self.asset_map = asset_map
        self.videos = videos
        self.sheet = Sheet()
        self.video_cursor = 0
        self.has_h1 = False

    # -- estilos comuns a qualquer elemento (chaves com prefixo `_`) --------

    def common_styles(self, el, sel):
        s = el.get("settings", {})
        for bp in BREAKPOINTS:
            props = OrderedDict()
            props["padding"] = box(s.get(f"_padding{bp}"))
            props["margin"] = box(s.get(f"_margin{bp}"))
            props["align-self"] = s.get(f"_flex_align_self{bp}")
            props["width"] = size(s.get(f"_element_width{bp}"))
            if s.get(f"_border_border{bp}"):
                props["border-style"] = s.get(f"_border_border{bp}")
                props["border-width"] = box(s.get(f"_border_width{bp}"))
                props["border-color"] = s.get(f"_border_color{bp}")
            props["border-radius"] = box(s.get(f"_border_radius{bp}"))
            bg = s.get(f"_background_background{bp}")
            if bg == "classic":
                props["background-color"] = s.get(f"_background_color{bp}")
            elif bg == "gradient":
                props["background-image"] = gradient(s, "_background_")
            elif s.get(f"_background_color{bp}"):
                props["background-color"] = s.get(f"_background_color{bp}")
            if s.get(f"_box_shadow_box_shadow_type{bp}") == "yes":
                props["box-shadow"] = shadow(s.get(f"_box_shadow_box_shadow{bp}"))
            self.sheet.add(sel, props, bp)

        if s.get("_position"):
            self.sheet.add(sel, {"position": s["_position"], "z-index": s.get("_z_index")})
        elif s.get("_z_index"):
            self.sheet.add(sel, {"z-index": s.get("_z_index")})
        self.sheet.add_custom(s.get("custom_css"), sel)

    # -- tipografia --------------------------------------------------------

    def typography(self, s, sel, prefix=""):
        p = prefix
        for bp in BREAKPOINTS:
            props = OrderedDict()
            props["font-family"] = font_stack(s.get(f"{p}typography_font_family{bp}"))
            props["font-size"] = size(s.get(f"{p}typography_font_size{bp}"))
            props["font-weight"] = s.get(f"{p}typography_font_weight{bp}")
            props["font-style"] = s.get(f"{p}typography_font_style{bp}")
            props["line-height"] = size(s.get(f"{p}typography_line_height{bp}"))
            props["letter-spacing"] = size(s.get(f"{p}typography_letter_spacing{bp}"))
            props["text-transform"] = s.get(f"{p}typography_text_transform{bp}")
            props["text-decoration"] = s.get(f"{p}typography_text_decoration{bp}")
            self.sheet.add(sel, props, bp)

    # -- containers --------------------------------------------------------

    def container_styles(self, el, sel, top_level):
        s = el.get("settings", {})
        boxed = s.get("content_width", "boxed") != "full"
        inner = f"{sel} > .e-con-inner" if boxed else sel

        for bp in BREAKPOINTS:
            box_props = OrderedDict()
            box_props["padding"] = box(s.get(f"padding{bp}"))
            box_props["margin"] = box(s.get(f"margin{bp}"))
            box_props["min-height"] = size(s.get(f"min_height{bp}"))
            box_props["height"] = size(s.get(f"height{bp}"))
            width = size(s.get(f"width{bp}"))
            if width:
                box_props["width"] = width
                if top_level:
                    box_props["max-width"] = f"min(100%, {width})"
            if s.get(f"border_border{bp}"):
                box_props["border-style"] = s.get(f"border_border{bp}")
                box_props["border-width"] = box(s.get(f"border_width{bp}"))
                box_props["border-color"] = s.get(f"border_color{bp}")
            box_props["border-radius"] = box(s.get(f"border_radius{bp}"))
            if s.get(f"box_shadow_box_shadow_type{bp}") == "yes":
                box_props["box-shadow"] = shadow(s.get(f"box_shadow_box_shadow{bp}"))
            box_props["overflow"] = s.get(f"overflow{bp}")
            box_props["align-self"] = s.get(f"_flex_align_self{bp}")

            bg = s.get(f"background_background{bp}")
            if bg == "gradient":
                box_props["background-image"] = gradient(s, "background_")
            elif bg == "classic" or s.get(f"background_color{bp}"):
                box_props["background-color"] = s.get(f"background_color{bp}")
            image = s.get(f"background_image{bp}")
            if isinstance(image, dict) and image.get("url"):
                url = css_asset(image["url"], self.asset_map)
                box_props["background-image"] = f"url('{url}')"
                box_props["background-size"] = s.get(f"background_size{bp}") or "cover"
                box_props["background-position"] = s.get(f"background_position{bp}") or "center center"
                box_props["background-repeat"] = s.get(f"background_repeat{bp}") or "no-repeat"
            self.sheet.add(sel, box_props, bp)

            flex = OrderedDict()
            if s.get("container_type") == "grid":
                cols = s.get(f"grid_columns_grid{bp}")
                rows = s.get(f"grid_rows_grid{bp}")
                if cols or rows or bp == "":
                    flex["display"] = "grid"
                if isinstance(cols, dict) and _num(cols.get("size")) is not None:
                    flex["grid-template-columns"] = f"repeat({cols['size']}, 1fr)"
                if isinstance(rows, dict) and _num(rows.get("size")) is not None:
                    flex["grid-template-rows"] = f"repeat({rows['size']}, auto)"
                flex["justify-content"] = s.get(f"grid_justify_content{bp}")
                flex["align-items"] = s.get(f"grid_align_items{bp}")
            else:
                flex["flex-direction"] = s.get(f"flex_direction{bp}")
                flex["justify-content"] = s.get(f"flex_justify_content{bp}")
                flex["align-items"] = s.get(f"flex_align_items{bp}")
                flex["flex-wrap"] = s.get(f"flex_wrap{bp}")
            gap = s.get(f"flex_gap{bp}")
            if isinstance(gap, dict):
                unit = gap.get("unit") or "px"
                row, col = gap.get("row"), gap.get("column")
                if row not in (None, "") or col not in (None, ""):
                    flex["gap"] = f"{row or 0}{unit} {col or 0}{unit}"
            if boxed:
                bw = size(s.get(f"boxed_width{bp}"))
                if bw:
                    flex["max-width"] = bw
            self.sheet.add(inner, flex, bp)

        # Comportamentos que o Elementor aplica por omissao abaixo de 767px:
        # a largura volta a 100%, as linhas quebram e as grelhas ficam a 1 coluna.
        if size(s.get("width")) and not size(s.get("width_mobile")):
            self.sheet.add(sel, {"width": "100%", "max-width": "100%"}, "_mobile")
        direction = s.get("flex_direction_mobile") or s.get("flex_direction") or ""
        if direction.startswith("row") and not s.get("flex_wrap_mobile"):
            self.sheet.add(inner, {"flex-wrap": "wrap"}, "_mobile")
        if s.get("container_type") == "grid":
            if not s.get("grid_columns_grid_mobile"):
                self.sheet.add(inner, {"grid-template-columns": "repeat(1, 1fr)"}, "_mobile")
            # O export nao traz valor para tablet, e manter 4 colunas a 768px
            # fazia o conteudo transbordar; a 2 colunas o bloco cabe.
            cols = s.get("grid_columns_grid") or {}
            if not s.get("grid_columns_grid_tablet") and (cols.get("size") or 0) > 2:
                self.sheet.add(inner, {"grid-template-columns": "repeat(2, 1fr)"}, "_tablet")

        # sobreposicao (background overlay) -> pseudo-elemento ::before
        overlay = OrderedDict()
        kind = s.get("background_overlay_background")
        if kind == "gradient":
            overlay["background-image"] = gradient(s, "background_overlay_")
        elif kind == "classic":
            overlay["background-color"] = s.get("background_overlay_color")
        ov_img = s.get("background_overlay_image")
        if isinstance(ov_img, dict) and ov_img.get("url"):
            url = css_asset(ov_img["url"], self.asset_map)
            overlay["background-image"] = f"url('{url}')"
            overlay["background-size"] = s.get("background_overlay_size") or "cover"
            xpos, ypos = size(s.get("background_overlay_xpos")), size(s.get("background_overlay_ypos"))
            if xpos or ypos:
                overlay["background-position"] = f"{xpos or '0px'} {ypos or '0px'}"
            else:
                overlay["background-position"] = s.get("background_overlay_position") or "center center"
            overlay["background-repeat"] = s.get("background_overlay_repeat") or "no-repeat"
        if overlay:
            opacity = size(s.get("background_overlay_opacity"))
            overlay["opacity"] = opacity.replace("px", "") if opacity else "0.5"
            overlay["border-radius"] = "inherit"
            overlay["display"] = "block"
            self.sheet.add(f"{sel}::before", overlay)

        if s.get("position") == "absolute" or s.get("position") == "fixed":
            pos = OrderedDict(position=s["position"])
            if s.get("_offset_orientation_h") == "end":
                pos["right"] = size(s.get("_offset_x_end")) or "0"
                pos["left"] = "auto"
            else:
                pos["left"] = size(s.get("_offset_x")) or "0"
            if s.get("_offset_orientation_v") == "end":
                pos["bottom"] = size(s.get("_offset_y_end")) or "0"
            else:
                pos["top"] = size(s.get("_offset_y")) or "0"
            pos["z-index"] = s.get("z_index")
            self.sheet.add(sel, pos)
        elif s.get("z_index"):
            self.sheet.add(sel, {"z-index": s["z_index"]})

        # estados :hover
        hover = OrderedDict()
        if s.get("background_hover_background") == "gradient":
            hover["background-image"] = gradient(s, "background_hover_")
        elif s.get("background_hover_color"):
            hover["background-color"] = s["background_hover_color"]
        if s.get("border_hover_border"):
            hover["border-style"] = s["border_hover_border"]
            hover["border-width"] = box(s.get("border_hover_width"))
            hover["border-color"] = s.get("border_hover_color")
        if hover:
            transition = size(s.get("border_hover_transition"))
            if transition:
                self.sheet.add(sel, {"transition": f"all {transition.replace('px', 's')} ease"})
            self.sheet.add(f"{sel}:hover", hover)

        return boxed

    # -- widgets -----------------------------------------------------------

    def icon_svg(self, icon, extra_class="icon"):
        """Devolve markup para um icone Elementor (Font Awesome ou SVG do media library).

        Os icones Font Awesome sao embutidos como SVG com fill=currentColor: fica
        tudo num so pedido e a cor herda do CSS, sem mascaras nem webfonts.
        """
        if not isinstance(icon, dict):
            return ""
        value = icon.get("value")
        if isinstance(value, dict) and value.get("url"):
            url = local_asset(value["url"], self.asset_map)
            return f'<img class="{extra_class}" src="{url}" alt="" aria-hidden="true">'
        if isinstance(value, str) and value:
            markup = load_fa_icon(value)
            if markup:
                return markup.replace("<svg ", f'<svg class="{extra_class}" ', 1)
        return ""

    def widget_heading(self, el, sel):
        s = el.get("settings", {})
        tag = s.get("header_size") or "h2"
        if tag not in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "span"):
            tag = "h2"
        # O export nao traz nenhum h1 (no WordPress o tema tratava do titulo da
        # pagina). Como agora a pagina e autonoma, o primeiro titulo sobe a h1.
        if not self.has_h1 and not s.get("header_size"):
            tag = "h1"
            self.has_h1 = True
        title = s.get("title", "")
        self.typography(s, f"{sel} .e-heading")
        for bp in BREAKPOINTS:
            self.sheet.add(
                sel,
                {"text-align": s.get(f"align{bp}"), "color": s.get(f"title_color{bp}")},
                bp,
            )
        link = s.get("link") or {}
        inner = title
        if link.get("url"):
            target = ' target="_blank" rel="noopener"' if link.get("is_external") else ""
            inner = f'<a href="{html.escape(link["url"], quote=True)}"{target}>{title}</a>'
        return f'<{tag} class="e-heading">{inner}</{tag}>'

    def widget_text_editor(self, el, sel):
        s = el.get("settings", {})
        self.typography(s, sel)
        for bp in BREAKPOINTS:
            self.sheet.add(sel, {"text-align": s.get(f"align{bp}"), "color": s.get(f"text_color{bp}")}, bp)
        body = s.get("editor", "")
        if "<" not in body:
            body = f"<p>{body}</p>"
        return f'<div class="e-text">{body}</div>'

    def widget_button(self, el, sel):
        s = el.get("settings", {})
        link = s.get("link") or {}
        url = link.get("url") or "#"
        url = self.asset_map.get(url, url)
        target = ' target="_blank" rel="noopener"' if link.get("is_external") else ""
        btn = f"{sel} .e-button"
        self.typography(s, btn)

        for bp in BREAKPOINTS:
            props = OrderedDict()
            props["padding"] = box(s.get(f"text_padding{bp}"))
            props["border-radius"] = box(s.get(f"border_radius{bp}"))
            props["color"] = s.get(f"button_text_color{bp}")
            if s.get(f"background_color_b{bp}"):
                props["background-image"] = gradient(s, "background_")
                props["background-color"] = "transparent"
            elif s.get(f"background_color{bp}"):
                props["background-color"] = s.get(f"background_color{bp}")
            if s.get(f"button_box_shadow_box_shadow_type{bp}") == "yes":
                props["box-shadow"] = shadow(s.get(f"button_box_shadow_box_shadow{bp}"))
            self.sheet.add(btn, props, bp)
            self.sheet.add(sel, {"text-align": s.get(f"align{bp}")}, bp)

        if s.get("button_hover_box_shadow_box_shadow_type") == "yes":
            self.sheet.add(f"{btn}:hover", {"box-shadow": shadow(s.get("button_hover_box_shadow_box_shadow"))})
        if s.get("button_background_hover_color"):
            self.sheet.add(f"{btn}:hover", {"background-color": s["button_background_hover_color"]})
        if s.get("icon_align") == "row-reverse":
            self.sheet.add(btn, {"flex-direction": "row-reverse"})

        icon = self.icon_svg(s.get("selected_icon"), "e-button-icon icon")
        text = s.get("text", "")
        return (
            f'<a class="e-button" href="{html.escape(url, quote=True)}"{target}>'
            f'{icon}<span class="e-button-text">{text}</span></a>'
        )

    def widget_image(self, el, sel):
        s = el.get("settings", {})
        image = s.get("image") or {}
        url = local_asset(image.get("url", ""), self.asset_map)
        alt = html.escape(image.get("alt") or "", quote=True)
        img = f"{sel} img"
        for bp in BREAKPOINTS:
            props = OrderedDict()
            props["width"] = size(s.get(f"width{bp}"))
            props["height"] = size(s.get(f"height{bp}"))
            props["object-fit"] = s.get(f"object-fit{bp}")
            props["object-position"] = s.get(f"object-position{bp}")
            props["border-radius"] = box(s.get(f"image_border_radius{bp}"))
            self.sheet.add(img, props, bp)
        if s.get("height") or s.get("object-fit"):
            self.sheet.add(img, {"max-width": "100%"})
        link = s.get("link") or {}
        tag = f'<img src="{url}" alt="{alt}" loading="lazy" decoding="async">'
        if link.get("url"):
            tag = f'<a href="{html.escape(link["url"], quote=True)}">{tag}</a>'
        return tag

    def widget_icon_list(self, el, sel):
        s = el.get("settings", {})
        inline = s.get("view") == "inline"
        items = []
        for item in s.get("icon_list", []):
            icon = self.icon_svg(item.get("selected_icon"), "e-list-icon icon")
            text = item.get("text", "")
            link = item.get("link") or {}
            body = f'<span class="e-list-text">{text}</span>'
            if link.get("url"):
                body = f'<a href="{html.escape(link["url"], quote=True)}">{body}</a>'
            items.append(f'<li class="e-list-item">{icon}{body}</li>')

        cls = "e-list" + (" e-list-inline" if inline else "")
        self.typography(s, f"{sel} .e-list-item", prefix="icon_")
        for bp in BREAKPOINTS:
            self.sheet.add(f"{sel} .e-list-item", {"color": s.get(f"text_color{bp}")}, bp)
            self.sheet.add(
                f"{sel} .e-list-icon",
                {
                    "color": s.get(f"icon_color{bp}"),
                    "width": size(s.get(f"icon_size{bp}")),
                    "height": size(s.get(f"icon_size{bp}")),
                },
                bp,
            )
            gap = size(s.get(f"space_between{bp}"))
            if gap:
                self.sheet.add(f"{sel} .{cls.split()[0]}", {"gap": gap}, bp)
            self.sheet.add(f"{sel} .e-list", {"justify-content": s.get(f"icon_align{bp}")}, bp)
        if s.get("icon_self_vertical_align"):
            self.sheet.add(f"{sel} .e-list-icon", {"align-self": s["icon_self_vertical_align"]})
        if s.get("icon_align") == "row-reverse":
            self.sheet.add(f"{sel} .e-list-item", {"flex-direction": "row-reverse"})
        return f'<ul class="{cls}">{"".join(items)}</ul>'

    def widget_rating(self, el, sel):
        s = el.get("settings", {})
        value = float(s.get("rating_value") or 5)
        stars = []
        for i in range(1, 6):
            fill = max(0.0, min(1.0, value - (i - 1)))
            stars.append(f'<span class="e-star" style="--fill:{fill*100:.0f}%"></span>')
        return f'<div class="e-rating" role="img" aria-label="{value} em 5">{"".join(stars)}</div>'

    def widget_video(self, el, sel, index=None):
        """Substitui presto_video / [presto_player] por uma facade YouTube sem dependencias."""
        if index is None:
            index = self.video_cursor
            self.video_cursor += 1
        if index >= len(self.videos):
            return '<div class="e-video-missing">Vídeo indisponível</div>'
        video = self.videos[index]
        vid = video["video_id"]
        poster = local_asset(video.get("poster") or "", self.asset_map)
        title = html.escape(video.get("title") or "Vídeo", quote=True)
        style = f' style="background-image:url(\'{poster}\')"' if poster else ""
        return (
            f'<div class="e-video" data-video="{vid}" role="button" tabindex="0" '
            f'aria-label="Reproduzir: {title}"{style}>'
            f'<span class="e-video-play" aria-hidden="true"></span>'
            f"</div>"
        )

    def widget_form(self, el, sel):
        s = el.get("settings", {})
        rows = []
        for field in s.get("form_fields", []):
            name = field.get("custom_id") or field.get("_id")
            label = field.get("field_label") or ""
            placeholder = field.get("placeholder") or ""
            required = field.get("required") == "true"
            ftype = field.get("field_type") or "text"
            req_mark = ' <span class="e-req">*</span>' if required else ""
            req_attr = " required" if required else ""
            if ftype == "acceptance":
                text = field.get("acceptance_text") or ""
                rows.append(
                    f'<label class="e-field e-field-check">'
                    f'<input type="checkbox" name="{name}"{req_attr}>'
                    f'<span>{text}</span></label>'
                )
                continue
            if ftype == "textarea":
                control = f'<textarea name="{name}" rows="4" placeholder="{html.escape(placeholder, quote=True)}"{req_attr}></textarea>'
            else:
                input_type = {"tel": "tel", "email": "email"}.get(ftype, "text")
                control = (
                    f'<input type="{input_type}" name="{name}" '
                    f'placeholder="{html.escape(placeholder, quote=True)}"{req_attr}>'
                )
            rows.append(f'<label class="e-field"><span class="e-label">{label}{req_mark}</span>{control}</label>')

        webhook = s.get("webhooks") or ""
        button = s.get("button_text") or "Enviar"
        self.typography(s, f"{sel} .e-form-submit", prefix="button_")
        self.sheet.add(
            f"{sel} .e-form-submit",
            {
                "background-color": s.get("button_background_color"),
                "border-radius": box(s.get("button_border_radius")),
            },
        )
        self.sheet.add(f"{sel} .e-label", {"color": s.get("label_color")})
        self.sheet.add(f"{sel} .e-field input, " + f"{sel} .e-field textarea", {"border-color": s.get("field_border_color")})
        gap_row = size(s.get("row_gap")) or "12px"
        gap_col = size(s.get("column_gap")) or "11px"
        self.sheet.add(f"{sel} .e-form", {"gap": f"{gap_row} {gap_col}"})
        self.sheet.add_custom(s.get("custom_css"), sel)

        return (
            f'<form class="e-form" data-webhook="{html.escape(webhook, quote=True)}" novalidate>'
            + "".join(rows)
            + f'<button class="e-form-submit" type="submit">{button}</button>'
            + f'<p class="e-form-msg" role="status" aria-live="polite"></p>'
            + "</form>"
        )

    def widget_accordion(self, el, sel):
        s = el.get("settings", {})
        items = s.get("items", [])
        panels = []
        for idx, item in enumerate(items):
            child = el.get("elements", [])[idx] if idx < len(el.get("elements", [])) else None
            body = self.render_element(child, top_level=False) if child else ""
            panels.append(
                f'<details class="e-acc-item">'
                f'<summary class="e-acc-title">{item.get("item_title", "")}'
                f'<span class="e-acc-icon" aria-hidden="true"></span></summary>'
                f'<div class="e-acc-panel">{body}</div>'
                f"</details>"
            )
        self.typography(s, f"{sel} .e-acc-title", prefix="title_")
        self.sheet.add(f"{sel} .e-acc-title", {"color": s.get("normal_title_color")})
        self.sheet.add(f"{sel} .e-acc-title:hover", {"color": s.get("hover_title_color")})
        self.sheet.add(f"{sel} .e-acc-item[open] .e-acc-title", {"color": s.get("active_title_color")})
        self.sheet.add(f"{sel} .e-acc-icon", {"background-color": s.get("normal_icon_color")})
        self.sheet.add(f"{sel} .e-acc-item[open] .e-acc-icon", {"background-color": s.get("active_icon_color")})
        gap = size(s.get("accordion_item_title_space_between"))
        if gap:
            self.sheet.add(f"{sel} .e-acc", {"gap": gap})
        if s.get("accordion_border_normal_border"):
            self.sheet.add(
                f"{sel} .e-acc-item",
                {
                    "border-style": s.get("accordion_border_normal_border"),
                    "border-width": box(s.get("accordion_border_normal_width")),
                    "border-color": s.get("accordion_border_normal_color"),
                },
            )
        return f'<div class="e-acc">{"".join(panels)}</div>'

    def widget_carousel(self, el, sel):
        s = el.get("settings", {})
        slides = [self.render_element(child, top_level=False) for child in el.get("elements", [])]
        per_view = int(s.get("slides_to_show") or 3)
        scroll_by = int(s.get("slides_to_scroll") or 1)
        autoplay = int(s.get("autoplay_speed") or 0)
        speed = int(s.get("speed") or 500)
        gap = size(s.get("image_spacing_custom")) or "20px"
        self.sheet.add(sel, {"--slides": str(per_view), "--slide-gap": gap})
        for bp in BREAKPOINTS:
            self.sheet.add(f"{sel} .e-carousel-track", {"padding": box(s.get(f"content_padding{bp}"))}, bp)
        if s.get("arrow_normal_color"):
            self.sheet.add(f"{sel} .e-carousel-nav", {"color": s["arrow_normal_color"]})
        if s.get("arrow_hover_color"):
            self.sheet.add(f"{sel} .e-carousel-nav:hover", {"color": s["arrow_hover_color"]})
        slide_html = "".join(f'<div class="e-slide">{slide}</div>' for slide in slides)
        return (
            f'<div class="e-carousel" data-per-view="{per_view}" data-scroll-by="{scroll_by}" '
            f'data-autoplay="{autoplay}" data-speed="{speed}">'
            f'<button class="e-carousel-nav e-carousel-prev" type="button" aria-label="Anterior"></button>'
            f'<div class="e-carousel-viewport"><div class="e-carousel-track">{slide_html}</div></div>'
            f'<button class="e-carousel-nav e-carousel-next" type="button" aria-label="Seguinte"></button>'
            f"</div>"
        )

    def widget_offcanvas(self, el, sel):
        s = el.get("settings", {})
        body = "".join(self.render_element(child, top_level=False) for child in el.get("elements", []))
        panel = f"{sel} .e-modal-panel"
        for bp in BREAKPOINTS:
            self.sheet.add(panel, {"width": size(s.get(f"width{bp}"))}, bp)
        self.sheet.add(panel, {"border-radius": box(s.get("border_radius")), "height": s.get("height")})
        return (
            f'<div class="e-modal" id="form" hidden>'
            f'<div class="e-modal-backdrop" data-close></div>'
            f'<div class="e-modal-panel" role="dialog" aria-modal="true">{body}</div>'
            f"</div>"
        )

    def widget_icon(self, el, sel):
        s = el.get("settings", {})
        icon = self.icon_svg(s.get("selected_icon"), "e-icon icon")
        self.sheet.add(
            f"{sel} .e-icon",
            {
                "color": s.get("primary_color"),
                "width": size(s.get("size")),
                "height": size(s.get("size")),
            },
        )
        align = {"end": "flex-end", "start": "flex-start", "center": "center"}.get(s.get("align"), None)
        self.sheet.add(sel, {"display": "flex", "justify-content": align})
        dynamic = json.dumps(s.get("__dynamic__") or {})
        if "close" in dynamic:
            return f'<button class="e-modal-close" type="button" data-close aria-label="Fechar">{icon}</button>'
        return icon

    # -- despacho ----------------------------------------------------------

    def render_widget(self, el, sel):
        kind = el.get("widgetType")
        if kind == "heading":
            return self.widget_heading(el, sel)
        if kind == "text-editor":
            return self.widget_text_editor(el, sel)
        if kind == "button":
            return self.widget_button(el, sel)
        if kind == "image":
            return self.widget_image(el, sel)
        if kind == "icon-list":
            return self.widget_icon_list(el, sel)
        if kind == "rating":
            return self.widget_rating(el, sel)
        if kind == "html":
            raw = el.get("settings", {}).get("html", "")
            # As fontes passaram a ser auto-alojadas (assets/css/fonts.css), por
            # isso os <link>/<preconnect> para o Google Fonts saem daqui.
            raw = re.sub(r"<link[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>\s*", "", raw)
            return raw.strip()
        if kind in ("presto_video", "shortcode"):
            return self.widget_video(el, sel)
        if kind == "form":
            return self.widget_form(el, sel)
        if kind == "nested-accordion":
            return self.widget_accordion(el, sel)
        if kind == "nested-carousel":
            return self.widget_carousel(el, sel)
        if kind == "off-canvas":
            return self.widget_offcanvas(el, sel)
        if kind == "icon":
            return self.widget_icon(el, sel)
        return f"<!-- widget não suportado: {kind} -->"

    def render_element(self, el, top_level=False):
        el_id = el.get("id")
        sel = f".e-{el_id}"
        s = el.get("settings", {})
        extra = (s.get("_css_classes") or "").strip()

        if el.get("elType") == "container":
            boxed = self.container_styles(el, sel, top_level)
            self.sheet.add_custom(s.get("custom_css"), sel)
            classes = ["e-con", "e-con-boxed" if boxed else "e-con-full", f"e-{el_id}"]
            if extra:
                classes.append(extra)
            if s.get("animation"):
                classes.append("e-anim")
            children = "".join(self.render_element(child) for child in el.get("elements", []))

            video_link = s.get("background_video_link")
            media = ""
            if video_link:
                url = local_asset(video_link, self.asset_map)
                media = (
                    f'<video class="e-con-video" autoplay muted loop playsinline '
                    f'preload="none" aria-hidden="true"><source src="{url}"></video>'
                )
            attrs = f' id="{s["_element_id"]}"' if s.get("_element_id") else ""
            if boxed:
                return (
                    f'<div class="{" ".join(classes)}"{attrs}>{media}'
                    f'<div class="e-con-inner">{children}</div></div>'
                )
            return f'<div class="{" ".join(classes)}"{attrs}>{media}{children}</div>'

        # widget
        self.common_styles(el, sel)
        classes = ["e-widget", f"e-widget-{el.get('widgetType')}", f"e-{el_id}"]
        if extra:
            classes.append(extra)
        if s.get("animation"):
            classes.append("e-anim")
        body = self.render_widget(el, sel)
        attrs = f' id="{s["_element_id"]}"' if s.get("_element_id") else ""
        return f'<div class="{" ".join(classes)}"{attrs}>{body}</div>'

    def run(self):
        sections = "".join(self.render_element(sec, top_level=True) for sec in self.data["content"])
        return sections, self.sheet.render()


# --------------------------------------------------------------------------


def build():
    with open(SOURCE, encoding="utf-8") as fh:
        data = json.load(fh)
    with open(VIDEOS, encoding="utf-8") as fh:
        videos = json.load(fh)
    asset_map = {}
    if os.path.exists(ASSET_MAP):
        with open(ASSET_MAP, encoding="utf-8") as fh:
            asset_map = json.load(fh)

    converter = Converter(data, asset_map, videos)
    body, css = converter.run()

    with open(os.path.join(ROOT, "tools", "page.template.html"), encoding="utf-8") as fh:
        template = fh.read()

    page = template.replace("<!--BODY-->", body).replace("{{TITLE}}", "Blue Bolt Agency — Agência de Marketing Digital")

    with open(OUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(page)
    with open(OUT_CSS, "w", encoding="utf-8") as fh:
        fh.write(css)

    print(f"index.html: {len(page):,} bytes")
    print(f"assets/css/page.css: {len(css):,} bytes")


if __name__ == "__main__":
    build()
