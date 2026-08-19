# RESOLVIO

A modern customer support platform that manages support tickets with real-time chat, AI-powered assistance, and a dedicated agent dashboard.

**Live App:** [resolvio.dev](https://resolvio.dev)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Database Schema](#database-schema)

---

## Overview

**RESOLVIO** is a complete customer support solution that connects customers with support agents through an intuitive interface. Customers submit issues via an embeddable chat widget, agents respond through a real-time dashboard, and AI-powered features help generate contextual responses using a company knowledge base.

**Key Components:**
1. **Embeddable Widget** – Chat interface for customer websites
2. **Agent Dashboard** – Real-time ticket management interface
3. **AI Engine** – Knowledge base integration with vector embeddings
4. **Real-time Messaging** – WebSocket-powered live updates

---

## Core Features

### Customer Experience

- **Chat Widget** – Lightweight, embeddable chat widget for any website
- **Ticket Creation** – Customers submit support requests with subject, category, and priority
- **Conversation History** – All messages persist in localStorage, resumable after page reload
- **Real-time Updates** – See agent responses instantly without refreshing
- **Multiple Categories** – Billing, Technical, General issue classification

### Agent Dashboard

- **Ticket List** – View all incoming tickets with status at a glance
- **Ticket Details** – Open any ticket to see full conversation history
- **Live Replies** – Send responses that appear instantly to customers
- **Ticket Management** – Update status (open/resolved), priority (low/medium/high), and category
- **Role-Based Access** – Owner and Agent roles with appropriate permissions
- **Search & Filter** – Find tickets by customer, subject, or content

### AI-Powered Features

- **Knowledge Base Management** – Create and organize company-specific documentation
- **Vector Embeddings** – Semantic search using pgvector for intelligent retrieval
- **AI Responses** – Generate contextual answers using Google Generative AI
- **Document Indexing** – Automatic chunking and embedding of knowledge base articles

### Multi-Tenancy & Security

- **Company Isolation** – Each company has separate tickets and knowledge base
- **API Key Authentication** – Secure widget integration via company-specific API keys
- **Token-Based Auth** – DRF token authentication for agent dashboard
- **User Management** – Email-based login with role-based access control

---

## How It Works

### Customer Flow

1. **Widget Load** – Customer's website loads the resolvio widget script
2. **Submit Ticket** – Customer enters name, email, issue details, category, and priority
3. **Ticket Created** – Backend automatically creates a Ticket and first Message
4. **Chat Continues** – Customer can add more messages to the same conversation
5. **Agent Replies** – Agent responds through dashboard
6. **Real-time Notification** – Customer sees reply instantly via WebSocket
7. **Close Ticket** – Agent marks ticket as resolved

### Agent Flow

1. **Login** – Agent logs into dashboard with email credentials
2. **View Tickets** – See list of all open tickets sorted by priority
3. **Open Ticket** – Click to view customer messages and conversation history
4. **Compose Reply** – Type response and send to customer
5. **Update Status** – Mark ticket as resolved or reopen if needed
6. **Manage Knowledge Base** – Add articles for AI assistance
7. **Logout** – Session ends

### Real-Time Communication

- **WebSocket Connection** – Dashboard and widget maintain persistent WebSocket connections
- **Message Sync** – New messages broadcast to all connected clients
- **Typing Indicators** – Optional real-time typing status
- **Connection Fallback** – Graceful degradation if WebSocket unavailable

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18 + Vite + React Router + Tailwind CSS |
| **Backend** | Django 5.2 + Django REST Framework + Django Channels |
| **Database** | PostgreSQL 16 + pgvector (vector embeddings) |
| **Real-time** | Django Channels + Redis + Daphne (ASGI) |
| **AI** | Google Generative AI API (Gemini) |
| **Infrastructure** | Docker + Vercel (frontend) + EC2 (backend) |

---

## Architecture

### Frontend Architecture

```
Widget Entry Point (widget.js)
├── ChatWidget Component
│   ├── Message Display
│   ├── Input Form
│   └── WebSocket Connection
│
Main App (main.jsx)
├── Login / Signup Pages
├── Agent Dashboard
│   ├── TicketsPage (list view)
│   └── TicketDetail (conversation view)
└── KnowledgeBasePage (admin panel)
```

### Backend Architecture

```
Django Project (core)
├── Settings & Configuration
├── URL Routing
└── ASGI/WSGI Configuration

Main App (app)
├── Models
│   ├── User (email-based)
│   ├── Company
│   ├── Ticket
│   ├── Message
│   └── KnowledgeBase
├── Views & Serializers (API endpoints)
├── Consumers (WebSocket handlers)
├── Services (business logic)
└── AI Module
    ├── Gemini Integration
    ├── Embeddings & Indexing
    ├── Chunking
    └── Answer Generation
```

### Data Flow

```
Customer Widget
    ↓ (HTTPS)
API Gateway → Django REST API
    ↓
[Models] ← PostgreSQL
    ↓
WebSocket → Channels Layer ← Redis
    ↓
Agent Dashboard (React)

Knowledge Base → AI Module → Google Gemini
    ↓
Vector Embeddings → pgvector Search
    ↓
Context for AI Responses
```

## Project Structure

```
resolvio/
├── backend/                          # Django REST API backend
│   ├── core/                         # Django project configuration
│   │   ├── settings.py               # Database, apps, middleware config
│   │   ├── asgi.py                   # ASGI for WebSockets
│   │   ├── wsgi.py                   # WSGI for traditional HTTP
│   │   └── urls.py                   # Root URL routing
│   │
│   ├── app/                          # Main application
│   │   ├── models.py                 # Database models (User, Ticket, Message, etc.)
│   │   ├── views.py                  # API ViewSets
│   │   ├── serializers.py            # Request/response serialization
│   │   ├── urls.py                   # API endpoint routing
│   │   ├── services.py               # Business logic
│   │   ├── consumers.py              # WebSocket message handlers
│   │   ├── routing.py                # WebSocket URL routing
│   │   ├── middleware.py             # Custom middleware (CORS, etc.)
│   │   │
│   │   └── ai/                       # AI/ML module
│   │       ├── base.py               # Abstract base classes
│   │       ├── factory.py            # AI provider factory pattern
│   │       ├── gemini.py             # Google Generative AI client
│   │       ├── indexing.py           # Vector indexing engine
│   │       ├── chunking.py           # Document chunking algorithm
│   │       └── answering.py          # Answer generation logic
│   │
│   └── migrations/                   # Database schema versions
│
├── frontend/                         # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx                   # Main dashboard app
│   │   ├── widget.js                 # Embeddable widget entry point
│   │   │
│   │   ├── api/                      # API client functions
│   │   │   ├── tickets.js            # Ticket CRUD operations
│   │   │   └── knowledgeBase.js      # Knowledge base operations
│   │   │
│   │   ├── components/
│   │   │   ├── ChatWidget.jsx        # Main chat widget component
│   │   │   ├── Login.jsx             # Agent login form
│   │   │   ├── Signup.jsx            # Agent registration form
│   │   │   ├── auth/                 # Authentication wrappers
│   │   │   ├── tickets/              # Ticket UI components
│   │   │   │   ├── TicketDetail.jsx  # Conversation view
│   │   │   │   └── StatusBadge.jsx   # Status display
│   │   │   └── shared/               # Reusable UI elements
│   │   │
│   │   ├── hooks/
│   │   │   └── useWebSocket.js       # WebSocket connection hook
│   │   │
│   │   ├── pages/
│   │   │   ├── TicketsPage.jsx       # Dashboard ticket list
│   │   │   ├── KnowledgeBasePage.jsx # KB management
│   │   │   └── WidgetSetupPage.jsx   # Widget embed guide
│   │   │
│   │   └── widget/                   # Standalone widget bundle
│   │       ├── index.jsx
│   │       └── widget.css
│   │
│   ├── vite.config.js                # Main app build config
│   └── widget.vite.config.js         # Separate widget build config
│
└── docker-compose.yml                # Local development orchestration
```

---

## Key Features Deep Dive

### Real-Time Messaging

- **WebSocket Protocol:** Persistent bidirectional connection between widget/dashboard and server
- **Redis Channel Layer:** Enables multi-process message broadcasting (horizontal scaling)
- **Automatic Reconnection:** Client-side fallback to polling if connection drops
- **Message Ordering:** Guaranteed delivery order via timestamp-based sequencing

### Multi-Tenancy

- **Company Isolation:** Every query filtered by `company_id`
- **API Key Auth:** Widget includes company API key; server validates before creating tickets
- **Data Privacy:** One company cannot query another company's tickets or knowledge base
- **Namespace Isolation:** Each company has separate WebSocket namespace

### AI Answer Generation

1. **Knowledge Base Indexing:**
   - User uploads KB article
   - System chunks article into 500-token segments
   - Each chunk embedded using Gemini embedding model
   - Vectors stored in pgvector for semantic search

2. **Query Processing:**
   - Customer message embedded using same model
   - Vector similarity search finds top-k relevant KB chunks
   - Chunks passed as context to Gemini model
   - Model generates contextual response

3. **Response Integration:**
   - Optional: Send AI response to agent for review
   - Optional: Send directly to customer
   - Agent can edit before sending

### Widget Integration

- **Script Tag Embed:** Single `<script>` tag loads widget
- **Company Isolation:** API key ensures widget only sends to correct company
- **localStorage State:** Conversation persists across page reloads
- **Responsive Design:** Mobile and desktop optimized
- **Customizable Styling:** Company branding support

---

## Workflow Examples

### Customer Support Flow

```
1. Customer visits example.com
2. Widget loads from resolvio.dev CDN
3. Customer types issue and clicks "Send"
4. Widget validates form, embeds company API key
5. POST /api/tickets/ creates ticket in database
6. Agent sees new ticket in dashboard
7. Agent opens ticket, sees customer messages
8. Agent types reply in dashboard
9. WebSocket broadcasts message to widget
10. Customer sees reply in real-time
11. Conversation continues...
12. Agent marks ticket "resolved"
13. Widget shows "Resolved" badge
```

### Knowledge Base to Answer Flow

```
1. Admin uploads "Password Reset Guide" to KB
2. System chunks and embeds the document
3. Customer asks: "How do I reset my password?"
4. Message embedded and searched against KB vectors
5. Top chunks retrieved and passed to Gemini
6. Gemini generates answer with KB context
7. Agent reviews and sends to customer
```

---

## Contributing

Report issues, request features, or submit PRs on GitHub.

---

**Live:** [resolvio.dev](https://resolvio.dev)
