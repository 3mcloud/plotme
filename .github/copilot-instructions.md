## Compliance Enforcement

- For every copilot task in this repository, run the compliance workflow before finishing.
- Treat compliance review as always-on, even when the user does not explicitly ask for it.
- Whenever adding generated content to the repository add the first and last lines of the content to the generated-log.md file in the root directory. Label each entry with the file name, line numbers where the content was inserted, date, and AI model. This will allow for tracking of generated content and attribution.
- generated-log.md contains a table. The column order is | Labeled in Source | Date | Model | File | Lines | First Line | Last Line |. The labeled in source column starts with 'no' and should be updated to 'yes' when the generated content is labeled in the source code with comments.

## When To Use Custom Agents

- Use the `3m-gai-compliance-source-scan` agent for full repository compliance scans, dependency/license review, or when the user asks about compliance. Only do this automatically before commits.
- Use the `3m-gai-compliance-labeling` agent only if requested. Do not use it automatically, as it adds extra comments to the code which some users may find undesirable especiially during development.
