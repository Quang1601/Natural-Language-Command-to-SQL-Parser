# Natural Language to SQL Parser

A modern web application that converts natural language queries into SQL statements. Built with Next.js, React, and Tailwind CSS.

## 🎯 Project Overview

**Purpose:** Enable users to generate SQL queries by typing natural language questions, making database querying accessible without SQL knowledge.

**Status:** Frontend ✅ | Dummy Backend 🟡 | Real Backend 🔄

## 🛠️ Tech Stack

- **Frontend:** Next.js 13+ (App Router)
- **Styling:** Tailwind CSS with custom animations
- **State Management:** React Hooks (useState, useEffect, useRef)
- **Type Safety:** TypeScript
- **Fonts:** Inter + Inria Sans (via Next.js Google Fonts)
- **Architecture:** Modular components + Service layer pattern

## 📁 Project Structure

```
src/app/
├── page.tsx                 # Main Home component (~100 lines)
├── components/
│   ├── Chat.tsx            # ChatConversation + ChatInputArea
│   ├── Magnifier.tsx       # Animation components
│   ├── StartButton.tsx     # Interactive button
│   ├── Icons.tsx           # 9 SVG icon definitions
│   └── LoadingStyles.tsx   # CSS animations
└── services/
    └── sqlParser.ts        # Dummy SQL generator (800ms delay)

DEVELOPMENT_GUIDE.tex       # Detailed development documentation
```

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation

```bash
# Clone repository
git clone <repository-url>
cd Natural-Language-Command-to-SQL-Parser

# Install dependencies
npm install
# or
yarn install
```

### Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## 💬 Usage

### Sample Queries

**✅ Returns SQL:**
- "Find users older than 50 who use YouTube more than 15 hours daily"
- "Show users by age and income"
- "Find users in New York under 40 years old"
- "Count purchases per user"
- "Calculate average spending"

**❌ Requests Details:**
- "hi" (too short)
- "what is sql" (no relevant keywords)
- "hello there" (no context)

### Features

- 🎨 **Beautiful Chat UI** - Messenger-style message bubbles with auto-wrapping
- ⚡ **Auto-scroll** - Smart scrolling (only when user near bottom)
- 📝 **Multi-line Input** - Auto-growing textarea with Shift+Enter for new lines
- 🔄 **Loading Indicator** - Smooth loading animation inside message box
- 📱 **Responsive Design** - Works on desktop and mobile
- 🎯 **Smart Keyword Matching** - Semantic understanding of query intent
- ✨ **Smooth Animations** - Magnifier animation, fade effects

## 🔧 Key Components

### ChatConversation
Displays message history with:
- User messages (white bubble, top-left corner)
- Bot messages (white bubble, top-right corner)
- SQL code blocks with syntax highlighting
- Loading indicator (animated spinner)
- Smart auto-scroll behavior

### ChatInputArea
Multi-line input with:
- Auto-growing textarea
- Add/Mic/Send button states
- Focus styling with glow effect
- Enter to send, Shift+Enter for new line

### sqlParser Service
Dummy backend replacement with:
- 8 SQL query templates
- Keyword-based query generation
- 800ms simulated network delay
- Input validation (min 3 chars + relevant keywords)

## 📋 Development Timeline

### Phase 1: SOLID Refactoring ✅
- Separated 465-line monolith into 5 modular components
- Improved code maintainability and scalability

### Phase 2: Dummy Data Implementation ✅
- Created SQL parser service for frontend testing
- Smart keyword matching with semantic aliases
- Proper error handling for vague queries

### Phase 3: UI/UX Improvements ✅
- Fixed loading state propagation
- Implemented hidden scrollbar with smart auto-scroll
- Multi-line textarea with auto-grow
- Unified message box styling
- Enhanced keyword matching with aliases

##  Next Steps

1. **Replace Dummy Backend**
   - Create `/api/parse-nl-to-sql` endpoint
   - Implement actual NL-to-SQL parsing logic
   - Update `sqlParser.ts` to call real API

2. **Add File Upload**
   - Allow users to upload SQL schemas
   - Parse database structure for smarter queries

3. **User Authentication**
   - Add login/signup functionality
   - Store query history per user

4. **Query Execution**
   - Add database connection management
   - Execute generated SQL and return results

5. **Advanced Features**
   - Query history and favorites
   - Query explanation and optimization
   - Multi-language support

## 🎓 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Hooks API](https://react.dev/reference/react/hooks)

## 📝 License

This project is open source.

## 👤 Author

Development Session: December 12, 2025

---

**Happy Coding!** 🚀
