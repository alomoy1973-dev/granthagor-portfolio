---
name: Literary Minimalist
colors:
  surface: '#faf9f5'
  surface-dim: '#dbdad6'
  surface-bright: '#faf9f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f0'
  surface-container: '#efeeea'
  surface-container-high: '#e9e8e4'
  surface-container-highest: '#e3e2df'
  on-surface: '#1b1c1a'
  on-surface-variant: '#444748'
  inverse-surface: '#2f312e'
  inverse-on-surface: '#f2f1ed'
  outline: '#747878'
  outline-variant: '#c4c7c7'
  surface-tint: '#5f5e5e'
  primary: '#181919'
  on-primary: '#ffffff'
  primary-container: '#2d2d2d'
  on-primary-container: '#959494'
  inverse-primary: '#c8c6c6'
  secondary: '#556254'
  on-secondary: '#ffffff'
  secondary-container: '#d6e4d2'
  on-secondary-container: '#596658'
  tertiary: '#071a25'
  on-tertiary: '#ffffff'
  tertiary-container: '#1d2f3a'
  on-tertiary-container: '#8497a4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e4e2e1'
  primary-fixed-dim: '#c8c6c6'
  on-primary-fixed: '#1b1c1c'
  on-primary-fixed-variant: '#474747'
  secondary-fixed: '#d9e6d5'
  secondary-fixed-dim: '#bdcaba'
  on-secondary-fixed: '#131e14'
  on-secondary-fixed-variant: '#3e4a3d'
  tertiary-fixed: '#d2e5f4'
  tertiary-fixed-dim: '#b6c9d8'
  on-tertiary-fixed: '#0a1e28'
  on-tertiary-fixed-variant: '#374955'
  background: '#faf9f5'
  on-background: '#1b1c1a'
  surface-variant: '#e3e2df'
typography:
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-sm:
    fontFamily: Playfair Display
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: EB Garamond
    fontSize: 20px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: EB Garamond
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.4'
    letterSpacing: 0.03em
spacing:
  base: 8px
  container-max: 1140px
  content-max: 720px
  gutter: 24px
  margin-mobile: 20px
  stack-lg: 80px
  stack-md: 48px
  stack-sm: 24px
---

## Brand & Style

The design system is centered on the concept of the "author’s sanctuary"—a digital space that mimics the quiet, focused atmosphere of a well-appointed library or a fresh sheet of parchment. It targets an audience that appreciates long-form thought, intellectual depth, and the tactile history of the written word.

The aesthetic blends **Minimalism** with **Editorial Elegance**. By leveraging generous whitespace (macro-typography) and a restricted palette, the UI recedes to allow the content to breathe. The emotional response should be one of serenity and focus, stripping away the frantic patterns of the modern web in favor of a timeless, archival quality.

## Colors

The palette is inspired by traditional printing materials. The primary background (#FDFCF8) mimics the warmth of high-quality parchment, reducing eye strain and providing a softer contrast than pure white. 

- **Primary (Charcoal):** Used for maximum legibility in body text and primary navigation.
- **Secondary (Muted Sage):** Used for subtle accents, success states, or categories. It evokes a sense of organic growth and calm.
- **Tertiary (Dusty Blue):** Reserved for secondary call-to-actions or decorative flourishes like blockquote borders.
- **Neutral:** A range of warm greys derived from the charcoal primary are used for hair-line borders and metadata.

## Typography

This design system treats typography as the primary visual element. 

- **Headlines:** Use **Playfair Display**. Its high stroke contrast and elegant serifs provide an authoritative, editorial feel. Letter spacing is slightly tightened on large displays to maintain visual tension.
- **Body:** Use **EB Garamond**. Chosen for its historical roots and exceptional readability in long-form prose. The line height is intentionally generous (1.6) to facilitate a comfortable rhythmic scanning of lines.
- **System/Labels:** Use **Inter**. A clean, functional sans-serif provides a necessary "modern" anchor for functional elements like dates, tags, and button labels, ensuring they are clearly distinguished from the narrative content.

## Layout & Spacing

The layout follows a **Fixed-Width Centered** philosophy for reading clarity. While the site container spans up to 1140px, the actual text narrative is restricted to a "Reading Well" of 720px to maintain optimal characters-per-line (CPL).

- **Grid:** A 12-column grid is used for landing pages, but article pages often collapse to a single centered column with wide gutters.
- **Rhythm:** Vertical rhythm is driven by the `stack` variables. Use `stack-lg` to separate major thematic sections and `stack-md` for spacing between headlines and body copy. 
- **Mobile:** Margins reduce to 20px, and vertical spacing is compressed by approximately 20% to account for the smaller viewport height.

## Elevation & Depth

This design system rejects heavy shadows in favor of **Low-Contrast Outlines** and **Tonal Layering**. Depth is communicated through the physical metaphor of stacked sheets of paper.

- **Surfaces:** Most interactive elements sit directly on the parchment background.
- **Borders:** Use 1px solid lines in a lightened version of the primary charcoal (e.g., #E0DDD5). These "hairline" borders define sections without adding visual weight.
- **Interaction:** On hover, elements may transition to a slightly lighter tint of the background or reveal a subtle, extremely diffused shadow (15% opacity, 20px blur) to suggest the element is being "lifted" off the page.

## Shapes

The shape language is strictly **Sharp (0)**. 

To reinforce the archival and literary feel, all buttons, input fields, and image containers utilize 90-degree corners. This evokes the edges of books, stationery, and traditional printing blocks. Any "softness" in the UI should come from the color palette and typography, rather than the geometry of the components.

## Components

- **Buttons:** Primary buttons use a solid Charcoal background with Parchment text. Secondary buttons use a 1px Charcoal border with a transparent background. All buttons utilize the `label-md` uppercase typography.
- **Input Fields:** Minimalist design with only a bottom border (1px). Focus states transition the border color to Sage.
- **Cards:** No heavy shadows or thick borders. Cards are defined by a subtle 1px border or a very slight background color shift (#F8F6F0).
- **Blockquotes:** Set in `body-lg` italic. A 2px solid border in Sage or Dusty Blue should be placed to the left of the text, with generous padding.
- **Lists:** Unordered lists use custom "bullet" markers—small, solid charcoal squares (3px) to match the sharp shape language.
- **Links:** Inline links are underlined with a 1px Sage line, positioned 2px below the baseline to ensure it doesn't cut through descenders. On hover, the underline weight increases to 2px.