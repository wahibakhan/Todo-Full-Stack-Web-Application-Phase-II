# API Contracts

**Feature**: 001-console-todo
**Date**: 2025-12-29

## Overview

This directory typically contains API contracts (OpenAPI/GraphQL schemas) for features that expose HTTP endpoints or external APIs.

## Not Applicable for Phase 1

**Console Todo Application** is a standalone command-line interface application with no network communication or HTTP API endpoints (per Phase 1 Constitution constraint C-003).

**No contracts needed because**:
- No REST API endpoints
- No GraphQL schema
- No HTTP server
- No external integrations
- Console-only interface using `input()` and `print()`

## Internal "Contracts" (Python Function Signatures)

While there are no API contracts, the application does have internal contracts defined by Python function signatures with type hints. These are documented in:

- **Data Model**: `specs/001-console-todo/data-model.md`
  - Task dataclass structure
  - TaskStorage public methods
  - Custom exception signatures

- **Code Implementation**: `src/todo_app/`
  - `models.py` - Task dataclass
  - `storage.py` - TaskStorage class methods
  - `cli.py` - CLI function signatures
  - `main.py` - Application entry point

## Future Phases

API contracts will become relevant in future phases:

- **Phase 2**: May expose CLI commands as programmatic API (internal Python functions)
- **Phase 3**: May introduce REST API or web interface with OpenAPI specification
- **Phase 4+**: May add GraphQL, WebSocket, or other API protocols

For Phase 1, all interfaces are internal Python function calls with type hints serving as contracts.
