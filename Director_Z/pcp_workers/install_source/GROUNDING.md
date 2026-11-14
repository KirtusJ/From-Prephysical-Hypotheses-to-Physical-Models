# Where plugins and Store apps install from: grounding, before anything is built

Director Z, 14 November 2026. Stage 1 of 3: grounding (this file), design, build. Nothing is built yet.

The principal's instruction: no need to ask; ground against common standard practice; learn from Windows, Linux
and macOS, and consider OpenBSD and FreeBSD, in particular how each excels, how it does not, and its weak points
and failures; ground externally before building; take the time it needs. Also: the principal likes Composer's
system in PHP; check against it and see what is worth taking.

## How this was grounded, and its limits

Sixteen web searches on 14 November 2026. The links below are the pages the searches returned. **Limit, stated
plainly:** the search tool returns summaries; direct fetches of three primary pages failed because their hosts
are outside this session's allowed network (`flak.tedunangst.com`, `theupdateframework.io`, `man.freebsd.org`).
So every external statement below is from a search summary of the linked page, not from my own reading of the
page, unless marked otherwise. Statements marked [own] are my general knowledge and are not sourced here; they
must be sourced or dropped before the design relies on them. What was tested by me on this machine is marked
[tested].

## 1. What is true today [tested]

Claude Code 2.1.325, isolated configuration folder:

- `KirtusJ/pcp-claude` and `KirtusJ/pcp-os-claude` are plugin folders without a marketplace file; neither can be
  registered as an install source.
- `KirtusJ/pcp` has a marketplace file only in the subfolder `PCP_1.0_Plugins`; it works by local path after a
  clone, installs build 19, and its programs arrive without the executable bit.
- A marketplace file that points at the two plugin repositories validates and installs both at build 22; the
  hook runs when `pcp-os-claude` is taken at its fix branch.
- Each of these repositories is a sealed inventory checked against its own manifest, so a file added to one
  shows as a difference.
- The PCP OS Store has no install source: instruments are a table compiled into the host; a module is added
  from a local folder. The plugin's own README says of its programs: "Neither is signed, and nothing in an
  edition lets you check that a program was built from its source."

## 2. The five systems: where each excels, where it fails

### OpenBSD

Excels:
- One small tool for one job. `signify` was written in 2014 because existing tools were too complex; "no key
  servers, no web of trust, just keys". It has verified every release, patch and package since OpenBSD 5.5.
  ([signify](https://flak.tedunangst.com/post/signify), [isopenbsdsecu.re](https://isopenbsdsecu.re/mitigations/signify/),
  [BSDCan 2015](https://www.bsdcan.org/2015/schedule/events/545.en.html))
- Key rotation without infrastructure: the key for the release two versions ahead is generated early and
  shipped inside the current release, so each release carries the trust path to the next.
  ([signify](https://flak.tedunangst.com/post/signify))
- The base system and the packages are separate layers with separate tools: `syspatch` and `sysupgrade` touch
  the base only, `pkg_add` touches packages only, and packages must match the base branch.
  ([OpenBSD Handbook: updates](https://www.openbsdhandbook.com/system_management/updates),
  [upgrade](https://www.openbsdhandbook.com/upgrade/))

Fails or is weak:
- The keys themselves are not signed; trust in the first key is implicit, carried from one release to the next.
  Whoever obtains the first release from a bad place has no anchor.
  ([signify](https://flak.tedunangst.com/post/signify))
- Packages originally carried the signature inside the archive, so the archive had to be unpacked before it
  could be checked; this was fixed later by signing the compressed stream.
  ([signify](https://flak.tedunangst.com/post/signify))
- The author wrote a separate post on signify's shortcomings
  ([signify-shortcomings](https://flak.tedunangst.com/post/signify-shortcomings)); **not read**, host blocked.
- No revocation mechanism and no transparency log [own].

### FreeBSD

Excels:
- The repository catalogue is signed, and the client trusts fingerprints kept in a directory with `trusted` and
  `revoked` subdirectories, so revocation has a place.
  ([pkg-repo(8)](https://man.freebsd.org/pkg-repo(8)))
- Base and third-party software have separate repositories and, from 15.0, separate signing keys per major
  version (`/usr/share/keys/pkgbase-15` against `/usr/share/keys/pkg`).
  ([forum thread](https://forums.freebsd.org/threads/freebsd-15-aarch64-pkgbase-signing-keys.100785/))
- Ports: every package can be rebuilt from source by the user with the same recipe [own].

Fails or is weak:
- The move of the base system into packages (pkgbase) broke upgrades in the field: "No trusted public keys
  found" from a wrong fingerprint path or a stale local override, and a repository relocation announced during
  the 15.0 pre-release. Changing where things are fetched from and which key signs them is itself a failure
  point. ([pkgbase breakage, freebsd-stable](https://lists.freebsd.org/archives/freebsd-stable/2025-December/003733.html),
  [forum](https://forums.freebsd.org/threads/convert-15-0-release-to-pkgbase.100491/))
- The sources here are forum and list posts, not the Handbook; the details are unverified.

### Linux (Debian and Ubuntu; Nix; Snap and Flatpak)

Excels:
- apt: one signed metadata file (`InRelease`) holds hashes of the package lists, which hold hashes of every
  package, so one signature covers the whole archive, and mirrors need not be trusted.
  ([Ubuntu: archive verification](https://documentation.ubuntu.com/security/software-integrity/archive-verification/))
- Nix: a component's path contains a hash of everything that went into building it; nothing is ever
  overwritten; an upgrade is a new path and a switch of one pointer, so upgrades are atomic and roll back.
  ([Nix](https://en.wikipedia.org/wiki/Nix_(package_manager)), [Dolstra, HotOS 2007](https://www.usenix.org/legacy/event/hotos07/tech/full_papers/dolstra/dolstra_html/))
- Reproducible builds: "given the same source code, build environment and build instructions, any party can
  recreate bit-by-bit identical copies". ([definition](https://reproducible-builds.org/docs/definition/))

Fails or is weak:
- A signature proves who published, not what was built. The xz backdoor (CVE-2024-3094) lived in the release
  tarballs and not in the Git repository; packagers built from the tarballs. The lesson drawn: build from the
  tagged source and compare the release archive with a clean build of it.
  ([XZ Utils backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor),
  [the git-tarball gap](https://manuelfedele.github.io/posts/xz-utils-backdoor-the-git-tarball-gap))
- The verifier is code and has bugs: CVE-2016-1252 let leading garbage in a signed file be read as metadata;
  CVE-2019-3462 let a redirect inject content over plain HTTP.
  ([CVE-2016-1252](https://mondoo.com/vulnerability-intelligence/vulnerability/CVE-2016-1252),
  [CVE-2019-3462](https://access.redhat.com/security/cve/CVE-2019-3462))
- A key trusted for one source was trusted for all (`apt-key`); the fix is to bind each key to its source.
  ([Cloudflare](https://blog.cloudflare.com/dont-use-apt-key))
- Snap: the store was flooded with fake wallet applications from 2024; later, attackers took over old publisher
  accounts through expired e-mail domains; removal sometimes took days. A central store with self-service
  publishing is only as good as its review.
  ([Help Net Security](https://www.helpnetsecurity.com/2026/01/21/linux-malware-snap-store/),
  [popey](https://blog.popey.com/2026/01/malware-purveyors-taking-over-published-snap-email-domains/))
- Snap updates on the publisher's schedule, with no simple way for the user to refuse; the same channel that
  removes malware can push it to everyone. ([snapcraft forum](https://forum.snapcraft.io/t/disabling-automatic-refresh-for-snap-from-store/707/150))
- Flatpak: the sandbox is declared by the application, and many declared permissions allow escape; "you can
  only trust the publisher and reviewer". ([LWN](https://lwn.net/Articles/966908))
- Dependency resolution between independently versioned shared libraries ("dependency hell") [own].

### macOS

Excels:
- One identity per developer, and a central scan (notarization) before software runs by default; the App Store
  adds a sandbox and review [own].

Fails or is weak:
- Launching depended on a live server. On 12 November 2020 the certificate-status server was slow, and
  applications hung at launch worldwide until the check timed out. A security check that needs the network at
  use time is an availability failure waiting.
  ([TidBITS](https://tidbits.com/2020/11/13/apple-network-failure-destroys-an-afternoon-of-worldwide-mac-productivity/),
  [Eclectic Light](https://eclecticlight.co/2020/11/15/last-week-on-my-mac-making-essential-services-fail-safe/))
- The same check sent identifying data to the vendor; Apple later said it had stopped logging addresses.
  ([9to5Mac](https://9to5mac.com/2020/11/15/apple-explains-addresses-mac-privacy-concerns/))
- The central scan approved malware: Shlayer installers were notarized in 2020, revoked, and came back under
  another developer identity. ([TechCrunch](https://techcrunch.com/2020/08/31/apple-notarized-mac-malware/))

### Windows

Excels:
- A single vendor-signed update channel for the system, and installers with a transaction model that is meant to
  roll back [own].

Fails or is weak:
- Shared mutable libraries. Installers placed shared DLLs in the system directory and broke each other ("DLL
  hell"). The cure, side-by-side storage of many versions, grows without bound and is collected only later.
  ([Microsoft: why VC8 installs to WinSxS](https://learn.microsoft.com/en-us/archive/blogs/martynl/why-does-vc8-install-libraries-to-winsxs))
- Rollback that leaves the system worse: after a failed Visual Studio 2005 SP1 install, rollback left a policy
  pointing applications at a runtime version that no longer existed.
  ([Microsoft setup blog](https://devblogs.microsoft.com/setup/?p=1703))
- The update channel's signature was forged. Flame (2012) used an MD5 collision against a Microsoft licensing
  certificate to sign code that Windows Update accepted, years after MD5 was known to be weak. A signing scheme
  is only as strong as its weakest still-accepted algorithm and its least-guarded certificate.
  ([Threatpost](https://threatpost.com/microsoft-details-flame-hash-collision-attack-060612),
  [Green](https://blog.cryptographyengineering.com/2012/06/05/flame-certificates-collisions-oh-my/))
- A signed update pushed to everyone at once. CrowdStrike, July 2024: a content file read one field more than
  the code supplied, content updates had not been tested like code, and there was no staged rollout; more than
  8 million machines went into reboot loops.
  ([root cause analysis](https://crowdstrike.com/wp-content/uploads/2024/08/Channel-File-291-Incident-Root-Cause-Analysis-08.06.2024.pdf))

## 3. Language package managers, and Composer

Failures seen elsewhere:
- npm, 2016: one author unpublished 273 packages and builds failed worldwide for about two and a half hours.
  Published versions must not be removable. ([left-pad](https://www.wikipedia.org/wiki/Left-pad))
- npm, 2018: a maintainer handed a package to a stranger, who added a malicious dependency. A quiet change of
  owner is a change of trust. ([LWN: event-stream](https://lwn.net/Articles/773121))
- Dependency confusion, 2021: tools preferred a public package over a private one of the same name; more than
  35 organizations were affected. ([Birsan](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610))
- Typosquatting on PyPI: 40 attacks counted between 2017 and 2020, most against the top 500 names.
  ([IQT](https://www.iqt.org/library/bewear-python-typosquatting-is-about-more-than-typos))

Composer (PHP), checked against the above:

What it does well, and what is worth taking:
- **The index holds metadata only and points at the repositories where the code lives.** Packagist is "an index
  of metadata read from Git repositories", with code served by the Git host. This is exactly our situation:
  the code is already in repositories. ([Packagist glossary](https://socket.dev/glossary/packagist),
  [repositories](https://getcomposer.org/doc/05-repositories.md))
- **The lock file.** `composer.lock` records, for each package, the exact commit it resolved to, so every
  machine installs the same thing. ([Packagist blog](https://blog.packagist.com/closing-composers-download-fallback-paths-in-private-packagist/))
- **Immutable versions.** Once a stable version is published, the Git reference it points to never changes.
  ([Immutable versions on Packagist](https://blog.packagist.com/immutable-versions-on-packagist/))
- **Sources are declared by the project.** A `repositories` entry of type `vcs`, `path`, or `composer` lets a
  project take a package from its own Git URL, a local folder, or its own index, with no central gatekeeper.
  ([repositories](https://getcomposer.org/doc/05-repositories.md))
- Code that runs at install time (plugins) must be allowed by name [own; the search did not confirm why
  `allow-plugins` was introduced].

Where it is weak:
- **No signature on packages.** Trust rests on the transport and on the Git host. For a Packagist package the
  archive is a zip the Git host builds for the commit, and the recorded checksum is empty, because the index
  never held the bytes. The lock pins a commit, not bytes. ([Packagist blog](https://blog.packagist.com/closing-composers-download-fallback-paths-in-private-packagist/),
  [critique, dated](https://unixsheikh.com/articles/composer-packagist-a-bad-implementation.html))
- The index service itself was attackable: an argument injection in Packagist (CVE-2022-24828) could have let an
  attacker change what packages pointed to.
  ([SonarSource](https://www.sonarsource.com/blog/securing-developer-tools-a-new-supply-chain-attack-on-php/))
- Repositories are tried in order and the first match wins, which is the shape that dependency confusion needs.
  ([repositories](https://getcomposer.org/doc/05-repositories.md))

## 4. The attack list the design must answer

From The Update Framework's catalogue ([security page](https://theupdateframework.io/security/), **not read**, host
blocked; names as given by the search summary and [Wikipedia](https://en.wikipedia.org/wiki/The_Update_Framework)):
arbitrary installation, rollback to an older version, indefinite freeze (being shown stale metadata forever),
mix-and-match of metadata from different times, fast-forward, slow retrieval, and compromise of one key. Its
means: versioned metadata, expiry times, and several roles with separate keys. A caution from its own community:
expiry trades one risk for another, because a client that cannot fetch fresh metadata then cannot install.
([sigstore blog](https://blog.sigstore.dev/the-update-framework-and-you-2f5cbaa964d5))

## 5. What follows for PCP (requirements; a design comes next, not here)

Each line names the lesson it comes from.

1. **Index apart from payload** (Composer; apt). A small index that lists what exists and where, kept outside
   every sealed inventory, so that adding or updating an entry never changes a sealed edition.
2. **Pin bytes, not names** (Composer's weak point; npm lock integrity; Nix). Each entry names an exact commit
   and a digest of the installed files. The repositories already carry manifests of digests; the index should
   name the manifest's digest.
3. **Immutable versions** (left-pad; Packagist). A published version is never changed or removed; a fix is a
   new version.
4. **One small verifier, one key purpose, a place for revocation, and the next key shipped in the current
   release** (OpenBSD; FreeBSD's `revoked`; Flame; the apt verifier bugs). No web of trust. Each key bound to
   one source (the `apt-key` lesson). In PCP OS the verifier is Rust (Rust holds primacy).
5. **Base apart from apps** (OpenBSD, FreeBSD). The host program is the base and is replaced only with the
   agreed notice; Store apps and modules are a separate layer that cannot change the base.
6. **Atomic install with a way back that is tested** (Nix; the MSI rollback failure). Install beside the old
   version, switch one pointer, keep the old; a test shows the way back works.
7. **No forced updates, and no single push to everyone** (Snap; CrowdStrike). The user's side decides when; a
   new version goes to one place first.
8. **Verification must not need the network at use time** (Apple, November 2020). Check at install, record the
   result; running does not call home.
9. **Nothing runs at install time unless allowed by name** (Composer plugins; npm install scripts [own]).
10. **Build from the tagged source, and make the build checkable** (xz; reproducible builds). Today nothing
    lets a reader check that the shipped program was built from its source; that is the largest gap.
11. **Names carry their owner, and no first-match across sources** (dependency confusion; typosquatting).
12. **Every install is a recorded fact** (PCP's own strength, which none of the five has in this form): the
    install, its source, commit and digest go into the register as a host-observed event.
13. **Changing where things come from is itself a risky change** (FreeBSD pkgbase). The first location chosen
    should be one that need not move.

## 6. Open before the design is fixed

- Read the three blocked primary pages (signify's shortcomings, the TUF attack list, `pkg-repo(8)`), or have
  them supplied. Until then items 4 and the attack list rest on summaries.
- Source or drop every line marked [own].
- Not yet searched: SolarWinds (a signed update from a compromised build system), Homebrew's 2018 incident, the
  2016 Linux Mint image replacement, winget and the Microsoft Store, the OpenBSD FAQ on package signing, and
  why Composer introduced `allow-plugins`.
- Decide with Director G: where the index lives without touching a sealed inventory (a branch that holds only
  the index, or a small repository), and whether verifying a signature in the host justifies a second
  dependency beside `sha2`.

## 7. Corrections after Director G read the primary sources (14 November 2026)

Director G, from an environment that can reach them, read the pages this session could not, and posted the
reading on `KirtusJ/pcp` pull request 29 (two comments, with links to the author's BSDCan paper, archived copies
of both signify essays, the pinned `pkg.conf(5)`, the FreeBSD release configuration, the TUF specification and
Composer's documents). **This is Director G's reading, not mine**: `www.openbsd.org` and `web.archive.org` were
also unreachable from here when I tried again. A different model family read the sources; that reduces exposure
and is not my own verification. The text above is left as first written; these lines correct it.

OpenBSD:
- The signify essay was published on 31 December 2013; the tool shipped in 5.5 in 2014. Section 2 says "written
  in 2014".
- The key schedule, from the author's paper: after 5.6, the keys for 5.8 were created and distributed inside the
  signed 5.7. Authenticating a release carries trust forward from a first key that must be trusted
  independently.
- The author's own list of shortcomings: limited detection of a freeze in the offline scheme; the old 64-bit
  checksum on the secret-key file as an oracle for testing candidate keys if that file is stolen; the
  unpack-before-verify exposure concerned historical packages (signed gzip came later; base sets already used a
  different order); package downgrades are distinguished from base rollback, and a later build timestamp is
  mentioned.
- My line "no revocation mechanism and no transparency log [own]" is **withdrawn**: the sources do not justify a
  blanket claim about present facilities.

FreeBSD:
- Catalogue signing is optional in `pkg` and recommended; the official 15.0 release configuration selects
  fingerprint checking for both ports and the separately configured base repository.
- The client reads local trust material; a revoked entry can reject a signer, but **delivering** revocation in
  time is a separate obligation that the directory layout does not meet by itself.
- The pkgbase failure was traced by an operator and the release engineer to a stale local override. So the
  lesson is narrower than I wrote: a local override that outlives a relocation fails closed and confusingly.
  Requirement 13 stands, with that reason.

The Update Framework:
- The catalogue also names endless downloads, unnecessary dependencies, valid packages returned for the wrong
  request, and a mirror obstructing updates. Director G reports that the list does not use the term "slow
  retrieval"; the search summary I used said it did. Unresolved between two secondary readings; if a slow
  transfer matters to PCP it gets its own test.
- The specification starts from a trusted root and requires each root rotation N to N+1 to be signed to both
  the old and the new thresholds.
- Expiry is evaluated for the update operation. Running an installation that was already verified, offline, is
  a different scope. This supports requirement 8 and bounds it: freshness is checked when updating, not when
  running.

Composer:
- In Composer 2 repositories are canonical by default: once a higher-priority source has a package, versions of
  it on lower-priority sources are excluded. So my sentence "the first match wins, which is the shape that
  dependency confusion needs" is **wrong as a criticism of Composer 2**; canonical priority is the defence. What
  remains exposed: a name missing from the private source, and sources marked non-canonical.
- `allow-plugins` defaults to empty and was introduced in 2.2 to control plugin execution. This confirms the
  line I had marked [own].

Effect on the requirements: none is removed. Requirement 4 gains "rotation signed by both the old and the new
key" (TUF) beside "next key shipped in the current release" (OpenBSD). Requirement 11 becomes "names carry their
owner, and sources have an explicit priority with the first holder of a name final" (Composer 2).

## 8. Scope, extended by the principal (14 November 2026)

"Likewise, users and machines need to be able to install applications from the store, and modules, the same."
So the design covers three kinds of thing through one mechanism, and two kinds of installer:

| What is installed | Today [tested or read in the source] | Needed |
|---|---|---|
| Plugins (Claude, and Director G's side's packages) | by a marketplace file on a branch; works, with the executable-bit fault open | the same index, pinned and checked |
| Store applications (instruments) | a fixed table compiled into the host; none can be added without rebuilding the host | an application that can be fetched, checked and installed without replacing the host |
| Modules | `pcpos module add <register> <folder>` from a local folder only | the same, from the index |

| Who installs | Needed |
|---|---|
| A person | one command (and, where there is a screen, one action) that names the thing, shows what it is and where it comes from before anything changes, and can be undone |
| A machine (an assistant or a program through the tool server, a scheduled job) | the same operation as a tool call with the same checks and the same record; no step that needs a person unless the standard in force says a person must allow it |

Requirements added to section 5:

14. **One mechanism for plugins, Store applications and modules.** One index format, one verifier, one install
    record. A second path for one kind is a second place for the failures of section 2.
15. **The same operation for a person and for a machine**, with the same checks. A machine's install is
    recorded with the machine as actor and is bounded by what the register's standard allows; a person can see
    and undo it. (From the failures above: a channel that installs for everyone without their say is the Snap
    and CrowdStrike shape; a check that only a person can pass is no check for a machine.)
16. **An installed application cannot widen its own reach.** What it may touch is declared in the index entry,
    shown before install, and enforced by the host, not by the application (the Flatpak lesson: a sandbox the
    application declares for itself protects nobody).

The hard part, stated now so that it is not discovered later: instruments are compiled Rust inside the host.
Installing one at run time means either (a) data-only applications interpreted by the host, (b) separate
programs the host starts with declared capabilities, as the kernel already does for user programs, or
(c) rebuilding the host, which is replacing the base. (b) matches the base-and-apps separation and the
kernel's capability model; (c) is not installation. This is a design decision for stage 2, with Director G,
and Rust holds primacy in it.

### Added by the principal, same day: the Store needs a command-line and a graphical implementation

17. **Two front ends over one core.** The Store is implemented both as commands (`pcpos store ...`, and the
    same operations as tool calls for machines) and as a graphical view. Both call the same Rust operations:
    list, show, verify, install, remove, undo. Neither front end holds logic of its own, so a check cannot be
    present in one and missing in the other. (The failure this avoids is the one in section 2 where a
    graphical store and a command path had different rules: a store reviewed in its window and unreviewed
    through its command line protects only the people who use the window.) What exists today to build on:
    the host's command table and tool server in Rust; the kernel's display, keyboard and drawing code; and
    Director G's recorded benchmark of a viewer. What the graphical view runs on (the kernel's own display, a
    terminal interface in the host, or a page served locally by the host) is a stage 2 decision; the order of
    work is the core first, the commands second, the graphical view third, each with tests in Rust.

Stages, restated: 1 grounding (this file; done, with section 7's corrections); 2 design, posted to Director G
before anything is built; 3 build: core, commands and tool calls, graphical view, in that order.
