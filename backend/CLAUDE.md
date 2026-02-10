# Claude Code Rules - Backend Component

This file governs AI-assisted development for the backend component of The Evolution of Todo - Phase II & III.

## Task Context

**Your Surface:** You operate on the backend component level, providing guidance for API, database, and server-side functionality.

**Your Success is Measured By:**
- All outputs strictly follow the user intent and spec requirements.
- All changes align with existing backend architecture (FastAPI, SQLModel, PostgreSQL).
- All implementations maintain Phase II foundation integrity while supporting Phase III extensions.
- All changes reference specific spec sections.

## Core Guarantees (Backend Product Promise)

- **Spec Compliance:** All implementations must follow the backend specifications in `specs/002-backend-todo-api/spec.md` and Phase III AI agent specs
- **Phase II Foundation:** Never modify or break existing Phase II functionality
- **Security Model:** Maintain strict multi-tenant isolation and JWT verification
- **API Contract:** Preserve all existing API endpoints and contracts

## Development Guidelines

### 1. Spec-First Implementation:
- ALWAYS read and reference the backend specs before making changes
- Derive all implementation details from spec requirements
- Maintain traceability between code and spec requirements

### 2. Phase II Preservation:
- Phase II (Todo Full Stack) remains completely immutable in terms of core functionality
- All Phase III (AI Chatbot) features extend Phase II without modification
- Backwards compatibility with Phase II APIs is mandatory
- Never remove or alter existing authentication flows

### 3. Backend Architecture:
- FastAPI for API framework
- SQLModel for database modeling
- PostgreSQL for data persistence
- JWT-based authentication with Better Auth integration
- Pydantic for data validation

### 4. Security & Authentication:
- JWT verification middleware must validate tokens using BETTER_AUTH_SECRET
- Enforce strict multi-tenant isolation on every database query
- Filter all data access by authenticated user_id
- Implement proper rate limiting and security headers

### 5. Database & Data:
- Use SQLModel for all database operations
- Maintain proper indexing for performance
- Implement proper transaction handling
- Follow ACID principles for data consistency

## Default Policies (Backend Specific)

- **Clarify and Plan First:** Understand business requirements separately from technical implementation
- **Do Not Invent:** Use only database schemas and API contracts defined in specs
- **No Hardcoded Secrets:** Use environment variables only
- **Smallest Viable Change:** Minimize diff size while meeting requirements
- **Preserve Existing Functionality:** Never break working features
- **Reference Existing Code:** Use code references when modifying existing components

## Backend-Specific Constraints

### 1. Phase II Foundation Constraints:
- Do not modify existing authentication flow
- Do not change existing API endpoint contracts
- Do not remove or alter existing database models that support core functionality
- Maintain all existing user workflows

### 2. Phase III Extension Constraints:
- AI chatbot features must be optional/opt-in
- Maintain all existing Phase II API contracts
- Preserve all existing database schemas
- Maximum 100ms additional latency for AI-enhanced operations

### 3. Security & Performance Constraints:
- 100% of data access attempts for resources not belonging to the authenticated user must be blocked
- API must respond to 95% of requests in under 200ms
- System must handle at least 50 concurrent requests without error rate exceeding 0.1%
- All API endpoints must return valid JSON responses according to the defined contract

## Code Standards

See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

### Backend Quality Standards:
- All API endpoints must have proper type hints
- All database models must follow SQLModel conventions
- All authentication flows must be secure and validated
- All error responses must be consistent and informative

### Backend Performance Standards:
- API responds to 95% of requests in under 200ms
- Database queries must be optimized with proper indexing
- Connection pooling must be properly configured
- Caching strategies where appropriate

## Spec Alignment Requirements

Before implementing any feature:
1. Locate the relevant spec section in `specs/002-backend-todo-api/spec.md` or Phase III AI agent specs
2. Verify the implementation aligns with the spec requirements
3. Reference the specific requirement number in your implementation
4. Test against the acceptance criteria defined in the spec

## API Endpoint Standards

All API endpoints must follow these patterns:
- `GET /api/{user_id}/tasks` - List tasks with optional status filtering
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status
- `POST /api/{user_id}/chat` - AI chat endpoint (Phase III)

## Database Model Standards

All database models must:
- Follow SQLModel conventions
- Include proper relationships and foreign keys
- Have appropriate indexes for performance
- Include proper validation constraints
- Follow the multi-tenant isolation pattern with user_id filtering

## Architectural Decision Records (ADRs)

When making significant backend architecture decisions, document them as ADRs in `history/adr/`.