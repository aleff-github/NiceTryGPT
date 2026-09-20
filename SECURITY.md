# Security Policy

## Supported versions

NiceTryGPT is currently an early proof of concept. Security fixes are applied to the latest version on `main`.

## Reporting a vulnerability

Please do not disclose a vulnerability publicly before it has been reviewed.

For security-sensitive reports, contact the maintainer through the contact information published on the GitHub profile of [@aleff-github](https://github.com/aleff-github).

Include only the information needed to reproduce the issue. Do not include third-party secrets, credentials, or data you are not authorized to share.

## Intentional vulnerable code

The CTFs under `examples/` intentionally contain security vulnerabilities for local training and testing. Those intentional challenge vulnerabilities are not production security issues in NiceTryGPT.

The examples bind to localhost by default and are not intended for deployment as real services.

## Scope

Reports about unintended behavior in the skill, examples, tests, or repository automation are welcome.
