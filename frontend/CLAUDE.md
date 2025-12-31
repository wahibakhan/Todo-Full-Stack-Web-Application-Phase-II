# Frontend Agent Instructions

## Tech Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5.x (strict mode)
- **Styling**: Tailwind CSS 3.x
- **Authentication**: Better Auth with JWT tokens
- **State**: React hooks (no external state management library)

## Key Principles

1. **Server Components by Default**: Use Server Components unless client interactivity is required
2. **Route Groups**: (auth) for public routes, (protected) for authenticated routes
3. **JWT Storage**: Tokens stored in httpOnly cookies (managed by Better Auth)
4. **API Client**: All backend calls go through `lib/api.ts` with credentials: "include"
5. **Type Safety**: All API responses typed in `lib/types.ts`

## Project Structure

```
app/
├── (auth)/           # Public routes (login, signup)
├── (protected)/      # Protected routes (dashboard)
├── layout.tsx        # Root layout with Better Auth provider
├── page.tsx          # Landing page
└── middleware.ts     # Route protection (JWT verification)

components/
├── TaskList.tsx      # Display all tasks
├── TaskItem.tsx      # Single task with actions
├── TaskForm.tsx      # Add/edit task form
├── LogoutButton.tsx  # Logout functionality
└── ui/               # Reusable UI components

lib/
├── api.ts           # API client (attaches JWT automatically)
├── auth.ts          # Better Auth configuration
└── types.ts         # TypeScript type definitions
```

## Environment Variables

Required in `.env.local`:
- `BETTER_AUTH_SECRET`: Shared secret for JWT (MUST match backend)
- `NEXT_PUBLIC_API_URL`: Backend API URL (http://localhost:8000)
- `DATABASE_URL`: Neon PostgreSQL connection (Better Auth needs it)

## Development

```bash
npm run dev        # Start dev server (http://localhost:3000)
npm run build      # Build for production
npm run type-check # TypeScript validation
npm run lint       # ESLint checks
```

## Authentication Flow

1. User signs up/logs in → Backend issues JWT
2. JWT stored in httpOnly cookie by Better Auth
3. Frontend middleware checks cookie on protected routes
4. API client automatically includes cookie in requests
5. Backend verifies JWT and extracts user_id

## Security Rules

- Never access JWT directly (httpOnly prevents this)
- All forms validate inputs before submission
- All user content escaped by Next.js by default
- No `dangerouslySetInnerHTML` usage allowed
- CORS handled by backend (frontend runs on localhost:3000)

## Phase 2 Constraints

- No AI agents or MCP tools in code
- No Docker/Kubernetes references
- No Phase 1 console/CLI code
- Professional, production-ready UI only
