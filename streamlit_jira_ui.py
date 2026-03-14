import os
import streamlit as st
from jira_integration import (
    JiraClient,
    EmailService,
    TicketStore,
    BugTicket,
    generate_bug_ticket_from_analysis,
    ticket_store,
    MANAGER_EMAIL,
)


def render_jira_tab(err_stats, err_cmd_patterns, log_texts, model):
    """Renders the Jira Integration tab content."""

    st.subheader("Auto-Generate Jira Bug Tickets")

    if not err_stats:
        st.info("Upload logs and run analysis first to generate bug tickets.")
        return

    st.markdown("### Detected Errors")
    st.caption("Select errors to generate Jira tickets from AI analysis.")

    selected_errors = []
    for i, (err, cnt) in enumerate(err_stats.most_common(10)):
        col1, col2, col3 = st.columns([0.05, 0.75, 0.2])
        with col1:
            checked = st.checkbox("", key=f"err_{i}")
        with col2:
            st.code(err, language=None)
        with col3:
            st.metric("Count", cnt)
        if checked:
            cmds = ""
            if err in err_cmd_patterns:
                cmds = ", ".join(
                    f"{cmd} ({c}x)"
                    for cmd, c in err_cmd_patterns[err].most_common(3)
                )
            selected_errors.append((err, cnt, cmds))

    st.markdown("---")

    manager_email = st.text_input(
        "QA Manager Email",
        value=MANAGER_EMAIL or "",
        placeholder="manager@company.com",
    )

    col_gen, col_send = st.columns(2)

    # ── Generate tickets ──
    with col_gen:
        if st.button("Generate Bug Tickets", type="primary", disabled=not selected_errors):
            st.session_state["generated_tickets"] = []

            progress = st.progress(0)
            for i, (err, cnt, cmds) in enumerate(selected_errors):
                with st.spinner(f"Analyzing error {i+1}/{len(selected_errors)}..."):
                    try:
                        ticket = generate_bug_ticket_from_analysis(
                            error_pattern=err,
                            error_count=cnt,
                            associated_commands=cmds,
                            log_source=f"{len(log_texts)} log file(s)",
                            llm_model=model,
                        )
                        st.session_state["generated_tickets"].append(ticket)
                    except Exception as e:
                        st.error(f"Failed to generate ticket for error: {e}")
                progress.progress((i + 1) / len(selected_errors))

            st.success(f"Generated {len(st.session_state['generated_tickets'])} ticket(s).")

    # ── Display generated tickets ──
    if "generated_tickets" in st.session_state and st.session_state["generated_tickets"]:
        st.markdown("### Generated Bug Tickets (Preview)")

        for i, ticket in enumerate(st.session_state["generated_tickets"]):
            severity_color = {
                "Critical": "red",
                "High": "orange",
                "Medium": "blue",
                "Low": "green",
            }.get(ticket.severity, "gray")

            with st.expander(
                f":{severity_color}[{ticket.severity}] {ticket.title}", expanded=True
            ):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**Failure Type:** `{ticket.failure_type}`")
                    st.markdown(f"**Severity:** :{severity_color}[{ticket.severity}]")
                with col_b:
                    st.markdown(f"**Assignee:** {ticket.suggested_assignee}")
                    st.markdown(f"**Log Source:** {ticket.log_source}")

                st.markdown("**Description:**")
                st.write(ticket.description)

                st.markdown("**Steps to Reproduce:**")
                st.write(ticket.steps_to_reproduce)

                st.markdown("**Error Pattern:**")
                st.code(ticket.error_pattern, language=None)

                new_title = st.text_input(
                    "Edit Title", value=ticket.title, key=f"title_{i}"
                )
                new_severity = st.selectbox(
                    "Edit Severity",
                    ["Critical", "High", "Medium", "Low"],
                    index=["Critical", "High", "Medium", "Low"].index(ticket.severity),
                    key=f"sev_{i}",
                )
                ticket.title = new_title
                ticket.severity = new_severity

    # ── Send for approval ──
    with col_send:
        tickets = st.session_state.get("generated_tickets", [])
        can_send = bool(tickets) and bool(manager_email)

        if st.button("Send to Manager for Approval", disabled=not can_send):
            email_svc = EmailService()
            sent = 0

            for ticket in tickets:
                token = ticket_store.add(ticket)
                success = email_svc.send_approval_email(ticket, manager_email, token=token)
                if success:
                    sent += 1

            if sent > 0:
                st.success(
                    f"Sent {sent} ticket(s) to {manager_email} for approval. "
                    f"Manager can approve/reject directly from the email."
                )
            else:
                st.error("Failed to send approval emails. Check SMTP settings in .env file.")

    # ── Pending approvals ──
    pending = ticket_store.pending
    if pending:
        st.markdown("---")
        st.markdown("### Pending Approvals")
        for token, ticket in pending.items():
            st.markdown(f"- **{ticket.title}** ({ticket.severity}) — `pending approval`")