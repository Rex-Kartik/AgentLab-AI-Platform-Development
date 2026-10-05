---
name: Cinematic Cyber-Intelligence
colors:
  surface: '#111317'
  surface-dim: '#111317'
  surface-bright: '#37393e'
  surface-container-lowest: '#0c0e12'
  surface-container-low: '#1a1c20'
  surface-container: '#1e2024'
  surface-container-high: '#282a2e'
  surface-container-highest: '#333539'
  on-surface: '#e2e2e8'
  on-surface-variant: '#bbc9cd'
  inverse-surface: '#e2e2e8'
  inverse-on-surface: '#2f3035'
  outline: '#859397'
  outline-variant: '#3c494c'
  surface-tint: '#2fd9f4'
  primary: '#8aebff'
  on-primary: '#00363e'
  primary-container: '#22d3ee'
  on-primary-container: '#005763'
  inverse-primary: '#006877'
  secondary: '#d0bcff'
  on-secondary: '#3c0091'
  secondary-container: '#571bc1'
  on-secondary-container: '#c4abff'
  tertiary: '#cadeff'
  on-tertiary: '#00315d'
  tertiary-container: '#99c3ff'
  on-tertiary-container: '#005091'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#a2eeff'
  primary-fixed-dim: '#2fd9f4'
  on-primary-fixed: '#001f25'
  on-primary-fixed-variant: '#004e5a'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#d4e3ff'
  tertiary-fixed-dim: '#a4c9ff'
  on-tertiary-fixed: '#001c39'
  on-tertiary-fixed-variant: '#004883'
  background: '#111317'
  on-background: '#e2e2e8'
  surface-variant: '#333539'
  canvas-base: '#07080A'
  surface-primary: '#0D0F13'
  surface-secondary: '#11141A'
  surface-elevated: '#161A21'
  border-subtle: '#252A33'
  border-strong: '#343A46'
  text-primary: '#F5F7FA'
  text-secondary: '#A2A9B8'
  text-muted: '#6F7787'
  accent-green: '#34D399'
  accent-orange: '#FB923C'
  accent-red: '#F87171'
typography:
  headline-xl:
    fontFamily: Syne
    fontSize: 56px
    fontWeight: '700'
    lineHeight: 64px
  headline-xl-mobile:
    fontFamily: Syne
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
  headline-lg:
    fontFamily: Syne
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
  headline-lg-mobile:
    fontFamily: Syne
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-md:
    fontFamily: Syne
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  body-sm:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  label-code:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
  label-eyebrow:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-tablet: 2rem
  margin-desktop: 3rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system establishes an atmospheric, highly technical, and cinematic visual language for an autonomous AI platform. Rooted in developer-grade precision and computational gravitas, the aesthetic rejects the ubiquitous tropes of modern AI SaaS—such as hyper-saturated purple ambient blobs, centered marketing cliches, and indiscriminate glassmorphic blurs. Instead, it draws from brutalist high-density layouts, modern technical telemetry, and cinematic spatial interfaces.

The emotional target is authoritative, deep, and surgical: the sensation of commanding a powerful, real-time computational infrastructure. Primary visual hierarchy is communicated through pure surface tonal separation, precise hairline borders, and localized, purposeful accent colors that act as telemetry signals rather than cosmetic decoration.

## Colors

The color system is constructed dark-first, grounded in deep, light-absorbent charcoal canvases rather than flat monochromatic black. Surfaces step upward in brightness as they layer over one another, ensuring clear depth hierarchies without requiring artificial contrast:
- `canvas-base` (`#07080A`): The foundational backdrop for the entire viewport and spatial WebGL scenes.
- `surface-primary` (`#0D0F13`): Base work areas, core application panels, and primary sidebars.
- `surface-secondary` (`#11141A`): Component grouping panels, tool execution cards, and message wrappers.
- `surface-elevated` (`#161A21`): Modals, floating action docks, context menus, and slide-over drawers.

### Accents & Functional Indicators
Chromatic accents are strictly semantic; they are never applied as decorative background gradients.
- **Cyan (`#22D3EE`)**: Primary technical accent representing active pipeline execution, signal routing, and telemetry glows.
- **Purple (`#8B5CF6`)**: Capability node category highlights and secondary structural actions.
- **Blue (`#60A5FA`)**: Network, external API, and search capability identification.
- **Green (`#34D399`)**: Successful tool execution, healthy node states, and operational presence.
- **Orange (`#FB923C`)**: Computational workflows, mathematical operations, and non-fatal warnings.
- **Red (`#F87171`)**: Execution exceptions, node failures, and fatal interruptions.

## Typography

The type system is divided into three distinct roles, balancing high-impact editorial character with data-dense terminal utility:

1. **Display (Syne)**: Distinctive, geometric, and high-contrast. Used exclusively for landing hero headers, section titles, and narrative anchor points. It provides an immediate avant-garde counterweight to generic SaaS typography.
2. **Interface & Narrative (Hanken Grotesk)**: A contemporary, sharp grotesque that manages application navigation, complex descriptions, dialogs, and primary body content without visual fatigue.
3. **Telemetry & Technical (JetBrains Mono)**: A monospaced typeface dedicated to execution logs, tool IDs, timestamps, parameter keys, node schemas, and latency indicators. `label-eyebrow` must always be styled with `text-transform: uppercase` and `letter-spacing: 0.08em`.

## Layout & Spacing

The design system enforces a modular rhythm built around multiples of 4px and 8px. Layouts conform to two paradigms:

### Marketing & Showcase Mode
Utilizes a fluid container with generous section spacing (`space-xl` scaled for macro offsets up to 120px) and a fixed hero height ranging between 85vh and 100vh. Sections utilize a 12-column grid with a maximum content constraint of 1440px.

### Operational Application Mode
Strict 3-column split-view terminal architecture designed desktop-first (`1440px`, `1600px`, `1920px`):
- **Navigation Rail / Left Column**: 260px fixed width (collapses to an icon rail of 64px on tablet screens < 1024px; opens via off-canvas drawer on mobile < 768px).
- **Workspace / Center Column**: Fluid column containing interactive chats, execution flows, and canvas workflows.
- **Activity & Telemetry / Right Column**: 380px fixed width for live step sequences, tool invocations, and memory payloads (collapsible drawer on tablet and responsive bottom sheet on mobile).

## Elevation & Depth

Visual hierarchy is primarily expressed through **tonal surface stacking** combined with **subtle, razor-thin luminous borders**. 

### Tonal Hierarchy
Depth does not depend on heavy, blurry dropshadows, which dilute dark mode clarity. Instead, layers physically brighten as they ascend toward the user:
- Base viewport: `#07080A`
- Static layout containers: `#0D0F13` with `1px solid #252A33`
- Cards and content modules: `#11141A` with `1px solid #252A33`
- Overlays, popovers, and sliding drawers: `#161A21` with `1px solid #343A46`

### Luminous Accents & Ambient Glows
- Focused or actively executing elements introduce localized ambient glows using the technical accent `#22D3EE` at 10%–15% opacity with a blur radius of 16px–24px.
- Subtle backdrop blur (`backdrop-filter: blur(12px)`) is reserved strictly for floating persistent navigation bars and contextual inspector heads over WebGL canvases.

## Shapes

The design system maintains a structured, architectural geometry. Roundedness is kept strictly **Soft (1)**, avoiding overly organic pill buttons and rounded bubble corners in favor of a crisp, industrial look.

- **Base Radius (4px / 0.25rem)**: Small chips, status badges, buttons, tool execution tags, code blocks, and form inputs.
- **Medium Radius (8px / 0.5rem)**: Standard capability cards, panel containers, and dialog sheets.
- **Large Radius (12px / 0.75rem)**: Maximum permissible radius, applied exclusively to elevated overlay modals and floating viewport docks.

## Components

### Buttons
- **Primary Action**: Solid `#F5F7FA` surface with `#07080A` text, 4px radius, `fontFamily: "Hanken Grotesk"`, medium weight. On hover, transitions in 150ms to `#FFFFFF` with a faint `0 0 12px rgba(245, 247, 250, 0.2)` glow.
- **Secondary / Technical**: `#11141A` surface with `1px solid #252A33` border and `#F5F7FA` text. Transitions to `border-color: #343A46` and `#161A21` background on hover.
- **Ghost / Trace**: Transparent fill with `#A2A9B8` text. Hover activates `#11141A` background and `#F5F7FA` text.

### Tool Execution & Capability Cards
- Built on `#11141A` with a hairline `1px solid #252A33` border and 8px border radius.
- Cards host an icon tile tinted to the tool’s category accent (e.g., `#22D3EE` for search, `#FB923C` for compute) at 10% fill with a 100% stroke outline.
- Active execution displays an animated border-beam sweep using `#343A46` with an accent trace.

### Chips & Status Indicators
- Rendered in `JetBrains Mono` at 11px with 4px border radius.
- Always include a compact geometric symbol or status bullet (`●` for live states, `✓` for completed cycles, `◌` for processing nodes, and `⚠` for warnings).
- Background fills remain tinted at 8% opacity of the corresponding accent with matching text (e.g., green `#34D399` text on `rgba(52, 211, 153, 0.08)` background).

### Input Fields & Terminal Prompts
- Background: `#0D0F13` with `1px solid #252A33`, inset padding of `0.625rem 0.875rem`, and 4px radius.
- Placeholder text in `#6F7787`.
- Focus state switches the border to `1px solid #22D3EE` with an ambient glow of `0 0 0 1px rgba(34, 211, 238, 0.3)`.

### Checkboxes & Radio Toggles
- Custom square (4px radius) and circle housings measuring 16x16px with `1px solid #252A33` on `#0D0F13`.
- Checked state fills with `#22D3EE` and displays a high-contrast `#07080A` checkmark.

### Telemetry Timelines & Tracing
- Hairline continuous spine of `1px solid #252A33`.
- Nodes attach along the spine with 8px circular beads; active nodes radiate an orbital ping animation in `#22D3EE`. Execution metadata displays strictly in `label-mono` using `#6F7787`.