# Publishing and distribution

The extension ID is `gkaria.amber-material-theme`. The same VSIX contains both
color themes and the file icon theme and can be uploaded to both registries.
The terminal suite is a separate ZIP: users extract it and follow the included
README and terminal setup guide. It does not modify anyone's configuration.

## Build a release

Use Node.js 22 or newer and Python 3.10 or newer:

```sh
npm ci --ignore-scripts
npm run package:release
```

This checks generated files, runs the existing tests, and writes these files
to `dist/` (with the version from `package.json`):

- `amber-material-theme-1.1.1.vsix`
- `amber-material-terminal-suite-1.1.1.zip`
- `amber-material-1.1.1-SHA256SUMS.txt`

Before publishing a new release, update the version in `package.json` and
`package-lock.json` together (`npm version patch --no-git-tag-version`), finish
the changelog, and commit the release contents. Never replace an already
published version with different contents. The existing `v1.1.0` GitHub release
predates this workflow; use a new version for these packaging changes.

Upload the three matching files to a GitHub Release for the corresponding
version/tag. GitHub Actions artifacts are useful for review, but GitHub Release
assets are the public downloads to link to. The workflow below does not create
a GitHub Release automatically. Keep older files in `dist/` out of the upload.

Verify downloaded files on macOS with `shasum -a 256 -c
amber-material-1.1.1-SHA256SUMS.txt` or on Linux with `sha256sum -c` followed by
the same filename. Run the command from the directory containing both files.

## VS Code Marketplace setup

1. Sign in to [publisher management](https://marketplace.visualstudio.com/manage)
   and create or confirm ownership of publisher ID `gkaria`. A matching GitHub
   username does not create a Marketplace publisher.
2. Follow Microsoft's [publishing instructions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
   to configure authentication. For the supplied workflow, create a Marketplace
   **Manage** PAT and add it as the GitHub repository secret `VSCE_PAT`.
3. Alternatively, upload the reviewed VSIX through publisher management for
   the first release; this avoids configuring CI authentication immediately.

Microsoft currently documents retirement of global Azure DevOps PATs on
December 1, 2026 and recommends Microsoft Entra ID with workload federation.
The supplied PAT workflow is a short-term option. For continued automation,
configure an authorized Entra identity and use `vsce publish --azure-credential`
following Microsoft's guide before that deadline.

Once publication succeeds, the listing will be:
<https://marketplace.visualstudio.com/items?itemName=gkaria.amber-material-theme>.
Then users can run `code --install-extension gkaria.amber-material-theme`.
Do not advertise this listing as live before checking it.

## Open VSX setup

Follow the [Open VSX publisher instructions](https://github.com/EclipseFdn/open-vsx.org/wiki/Publishing-Extensions):

1. Log in with GitHub, connect an Eclipse Foundation account, and accept the
   publisher agreement yourself.
2. Create an access token in Open VSX settings. Store it as the GitHub repository
   secret `OVSX_PAT`. Do not commit it or paste it into an issue.
3. Create the `gkaria` namespace using `ovsx create-namespace gkaria` with
   `OVSX_PAT` set in your local environment. If it already exists, confirm that
   your account has publishing rights instead of attempting to recreate it.
4. [Claim namespace ownership](https://github.com/EclipseFdn/open-vsx.org/wiki/Namespace-Access)
   for verified ownership. Creating a namespace and claiming ownership are
   separate steps.

Once publication succeeds, the listing will be:
<https://open-vsx.org/extension/gkaria/amber-material-theme>.
Open VSX supports editors that use that registry; users of other compatible
editors can install the GitHub Release VSIX directly.

## GitHub workflow

After these changes are on the default branch, open **Actions → Package and
publish → Run workflow** and select the release tag or commit-bearing branch.
Both publish switches default to off: the initial run builds downloadable
artifacts only. Review the VSIX and ZIP before selecting either registry.

The registry jobs publish the exact VSIX produced by the package job. They run
independently, so a failure in one registry does not stop the other. If one
upload fails, rerun with only that registry selected at the same release tag.
Duplicate versions deliberately fail rather than silently claiming success.

For local publishing of a reviewed package, with credentials configured:

```sh
npx --no-install vsce publish --packagePath dist/amber-material-theme-1.1.1.vsix
npx --no-install ovsx publish dist/amber-material-theme-1.1.1.vsix
```

Use the actual release version in place of `1.1.1`.

## Distribution beyond editors

| Target | Direct distribution | Wider discovery |
| --- | --- | --- |
| Ghostty | Both files in `ghostty/`, installed using the main README | Contribute the palette to iTerm2-Color-Schemes; Ghostty consumes that collection |
| Windows Terminal | JSON fragments in `windows-terminal/` | The same upstream collection generates Windows Terminal schemes |
| OpenCode | JSON files in `opencode/` | Link the release and custom-theme installation instructions |
| Claude Code | JSON files in `claude-code/` | Link the release and documented minimum version in the terminal guide |
| Codex CLI | `.tmTheme` files in `codex/` | Link the release and installation instructions in the main README |
| Starship | `starship/amber-material.toml`, including both palettes | Submit a community preset to Starship |
| PowerShell | PSReadLine scripts in `powershell/` | Distribute with the terminal suite and profile instructions |
| Grok Build | Pager TOML files and reference palette JSON in `grok/` | Describe this as pager styling; the reference JSON is not a loadable full theme |

### Ghostty upstream contribution

Ghostty's [theme dependency](https://github.com/ghostty-org/ghostty/blob/main/build.zig.zon)
uses an iTerm2 theme collection snapshot. The route to bundled discovery is an
upstream contribution to
[iTerm2-Color-Schemes](https://github.com/mbadolato/iTerm2-Color-Schemes#contribute),
followed by Ghostty adopting a snapshot containing it. Acceptance does not
make it immediately available in installed Ghostty releases.

Prepare dark and light source schemes from the terminal palette, run the
upstream generators, add screenshots and credits according to that project's
current contribution instructions, and submit a PR. Use the terminal colors,
not the editor's intentionally different background. This also provides ports
for other terminals through the upstream generators. The existing Ghostty
files alone are not a complete upstream submission.

### Starship and other custom-theme loaders

[Starship's preset gallery](https://starship.rs/presets/) invites community PRs.
Prepare screenshots and a preset page alongside the TOML for that submission.
For [OpenCode](https://opencode.ai/docs/themes/) and the other targets, the
release bundle already provides a direct file distribution route; registry
publication of the VSIX does not install these files into other applications.

## Listing presentation

The README includes real dark and light VS Code screenshots, and the extension
has a 256 × 256 PNG icon derived from `assets/icon.svg`. Publish the repository
changes before uploading the VSIX: Marketplace renders README images from the
repository URLs, not from files on your machine. Keep all third-party notices
in both release artifacts.
