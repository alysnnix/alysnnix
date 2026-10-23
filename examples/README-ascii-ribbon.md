<!--
  README variant: ascii-ribbon. The signature and ribbon as text art, kept in color by an SVG (light and dark), then intro, now, projects, links, langs.
  To use it: cp examples/README-ascii-ribbon.md README.md, then delete this comment.
  Asset paths are relative to the repo root (./assets/...), so images only resolve once it lives there.
  Art: scripts/gen_ascii.sh regenerates assets/ascii/ (scripts/ascii_ribbon.py draws the ribbon).
  Keep the langs markers: .github/workflows/github-langs.yml rewrites the block between them every day.
-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/ascii/ribbon-signature-dark.svg">
  <img src="./assets/ascii/ribbon-signature-light.svg" alt="Aly, handwritten, unwinding into a lavender and pink ribbon of threads, drawn in text characters" width="100%">
</picture>

I'm Aly. I've been writing software since 2019, and since 2021 at Seazone, mostly in the parts of a product that touch money: checkout and payments (3DS, Pix, PayPal), the A/B tests that decide what ships, and keeping pages fast on cheap phones. React, Next.js and TypeScript up front, Python, Django and FastAPI behind.

My machines are declared in Nix, and most days I write code in the terminal next to Claude Code.

`now` &nbsp; shipping [framebudget](https://framebudget.dev) 0.9 and writing about it on [the blog](https://aly.engineer/blog).

### things i've made

- **[framebudget](https://framebudget.dev)**, a small TypeScript library: before the first paint it measures how much of the 16.7 ms frame budget a device really has, and turns on only the visual effects that fit. 4.6 KB gzip boot script, an FPS governor, React, Vue and Angular bindings. MIT, [on npm](https://www.npmjs.com/package/framebudget).
- **[aly.engineer](https://aly.engineer)**, my site: a lab of small experiments, the blog, and the signature that turns into this ribbon.
- **[resume.aly.engineer](https://resume.aly.engineer)**, my resume as a site. Astro, Portuguese and English, on Cloudflare Workers.
- **[devproxy](https://github.com/alysnnix/devproxy)** gives each Docker Compose project its own loopback IP, so two stacks can both have Postgres on 5432. Go.
- **[apollo-fleet](https://github.com/alysnnix/apollo-fleet)** runs several isolated Apollo streaming hosts on one Windows machine, one per Moonlight client. Rust.

[aly.engineer](https://aly.engineer) &nbsp;/&nbsp; [blog](https://aly.engineer/blog) &nbsp;/&nbsp; [resume](https://resume.aly.engineer) &nbsp;/&nbsp; [linkedin](https://linkedin.com/in/alysnnix) &nbsp;/&nbsp; [4ly.alcantara@gmail.com](mailto:4ly.alcantara@gmail.com)

### most used

<!--START:langs-->
```text
TypeScript     4.7 MB   █████████████████████████   71.43%
JavaScript   671.6 kB   ████████████░░░░░░░░░░░░░   10.31%
Emacs Lisp   317.7 kB   █████████░░░░░░░░░░░░░░░░    4.88%
Shell        173.1 kB   ███████░░░░░░░░░░░░░░░░░░    2.66%
Nix          166.2 kB   ███████░░░░░░░░░░░░░░░░░░    2.55%
Go           159.7 kB   ██████░░░░░░░░░░░░░░░░░░░    2.45%
Python        81.3 kB   █████░░░░░░░░░░░░░░░░░░░░    1.25%
MDX           72.7 kB   █████░░░░░░░░░░░░░░░░░░░░    1.12%
```
<!--END:langs-->
