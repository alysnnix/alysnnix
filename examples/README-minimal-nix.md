<!--
  README variant: minimal-nix. The current layout kept, every field brought up to date, projects folded into the attrset, no bongo cat.
  To use it, copy this file over the repo root README.md (cp examples/README-minimal-nix.md README.md).
  Asset paths are relative to the repo root (./assets/...), so images only resolve once it lives there.
  Keep the langs markers: .github/workflows/github-langs.yml rewrites the block between them every day.
-->

# hey, i'm aly

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/aly-signature-dark.svg">
  <img align="left" height="150" src="./assets/aly-signature-light.svg" alt="Aly, handwritten" hspace="20" vspace="8" />
</picture>

```nix
{
  name     = "alysson alcantara";
  role     = "software engineer @ seazone";
  since    = 2019;
  location = "brazil";
  front    = [ "react" "next.js" "typescript" ];
  back     = [ "python" "django" "fastapi" ];
  focus    = [
    "checkout & payments (3ds, pix, paypal)"
    "a/b testing"
    "web performance"
    "design systems"
  ];
  os       = "nixos";
  editor   = "claude code, in the terminal";

  projects = {
    framebudget = "https://framebudget.dev";
    devproxy    = "https://github.com/alysnnix/devproxy";
    apolloFleet = "https://github.com/alysnnix/apollo-fleet";
  };

  links = {
    site     = "https://aly.engineer";
    blog     = "https://aly.engineer/blog";
    resume   = "https://resume.aly.engineer";
    linkedin = "https://linkedin.com/in/alysnnix";
    email    = "4ly.alcantara@gmail.com";
  };
}
```

<br clear="all" />

> Lately: shipping [framebudget](https://framebudget.dev), a small library that checks how much of the 16.7 ms frame budget a device has before the first paint and only turns on the effects that fit. Everything on my machines is declared in Nix, and most of my code gets written in the terminal alongside Claude Code.

## most used

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
