# AI Log Analyzer & QA Intelligence Platform

An AI-powered QA platform that automates log analysis, error classification, root-cause detection, and Jira bug ticket creation — helping QA teams reduce manual triage time by up to 70%.

**Live App:** [ai-assistant-intelligence.streamlit.app](https://ai-assistant-intelligence.streamlit.app/)

---

## Demo

https://github.com/user-attachments/assets/YOUR_VIDEO_ID

---

## The Problem

QA engineers spend hours manually reading through CI/CD and application logs, identifying errors, classifying them, writing bug reports, and creating Jira tickets. This process is repetitive, slow, and error-prone — especially when dealing with thousands of log lines across multiple files.

## The Solution

This platform uses LLM-powered analysis (Mistral AI + LangChain) to automate the entire QA log triage workflow:

1. **Upload logs** — drag and drop CI/CD or application log files
2. **AI analyzes** — automatically detects error patterns, clusters recurring failures, and maps command-error co-occurrences
3. **Generate bug tickets** — AI auto-classifies each error (environment, code defect, flaky test, data issue) and generates complete bug reports with title, description, severity, steps to reproduce, and suggested assignee
4. **One-click Jira integration** — sends tickets to the QA manager via email for approval. On approval, the ticket is auto-created in Jira via REST API
5. **Confirmation** — manager receives a confirmation email with a direct link to the Jira ticket

---

## Features

### QA Assistant (Chat)
- Ask natural language questions about your logs
- Get AI-powered root-cause analysis and debugging suggestions
- Paste error snippets and get instant explanations
- Failure classification into categories: environment, code defect, flaky test, data issue

### Log Analytics Dashboard
- Automatic error pattern detection and clustering
- Command frequency analysis
- Command-error co-occurrence mapping
- Error examples with expandable details
- Quick summary metrics in sidebar

### Jira Integration with Email Approval
- AI auto-generates fully populated bug tickets from detected errors
- Inline editing of ticket title and severity before submission
- Email sent to QA manager with Approve/Reject buttons
- On approval, ticket is auto-created in Jira via REST API
- Confirmation email with direct Jira link sent after ticket creation
- Pending approval tracking in the dashboard

---

## Screenshots

### QA Assistant - AI Chat
![QA Assistant](Screenshots/qa_assistant.png)

### Log Analytics Dashboard
![Log Analytics](Screenshots/log_analytics.png)

### Jira Integration - Generate Tickets
![Jira Integration](Screenshots/jira_integration.png)

### Email Approval Request
![Approval Email](Screenshots/approval_email.png)

### Ticket Created in Jira
![Jira Ticket](Screenshots/jira_ticket.png)

### Confirmation Email
![Confirmation Email](Screenshots/confirmation_email.png)

---

## License

This project is open source and available under the [MIT License](LICENSE).