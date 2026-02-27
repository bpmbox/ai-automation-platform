# Milestone 2: GitHub Actions Workflow

**Status**: IN PROGRESS

**Started**: 2026-02-27

## Summary

GitHub Actions workflow to automatically sync Issue events to Supabase Realtime database.

## Tasks

### 2.1 Issue Webhook Listener - DONE
- File: `.github/workflows/sync-issues.yml`
- Triggers: `issues.opened`, `issues.closed`, `issues.edited`, `issues.deleted`
- Extracts: issue number, title, body, creator, labels, status

### 2.2 Secrets Configuration - DONE
- `SUPABASE_URL` - encrypted via NaCl, stored in GitHub Secrets
- `SUPABASE_ANON_KEY` - encrypted via NaCl, stored in GitHub Secrets

### 2.3 Supabase Sync Logic - IN TESTING
- HTTP POST to Supabase REST API
- Upsert configured: `on_conflict=issue_number`
- Awaiting first live issue event to confirm end-to-end sync

### 2.4 Error Handling - PLANNED
- Retry logic for transient failures
- Failure logging and notifications

### 2.5 Health Monitoring - PLANNED
- Workflow run history in Actions tab
- Alert on consecutive sync failures

## Workflow Flow

```
GitHub Issue Event
       |
       v
GitHub Actions Runner (ubuntu-latest)
       |
       v
Extract Issue Data (bash + GitHub context)
       |
       v
HTTP POST to Supabase REST API
       |
       v
Upsert into github_issues table
```
