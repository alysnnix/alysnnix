<!--
  README variant: manpage. A man page: the ribbon as shaded text, then NAME, SYNOPSIS, DESCRIPTION, PROJECTS, ENVIRONMENT, SEE ALSO, langs. Plain markdown below the art, so it wraps on mobile.
  To use it: cp examples/README-manpage.md README.md, then delete this comment.
  Asset paths are relative to the repo root (./assets/...), so images only resolve once it lives there.
  Art: scripts/gen_ascii.sh regenerates assets/ascii/ (scripts/ascii_ribbon.py draws the ribbon).
  Keep the langs markers: .github/workflows/github-langs.yml rewrites the block between them every day.
-->

```text
ALY(1)                       aly.engineer                       ALY(1)

                            ...:::--=++=--:
                      ...::.:::::::--=+#@%#@%:                             ..:::
@%*+==::::.      :-:.::.::::::::-=++#*%@@@@@@@@=                      ..::::::::
@@@%%***+=+##+***--=-.::.::::-=++**##%+:       %@@@#=.           ::-=+=:::::::--
.+#*+++==+===++***+:-=..:.==++*+#*#%=            #@@@@@#*=+*++=+*=+==+=+:--==++*
  .=++==-----==++*+=-::-:+=++++*+#=               .*%%###%*%@#*+=*===--:-+=++*+*
    .-==--::.::::..:::.:+-++++++=                   .=*+=-==+*+==::-:::::-=*==:.
       :---::::.:--:..:::+==*=:                        :-----====-:::-::..:
         ..:::.:::-:::..:--:                               ..........
              ..........
```

**NAME**
&nbsp;&nbsp; aly, software engineer who works close to the money

**SYNOPSIS**
&nbsp;&nbsp; `aly [--front react next.js typescript] [--back python django fastapi]`

**DESCRIPTION**
&nbsp;&nbsp; Writes software since 2019, at Seazone since 2021. Spends most of the time on checkout and payments (3DS, Pix, PayPal), on the A/B tests that decide what ships, and on keeping pages fast on the phones people actually own. Cares about design systems that teams reuse instead of fork.

**PROJECTS**

[`framebudget`](https://framebudget.dev)
&nbsp;&nbsp; Before the first paint, measures how much of the 16.7 ms frame budget a device has and enables only the visual effects that fit. 4.6 KB gzip boot script, FPS governor, React, Vue and Angular bindings. MIT, [on npm](https://www.npmjs.com/package/framebudget).

[`devproxy`](https://github.com/alysnnix/devproxy)
&nbsp;&nbsp; A loopback IP per Docker Compose project, so two stacks can share port 5432. Go.

[`apollo-fleet`](https://github.com/alysnnix/apollo-fleet)
&nbsp;&nbsp; Several isolated Apollo streaming hosts on one Windows machine. Rust.

**ENVIRONMENT**
&nbsp;&nbsp; `OS=nixos` &nbsp; `EDITOR=claude` &nbsp; `NOW=framebudget`

**SEE ALSO**
&nbsp;&nbsp; [aly.engineer(1)](https://aly.engineer), [blog(7)](https://aly.engineer/blog), [resume(5)](https://resume.aly.engineer), [linkedin(1)](https://linkedin.com/in/alysnnix), [mail(1)](mailto:4ly.alcantara@gmail.com)

**FILES**

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
