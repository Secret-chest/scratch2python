name: Bug Report
description: File a bug report
title: "[Bug]: "
labels: ["bug", "triage"]
assignees:
  - Secret-chest
body:
  - type: markdown
    attributes:
      value: |
        File a bug report here.
  - type: textarea
    id: what-was-expected
    attributes:
      label: What did you expect to happen?
      placeholder: _What did you expect to happen?_
    validations:
      required: true
  - type: textarea
    id: what-happened
    attributes:
      label: What did actually happen?
      placeholder: _What did happen that you weren't expecting?_
    validations:
      required: true
  - type: textarea
    id: how-to-reproduce
    attributes:
      label: How did you make that happen?
      placeholder: _Tell us how to reproduce the issue._
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Relevant log output
      description: Please copy and paste any relevant log output. This will be automatically formatted into code, so no need for backticks.
      render: shell
  - type: checkboxes
    id: checks
    attributes:
      label: Latest version
      description: You must be running the latest Scratch2Python version.
      options:
        - label: I am running the **latest version**
          required: true
