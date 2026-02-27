# Milestone 3: VS Code Copilot Bridge

**Status**: PLANNED

## Summary

VS Code extension that bridges Supabase Realtime events with GitHub Copilot Chat,
enabling real-time AI collaboration directly in the developer's IDE.

## Architecture

```
Supabase Realtime
       |
       v
VS Code Extension (TypeScript)
       |
       v
GitHub Copilot Chat Panel
       |
       v
Developer sees AI responses in IDE
```

## Tasks

### 3.1 VS Code Extension Setup
- Create TypeScript extension with VS Code Extension API
- Webpack build configuration
- Extension manifest (package.json) for Marketplace

### 3.2 Supabase Realtime Listener
- Subscribe to `ai_responses` table changes
- Filter by `agent_id` to route responses correctly
- Handle connection drops and reconnects

### 3.3 Copilot Chat Integration
- Display AI responses in VS Code Copilot Chat panel
- Markdown and code syntax highlighting support
- Preserve message history within session

### 3.4 Response Sync Back to Supabase
- Capture user messages from Copilot Chat
- Insert into `ai_responses` with `agent_id = "copilot-extension"`
- Enable bidirectional AI communication

### 3.5 Error & State Management
- Graceful handling of Supabase connection failures
- Offline queue for messages when disconnected
- Agent state validation before processing

### 3.6 Documentation & Testing
- VS Code Marketplace publication
- Integration tests for Realtime listener
- User guide and troubleshooting documentation

## Dependencies

- Milestone 2 must be complete and tested
- Supabase `ai_responses` table (from Milestone 1)
- VS Code Extension API (^1.85.0)
- `@supabase/supabase-js` client library
