# Security Policy

## Reporting a vulnerability

Please report security issues **privately**. Do not open a public issue for a
vulnerability.

Use GitHub's [private vulnerability reporting](https://github.com/kyrisu/alfred-translate/security/advisories/new)
for this repository. You'll get an acknowledgement as soon as the report is
reviewed, and a fix or mitigation will be coordinated before any public
disclosure.

## Scope and threat model

This workflow takes free-form text typed into Alfred and passes it to a
translation backend. The most relevant concern is **shell injection** through
that input. As of the argv conversion, the Script Filter runs the Python entry
point as an external script with the query delivered via `argv` — Alfred does
**not** interpolate the query into a shell command line, so shell
metacharacters (`"`, `` ` ``, `$(...)`, `;`, `&&`) are treated as literal text
rather than evaluated.

The vendored `bin/translate` binary is built from
[scriptingosx/translate-cli](https://github.com/scriptingosx/translate-cli);
vulnerabilities in the upstream binary should also be reported upstream.
