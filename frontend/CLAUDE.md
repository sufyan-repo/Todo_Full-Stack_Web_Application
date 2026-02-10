# Claude Code Rules - Frontend Component

This file governs AI-assisted development for the frontend component of The Evolution of Todo - Phase II & III.

## Task Context

**Your Surface:** You operate on the frontend component level, providing guidance for UI/UX implementation and client-side functionality.

**Your Success is Measured By:**
- All outputs strictly follow the user intent and spec requirements.
- All changes align with existing frontend architecture (Next.js, TypeScript, Tailwind CSS).
- All implementations maintain Phase II foundation integrity while supporting Phase III extensions.
- All changes reference specific spec sections.

## Core Guarantees (Frontend Product Promise)

- **Spec Compliance:** All implementations must follow the frontend specifications in `specs/001-frontend-todo-ui/spec.md` and `specs/003-flagship-ui/spec.md`
- **Phase II Foundation:** Never modify or break existing Phase II functionality
- **Authentication Integration:** Maintain seamless JWT-based authentication flow
- **API Compatibility:** Preserve all existing API integration patterns

## Development Guidelines

### 1. Spec-First Implementation:
- ALWAYS read and reference the frontend specs before making changes
- Derive all implementation details from spec requirements
- Maintain traceability between code and spec requirements

### 2. Phase II Preservation:
- Phase II (Todo Full Stack) remains completely immutable in terms of core functionality
- All Phase III (AI Chatbot) features extend Phase II without modification
- Backwards compatibility with Phase II APIs and UI is mandatory
- Never remove or alter existing authentication flows

### 3. Frontend Architecture:
- Next.js 16+ with App Router
- TypeScript for all components
- Tailwind CSS for styling
- Framer Motion for animations
- SWR for data fetching
- React Hook Form with Zod validation

### 4. Authentication & Security:
- JWT tokens must be included automatically in all API requests
- Unauthenticated users must be redirected to sign-in page
- Token expiration must trigger appropriate UX flows
- Never store sensitive data in client-side storage

### 5. API Integration:
- Follow existing API client patterns
- Maintain consistent error handling
- Preserve optimistic update patterns
- Respect API rate limits and error responses

## Default Policies (Frontend Specific)

- **Clarify and Plan First:** Understand business requirements separately from technical implementation
- **Do Not Invent:** Use only APIs and contracts defined in specs
- **No Hardcoded Secrets:** Use environment variables only
- **Smallest Viable Change:** Minimize diff size while meeting requirements
- **Preserve Existing Functionality:** Never break working features
- **Reference Existing Code:** Use code references when modifying existing components

## Frontend-Specific Constraints

### 1. Phase II Foundation Constraints:
- Do not modify existing authentication flow
- Do not change existing API integration patterns
- Do not remove or alter existing UI components that support core functionality
- Maintain all existing user workflows

### 2. Phase III Extension Constraints:
- AI chatbot features must be optional/opt-in
- Maintain all existing Phase II user workflows
- Preserve all existing API contracts
- Maximum 100ms additional latency for AI-enhanced operations

### 3. UI/UX Constraints:
- Maintain all visual design requirements from flagship UI spec
- Preserve responsive behavior across all device sizes
- Maintain all accessibility requirements
- Follow all animation and interaction guidelines

## Code Standards

See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

### Frontend Quality Standards:
- All components must be TypeScript-compliant
- All UI must follow accessibility standards (WCAG 2.1 AA)
- All animations must respect user's reduced motion preferences
- All responsive breakpoints must be preserved (320px to 1920px)

### Frontend Performance Standards:
- Page load time under 2 seconds
- Animation frames at 60fps
- Efficient data fetching with SWR
- Proper loading and error states

## Spec Alignment Requirements

Before implementing any feature:
1. Locate the relevant spec section in `specs/001-frontend-todo-ui/spec.md` or `specs/003-flagship-ui/spec.md`
2. Verify the implementation aligns with the spec requirements
3. Reference the specific requirement number in your implementation
4. Test against the acceptance criteria defined in the spec

## Error Handling Standards

- All API errors must trigger appropriate user feedback
- Authentication errors must redirect to sign-in
- Network errors must display helpful retry options
- Form validation errors must be clear and actionable

## Architectural Decision Records (ADRs)

When making significant frontend architecture decisions, document them as ADRs in `history/adr/`.