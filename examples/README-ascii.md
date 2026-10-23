<!--
  README variant: ascii. Portrait as ASCII art beside a Nix attrset (regenerate with scripts/gen_ascii.sh), then intro, projects, links, langs.
  To use it, copy this file over the repo root README.md (cp examples/README-ascii.md README.md).
  Asset paths are relative to the repo root (./assets/...), so images only resolve once it lives there.
  Keep the langs markers: .github/workflows/github-langs.yml rewrites the block between them every day.
-->

## hey, i'm aly

```nix
@@@@@@@@@@@@%%%%%%%@%+
@@@@@@@@%*+=+++*#%%@%@#:
@@@@%%#*=....:-:-+*#%@@%+:
@@@#+==-:..::::..:-==#@%%%:
@@#**=--::.. .-+**+=--%*.*-       {
@@%#*+--:  .=***++=--:-- -+         name  = "alysson alcantara";
@@@%%%##*=::-===*=-:..:- =%.        role  = "software engineer @ seazone";
@@@%%%%*#%*====-:......--%%-        since = 2019;
@@%%%#*+#@#=---:     ..-@@#-        front = [ "react" "next.js" "typescript" ];
@@@#*+++*%%-::-=:    .::%%#-        back  = [ "python" "django" "fastapi" ];
@@@%#+=-+%*: .::.    .::%%*+.       depth = [ "payments" "a/b tests" "perf" ];
@@@@@*=-=**+::. .--. .:+@@##*+++    os    = "nixos";
@@@@@@*++*#*==--==.  :-+@@@@@@@@    home  = "https://aly.engineer";
@@@@@@@%**##*=-:.  ..-:+@%@@@@@%  }
@@@@@@@@@%#*+-:.    :- *@%@@@@@@
@@@@@@@@@@%#*+:. ..::. #@@@@@@@@
@@@@@@@@@@#***+---:.. :@@@@@@@@@
@@@@@@@@@@%*==+=-:....*@@@@@@@@@
```

I'm Aly, a software engineer in Brazil. I've been writing software since 2019 and have been at Seazone since 2021, where most of my work sits close to the money: checkout and payments (3DS, Pix, PayPal), the A/B tests that decide what ships, and the performance work that keeps pages quick on cheap phones. React, Next.js and TypeScript on the front, Python with Django and FastAPI behind it.

Outside work I build small tools for problems I keep running into, keep my whole machine in Nix, and write most of my code alongside Claude Code.

## things i've made

- **[framebudget](https://framebudget.dev)** measures, before the first paint, how much of the 16.7 ms frame budget a device really has, then turns on only the visual effects that fit. A 4.6 KB gzip boot script, an FPS governor that backs off when frames drop, and bindings for React, Vue and Angular. MIT, on [npm](https://www.npmjs.com/package/framebudget), source at [framebudget/core](https://github.com/framebudget/core).
- **[aly.engineer](https://aly.engineer)** is my site: a lab of small experiments, the blog, and a handwritten signature that unwinds into a ribbon of threads.
- **[resume.aly.engineer](https://resume.aly.engineer)** is my resume as a site, built with Astro in Portuguese and English and served from Cloudflare Workers.
- **[devproxy](https://github.com/alysnnix/devproxy)** gives every Docker Compose project its own loopback IP, so two stacks can both use port 5432 without remapping anything. Go.
- **[apollo-fleet](https://github.com/alysnnix/apollo-fleet)** runs several isolated Apollo (Sunshine) streaming hosts on one Windows machine, so more than one Moonlight client can play at once. Rust.
- **[paseo-github-integration](https://github.com/alysnnix/paseo-github-integration)** brings GitHub issues, pull requests, Projects boards and reviews into Paseo, one click away from a coding agent.

## find me

[aly.engineer](https://aly.engineer) &nbsp;&nbsp; [blog](https://aly.engineer/blog) &nbsp;&nbsp; [resume](https://resume.aly.engineer) &nbsp;&nbsp; [linkedin](https://linkedin.com/in/alysnnix) &nbsp;&nbsp; [4ly.alcantara@gmail.com](mailto:4ly.alcantara@gmail.com)

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
