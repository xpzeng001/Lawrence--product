# Lawrence Product Theme

This repository uses one shared visual theme for every shot. All future shots must follow these tokens unless the brand theme is intentionally revised.

Source reference: `wiselaw-theme-colors.md`

## Core Tokens

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

  --cool: #6b7b8f;
  --cool-dark: #576878;
  --success: #00a544;
  --shine: #c49485;

  --gradient-primary: linear-gradient(180deg, #8b5a4a 0%, #74493c 100%);
  --gradient-secondary: linear-gradient(180deg, #6b7b8f 0%, #576878 100%);
}
```

## Shot Rules

- Use warm off-white backgrounds, white cards, soft brown borders, and restrained shadows.
- Use `--foreground` for main titles and `--gradient-primary` or `--primary` for emphasis.
- Use `--muted-foreground` and `--text-tertiary` for secondary copy and small labels.
- Use `--cool` / `--cool-dark` only as an auxiliary balance color, not as the main brand color.
- Keep the visual mood professional, restrained, warm, and legal-tech oriented.
