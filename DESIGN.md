---
name: Riichi Score Calculator
description: A clear, table-ready web tool for scoring Japanese riichi mahjong hands.
colors:
  ink: "#111827"
  text: "#1f2933"
  text-soft: "#52606d"
  text-muted: "#66788a"
  field-label: "#334e68"
  detail-text: "#243b53"
  control-text: "#334155"
  surface-bg: "#f4f7f6"
  surface: "#ffffff"
  surface-soft: "#f8fafc"
  surface-raised: "#f1f5f9"
  surface-panel: "#fbfdff"
  border: "#cbd5e1"
  border-muted: "#bcccdc"
  border-soft: "#e4e7eb"
  border-panel: "#d9e2ec"
  primary: "#047857"
  primary-bright: "#10b981"
  primary-deep: "#065f46"
  primary-soft: "#d1fae5"
  primary-tint: "#ecfdf3"
  primary-light: "#a7f3d0"
  danger: "#b42318"
  danger-soft: "#fef2f2"
  danger-light: "#fecaca"
  danger-accent: "#fca5a5"
  warning: "#92400e"
  warning-soft: "#fffbeb"
  warning-border: "#fde68a"
typography:
  display:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "clamp(2rem, 6vw, 3.8rem)"
    fontWeight: 900
    lineHeight: 1
  headline:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "1.2rem"
    fontWeight: 850
    lineHeight: 1.2
  title:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "0.92rem"
    fontWeight: 850
    lineHeight: 1.25
  body:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "0.9rem"
    fontWeight: 800
    lineHeight: 1.2
  tile:
    fontFamily: "system symbol fallback"
    fontSize: "2.35rem"
    fontWeight: 400
    lineHeight: 1
  tile-compact:
    fontFamily: "system symbol fallback"
    fontSize: "1.65rem"
    fontWeight: 400
    lineHeight: 1
  badge:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "0.66rem"
    fontWeight: 900
    lineHeight: 1
rounded:
  sm: "8px"
  pill: "999px"
spacing:
  xs: "8px"
  sm: "10px"
  md: "12px"
  lg: "16px"
  xl: "20px"
  xxl: "24px"
  page: "28px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: "0 16px"
    height: "46px"
    typography: "{typography.label}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.field-label}"
    rounded: "{rounded.sm}"
    padding: "0 16px"
    height: "46px"
    typography: "{typography.label}"
  tile-button:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    width: "54px"
    height: "62px"
    typography: "{typography.tile}"
  input-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.sm}"
    padding: "0 12px"
    height: "46px"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.sm}"
    padding: "24px"
---

# Design System: Riichi Score Calculator

## 1. Overview

**Creative North Star: "The Quiet Tile Table"**

The interface should feel like a calm scoring surface laid beside an actual game: organized, legible, and focused on recognition. The product is not a Japanese-themed decoration exercise. Its character comes from mahjong tile faces, grouped suits, table-like spacing, and clear scoring feedback.

This is a product UI for casual and learning users, so clarity beats atmosphere. Every screen should reduce notation burden, reveal what is still missing, and make the scoring result feel explainable. The current system is restrained: pale neutral surfaces, a single green primary action language, red only for errors and winning-tile emphasis, and 8px component geometry throughout.

It explicitly rejects casino styling, decorative Japanese tropes, brush fonts, lanterns, temple imagery, heavy red-and-black theming, expert-only density, and shorthand tile codes as the primary visual representation.

**Key Characteristics:**

- Restrained product density with clear two-column desktop structure and single-column mobile behavior.
- Real tile recognition should be the signature visual layer; surrounding chrome stays quiet.
- Green is the action and success language; red is reserved for error, red-five, and winning-tile distinction.
- Components use consistent 8px corners, clear borders, and direct labels.
- Readiness, error, and result states are visible explanations, not decorative notices.

## 2. Colors

The palette is a cool, clean tabletop neutral system with emerald action cues and red scoring exceptions.

### Primary

- **Table Green**: The primary action and success color. Use for the score action, selected controls, online status, ready state, and focused positive state.
- **Fresh Felt**: The brighter green used sparingly for active borders and checkbox accents.
- **Green Wash**: The selected-state fill for active segmented controls and chosen tiles.

### Secondary

- **Winning Red**: The danger and special-tile color. Use for errors, offline state, red fives, and winning-tile distinction only.
- **Red Tile Wash**: The pale red support color for error panels and red-five borders.
- **Hand Marker Red**: The inset marker used on the winning tile.

### Tertiary

- **Readiness Amber**: The warning language for incomplete hands. Use only for "before scoring" guidance and missing-input states.

### Neutral

- **Ink Black**: Primary headings, tile labels, score surfaces, and high-emphasis values.
- **Slate Text**: Body text and form text.
- **Soft Slate**: Secondary text, metadata, and muted labels.
- **Table Mist**: The page background.
- **White Tile**: Main cards, buttons, fields, and tile faces.
- **Cool Tray**: Tile trays and low-emphasis component backgrounds.
- **Panel Frost**: Helper and advanced panels.
- **Tile Border**: Interactive control borders.
- **Soft Divider**: Internal dividers and low-emphasis borders.

### Named Rules

**The Tile Color Rule.** Tile visuals may carry suit identity and red-five meaning; page chrome must not compete with them.

**The Red Is Meaning Rule.** Red is not a theme color. It means error, red-five, or winning-tile emphasis.

## 3. Typography

**Display Font:** Inter with system sans fallbacks  
**Body Font:** Inter with system sans fallbacks  
**Label/Mono Font:** Inter with system sans fallbacks

**Character:** The typography is compact, plain, and instructional. It should feel like a trustworthy tool surface, not a poster, game splash screen, or restaurant menu.

### Hierarchy

- **Display** (900, `clamp(2rem, 6vw, 3.8rem)`, line-height 1): Page title only. Keep it short and do not use decorative display fonts.
- **Headline** (850, `1.2rem`, line-height 1.2): Panel titles such as hand entry and result.
- **Title** (850, `0.92rem`, line-height 1.25): Field labels, tile group headings, and section labels.
- **Body** (400, `1rem`, line-height 1.5): Form values, helper copy, and result explanations. Keep prose under 75ch when it becomes instructional.
- **Label** (800-900, `0.86rem` to `0.9rem`, optional uppercase only for tiny score metadata): Buttons, badges, and compact status text.
- **Tile** (400, `2.35rem` standard / `1.65rem` compact, line-height 1): Mahjong tile glyphs only, using symbol fonts before emoji fallbacks.
- **Badge** (900, `0.66rem`, line-height 1): Tiny count and red-five markers attached to tile controls.

### Named Rules

**The Notation Reduction Rule.** Typography must support tile recognition, not replace it. Text labels explain choices, but tile faces should carry the primary tile identity.

**The No Brush Font Rule.** Brush, calligraphic, faux-Japanese, or menu-style display fonts are prohibited.

## 4. Elevation

The system currently uses a hybrid of thin borders and one broad ambient shadow on major panels. Depth is structural: panels separate input from result, trays separate tile collections, and dark score display isolates the final payment. Avoid adding more shadow vocabulary until the tile visuals are upgraded and the hierarchy can be judged again.

### Shadow Vocabulary

- **Panel Ambient** (`box-shadow: 0 20px 50px rgba(31, 41, 51, 0.08)`): Current form and result panels only.
- **Winning Tile Inset** (`box-shadow: inset 0 -4px 0 #fca5a5`): Marks the winning tile without changing its overall shape.

### Named Rules

**The One Lift Rule.** Large ambient shadow belongs to top-level panels only. Buttons, chips, fields, and tiles stay border-defined unless interaction state demands movement.

## 5. Components

### Buttons

- **Shape:** Gently squared controls with an 8px radius.
- **Primary:** Table Green background with white text, 46px minimum height, 850 weight, icon plus label when an icon exists.
- **Hover / Focus:** Hover lifts by 1px. Focus states must be visible and should use the primary border language rather than shadow-only styling.
- **Secondary / Drawer:** White surface, Tile Border stroke, Slate label color, same 46px height and icon spacing.

### Chips

- **Style:** White tile-like capsules with 8px corners, Tile Border stroke, compact horizontal padding, and high-weight labels.
- **State:** Chips may remove dora indicators or display selected tiles. A removal affordance must be explicit; do not rely on color alone.

### Cards / Containers

- **Corner Style:** 8px radius across panels, helper sections, trays, cards, and empty states.
- **Background:** Main panels use White Tile. Helper sections use Panel Frost. Tile trays use Cool Tray.
- **Shadow Strategy:** Only top-level form and result panels use Panel Ambient.
- **Border:** Panels use Border Panel. Internal helper sections use Soft Divider. Tile trays use dashed Tile Border.
- **Internal Padding:** Major panels use 24px desktop and 18px on mobile; helper sections use 16px.

### Inputs / Fields

- **Style:** White background, Tile Border stroke, 8px radius, 46px minimum height, 12px horizontal padding.
- **Focus:** Add a clear visible focus treatment using Table Green or Fresh Felt. Browser defaults alone are not enough for final polish.
- **Error / Disabled:** Disabled tiles reduce opacity and block pointer interaction. Error states use Red Tile Wash with Winning Red text and an icon.

### Navigation

This app has no persistent navigation. The top bar carries product identity, page title, and backend status. Keep it functional and compact; do not turn it into a marketing header.

### Tile Selection

Tile controls are the signature component. They currently render as text-code buttons, but the design system direction is real mahjong tile faces. Each tile must remain at a stable size, support keyboard selection, expose an accessible text label, and show selected, winning, disabled, and red-five states without relying on color alone.

### Result Panel

The result panel is a sticky desktop summary and an inline mobile section. The main payment uses the dark Ink Black surface with Green Light metadata. Yaku and fu details use compact neutral pills so the result reads as explanation rather than a single opaque number.

## 6. Do's and Don'ts

### Do:

- **Do** use real mahjong tile visuals as the primary representation for tile selection and entered hands.
- **Do** preserve the 8px component radius unless a control is intentionally pill-shaped, such as backend status.
- **Do** use Table Green for primary actions, selected controls, and ready/success states.
- **Do** keep advanced options grouped and progressively disclosed.
- **Do** pair every color-coded tile or scoring state with text, icon, shape, position, or accessible label.
- **Do** keep the desktop layout focused on hand entry plus result, and collapse to one column below 960px.

### Don't:

- **Don't** use casino styling, decorative Japanese tropes, brush fonts, lanterns, temple imagery, or heavy red-and-black theming.
- **Don't** make shorthand tile codes such as `1m` or `3p` the primary tile representation once tile faces are available.
- **Don't** create expert-only density. Casual users must see what to do next.
- **Don't** use red as general decoration. Red means error, red-five, or winning-tile distinction.
- **Don't** add decorative shadows to every button, chip, and tile. Top-level panels already own elevation.
- **Don't** replace familiar form controls with custom affordances unless the custom control is more accessible and easier to understand.
