# WiseLaw 官网主题色彩提取

- 来源链接：https://lawrence.wiselawai.com/en
- 提取日期：2026-05-11
- 提取方式：页面 HTML/CSS 变量、内联渐变样式、首屏产品图抽样

## 色彩印象

WiseLaw 官网整体采用“暖米白 + 栗棕 + 深咖黑”的法律科技品牌色系。页面气质偏克制、专业、可信，不走高饱和科技蓝路线，而是用暖色背景与低饱和棕色建立“法律、办公、可靠、实体工作站”的感觉。

## 核心主题色

| 色彩角色 | CSS 变量 | 色值 | 色块 | 用途 |
| --- | --- | --- | --- | --- |
| 页面背景 | `--background` | `#faf8f6` | <span style="display:inline-block;width:48px;height:18px;background:#faf8f6;border:1px solid #ddd;"></span> | 全站主背景、首屏暖白底 |
| 主文字 | `--foreground` | `#2c2421` | <span style="display:inline-block;width:48px;height:18px;background:#2c2421;"></span> | 标题、正文强信息 |
| 卡片背景 | `--card` | `#ffffff` | <span style="display:inline-block;width:48px;height:18px;background:#ffffff;border:1px solid #ddd;"></span> | 卡片、表单、内容容器 |
| 品牌主色 | `--primary` | `#8b5a4a` | <span style="display:inline-block;width:48px;height:18px;background:#8b5a4a;"></span> | CTA 按钮、链接 hover、图标、高亮信息 |
| 主色反白文字 | `--primary-foreground` | `#ffffff` | <span style="display:inline-block;width:48px;height:18px;background:#ffffff;border:1px solid #ddd;"></span> | 主按钮文字 |

## 辅助色与中性色

| 色彩角色 | CSS 变量 | 色值 | 色块 | 用途 |
| --- | --- | --- | --- | --- |
| 次级背景 | `--secondary` | `#f5f2ef` | <span style="display:inline-block;width:48px;height:18px;background:#f5f2ef;border:1px solid #ddd;"></span> | 浅色分区、弱背景 |
| 弱化背景 | `--muted` | `#f5f2ef` | <span style="display:inline-block;width:48px;height:18px;background:#f5f2ef;border:1px solid #ddd;"></span> | 标签、浅底提示 |
| 弱化文字 | `--muted-foreground` | `#5c524d` | <span style="display:inline-block;width:48px;height:18px;background:#5c524d;"></span> | 描述文本、导航普通态 |
| 强调浅底 | `--accent` | `#f5edeb` | <span style="display:inline-block;width:48px;height:18px;background:#f5edeb;border:1px solid #ddd;"></span> | hover 背景、浅色品牌底 |
| 强调文字 | `--accent-foreground` | `#8b5a4a` | <span style="display:inline-block;width:48px;height:18px;background:#8b5a4a;"></span> | 强调区文字 |
| 边框 | `--border` | `#e8e2dc` | <span style="display:inline-block;width:48px;height:18px;background:#e8e2dc;border:1px solid #ddd;"></span> | 卡片边框、分割线 |
| 输入框边界 | `--input` | `#d9d0c8` | <span style="display:inline-block;width:48px;height:18px;background:#d9d0c8;border:1px solid #ddd;"></span> | 表单输入框 |
| 聚焦环 | `--ring` | `#8b5a4a` | <span style="display:inline-block;width:48px;height:18px;background:#8b5a4a;"></span> | focus ring |
| 三级文字 | `--text-tertiary` | `#8c8279` | <span style="display:inline-block;width:48px;height:18px;background:#8c8279;"></span> | 次要说明、辅助标签 |
| 禁用文字 | `--text-disabled` | `#b8b0a3` | <span style="display:inline-block;width:48px;height:18px;background:#b8b0a3;"></span> | disabled 状态 |
| hover 背景 | `--bg-hover` | `#f0ebe7` | <span style="display:inline-block;width:48px;height:18px;background:#f0ebe7;border:1px solid #ddd;"></span> | 菜单、按钮 hover |
| active 背景 | `--bg-active` | `#ebdad6` | <span style="display:inline-block;width:48px;height:18px;background:#ebdad6;border:1px solid #ddd;"></span> | 当前选中、按下态 |
| 危险色 | `--destructive` | `#ef4444` | <span style="display:inline-block;width:48px;height:18px;background:#ef4444;"></span> | 错误、删除、校验失败 |

## 渐变色

| 名称 | CSS 变量 | 色值 | 用途 |
| --- | --- | --- | --- |
| 品牌主渐变 | `--gradient-primary` | `linear-gradient(180deg, #8b5a4a 0%, #74493c 100%)` | 主按钮、标题渐变文字、装饰光晕 |
| 冷灰蓝辅助渐变 | `--gradient-secondary` | `linear-gradient(180deg, #6b7b8f 0%, #576878 100%)` | 次级装饰光晕、冷色平衡 |
| 首屏暖光背景 | inline style | `radial-gradient(ellipse 70% 50% at 50% -5%, rgba(139, 90, 74, 0.07) 0%, transparent 70%), linear-gradient(117deg, #faf6f5 0%, rgba(255, 255, 255, 0) 80%)` | hero 区域顶部柔光 |

## 页面中出现的补充色

| 色值 | 色块 | 出现位置 / 作用 |
| --- | --- | --- |
| `#74493c` | <span style="display:inline-block;width:48px;height:18px;background:#74493c;"></span> | 品牌主渐变深色端 |
| `#6b7b8f` | <span style="display:inline-block;width:48px;height:18px;background:#6b7b8f;"></span> | 辅助冷灰蓝渐变起点 |
| `#576878` | <span style="display:inline-block;width:48px;height:18px;background:#576878;"></span> | 辅助冷灰蓝渐变终点 |
| `#45556c` | <span style="display:inline-block;width:48px;height:18px;background:#45556c;"></span> | 流程步骤未激活圆点 |
| `#00a544` | <span style="display:inline-block;width:48px;height:18px;background:#00a544;"></span> | 成功状态、完成步骤 |
| `#ef4444` | <span style="display:inline-block;width:48px;height:18px;background:#ef4444;"></span> | 错误 / destructive |
| `#c49485` | <span style="display:inline-block;width:48px;height:18px;background:#c49485;"></span> | 标题 shimmer 动画中的亮棕色 |
| `rgba(250, 248, 246, 0.85)` | <span style="display:inline-block;width:48px;height:18px;background:rgba(250,248,246,.85);border:1px solid #ddd;"></span> | 顶部导航半透明背景 |
| `rgba(139, 90, 74, 0.07)` | <span style="display:inline-block;width:48px;height:18px;background:rgba(139,90,74,.07);border:1px solid #ddd;"></span> | 首屏暖色径向光 |

## 推荐设计令牌

```css
:root {
  --background: #faf8f6;
  --foreground: #2c2421;
  --card: #ffffff;
  --card-foreground: #2c2421;

  --primary: #8b5a4a;
  --primary-dark: #74493c;
  --primary-foreground: #ffffff;

  --secondary: #f5f2ef;
  --secondary-foreground: #2c2421;
  --muted: #f5f2ef;
  --muted-foreground: #5c524d;
  --accent: #f5edeb;
  --accent-foreground: #8b5a4a;

  --border: #e8e2dc;
  --input: #d9d0c8;
  --ring: #8b5a4a;

  --text-tertiary: #8c8279;
  --text-disabled: #b8b0a3;
  --bg-hover: #f0ebe7;
  --bg-active: #ebdad6;
  --destructive: #ef4444;

  --gradient-primary: linear-gradient(180deg, #8b5a4a 0%, #74493c 100%);
  --gradient-secondary: linear-gradient(180deg, #6b7b8f 0%, #576878 100%);
}
```

## 配色使用建议

- 主按钮：使用 `--gradient-primary` 或 `--primary`，文字使用 `#ffffff`。
- 页面大面积背景：使用 `#faf8f6`，卡片使用 `#ffffff`，边框使用 `#e8e2dc`。
- 标题文字：使用 `#2c2421`；正文说明可使用 `#5c524d`。
- 标签 / 徽章：浅底建议用 `#f5edeb` 或 `rgba(139, 90, 74, 0.05)`，文字用 `#8b5a4a`。
- 冷灰蓝 `#6b7b8f` / `#576878` 只适合作为辅助装饰色，不宜替代品牌主色。

## 可访问性简评

- `#2c2421` 在 `#faf8f6` 上对比度约为 `14.35:1`，适合正文和标题。
- `#8b5a4a` 在 `#faf8f6` 上对比度约为 `5.42:1`，可用于普通字号文本。
- `#5c524d` 在 `#faf8f6` 上对比度约为 `7.16:1`，适合说明文字。
