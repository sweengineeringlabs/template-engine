# Documentation Guide

**Audience**: All team members (writers, developers, reviewers)

---

## WHAT: User Guide vs Developer Guide

This guide explains the two types of documentation we write and when to use each.

### The Simple Rule

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   WHO is reading?                                                   │
│                                                                     │
│   ├── "I want to USE this feature"      → User Guide               │
│   │                                                                 │
│   └── "I want to CHANGE this feature"   → Developer Guide          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Side-by-Side Comparison

| Aspect | User Guide | Developer Guide |
|--------|------------|-----------------|
| **Audience** | People who USE the software | People who BUILD the software |
| **Goal** | "How do I do X?" | "How does X work internally?" |
| **Assumes** | Basic programming knowledge | Deep codebase knowledge |
| **Shows** | Syntax, examples, best practices | Architecture, code flow, internals |
| **Answers** | "What can I do?" | "How is it implemented?" |

### Real Example: Component Props

| User Guide Says | Developer Guide Says |
|-----------------|----------------------|
| "Use `name?: Type` to make a prop optional" | "`parse_prop_def()` checks for `Token::Question` and wraps type in `Option<T>`" |
| "Optional props default to `None`" | "`is_option_type()` returns true if first path segment is `Option`" |
| "This is similar to TypeScript" | "AST `PropDef` has `is_optional: bool` field set during parsing" |

---

## WHY: Why We Need Both

### Problem: One Document Can't Serve Everyone

```
❌ WRONG: Single document for everyone

   User reads:                          Developer reads:
   "parse_prop_def() checks            "To make a prop optional,
    Token::Question and wraps           just add ? after the name"
    the AST type in Option<T>"
           │                                    │
           ▼                                    ▼
   "What? I just want to                "I know that already!
    make a prop optional!"               How do I fix the parser bug?"
```

### Solution: Two Documents, Two Audiences

```
✅ RIGHT: Separate documents

   User reads USER GUIDE:              Developer reads DEVELOPER GUIDE:
   "To make a prop optional,           "parse_prop_def() in components.rs
    add ? after the name:               handles the ? token at line 116:

    size?: Size                         let is_optional = self.eat(&Token::Question)

    This defaults to None"              The type is then wrapped in Option<T>"
           │                                    │
           ▼                                    ▼
   "Perfect! I'll use that"            "Got it! I'll fix that line"
```

### The Audience Test

Ask yourself:

| If reader wants to... | They need... |
|-----------------------|--------------|
| Write a component with optional props | User Guide |
| Fix a bug in prop parsing | Developer Guide |
| Learn prop syntax | User Guide |
| Add a new prop attribute | Developer Guide |
| Migrate from another framework | User Guide |
| Understand the AST structure | Developer Guide |

---

## HOW: Writing Each Type

### User Guide Structure

```markdown
# [Feature] User Guide

## Overview
Brief description of what users can do.

## Quick Start
Copy-paste example that works immediately.

## Syntax Options
All the ways to use this feature.

## When to Use Each
Decision guide / flowchart.

## Examples
Real-world use cases with code.

## Common Mistakes
What NOT to do.

## FAQ
Frequently asked questions.
```

**Key Principles:**
- Start with working code
- Show, don't explain internals
- Use familiar comparisons (TypeScript, Python)
- Focus on "what can I do?"

### Developer Guide Structure

```markdown
# [Feature] Developer Guide

## Architecture Overview
Where this fits in the codebase.

## Key Files
Which files to look at.

## Data Flow
How data moves through the system.

## Implementation Details
Code walkthrough with line numbers.

## Adding New Features
Step-by-step modification guide.

## Testing
How to test changes.

## Common Pitfalls
Bugs to avoid when changing code.
```

**Key Principles:**
- Reference specific files and line numbers
- Show internal data structures
- Explain WHY decisions were made
- Include debugging tips

---

## HOW: Identifying Your Audience

### The 3-Question Test

Before writing, ask:

```
1. Will they have the source code open?

   YES → Developer Guide
   NO  → User Guide

2. Do they need to understand the implementation?

   YES → Developer Guide
   NO  → User Guide

3. Are they trying to change the behavior?

   YES → Developer Guide
   NO  → User Guide
```

### Audience Personas

#### User Guide Reader: "Alex the App Developer"
- Building an app WITH RustScript
- Doesn't care how the compiler works
- Wants working examples
- Compares to TypeScript/React
- Asks: "How do I make this optional?"

#### Developer Guide Reader: "Sam the Compiler Contributor"
- Contributing TO RustScript
- Needs to understand internals
- Wants code references
- Reads AST/HIR definitions
- Asks: "Where does the `?` get transformed to `Option<T>`?"

---

## HOW: Documentation Checklist

### Before Writing

- [ ] Identified the audience (User or Developer)
- [ ] Chose the correct template
- [ ] Listed what the reader wants to accomplish

### User Guide Checklist

- [ ] Has working code example in first 30 seconds of reading
- [ ] No references to internal file paths or line numbers
- [ ] Compares to familiar languages/frameworks
- [ ] Includes "when to use" decision guide
- [ ] Has copy-paste examples
- [ ] Covers common mistakes

### Developer Guide Checklist

- [ ] Lists all relevant source files
- [ ] Includes line number references
- [ ] Shows data structure definitions
- [ ] Explains the "why" behind decisions
- [ ] Has "how to modify" section
- [ ] Includes testing instructions
- [ ] Documents common pitfalls

---

## Summary

| Question | Answer |
|----------|--------|
| What is a User Guide? | Documentation for people who USE the software |
| What is a Developer Guide? | Documentation for people who BUILD/MODIFY the software |
| How do I choose? | Ask: "Does the reader need the source code?" |
| Where do they live? | `docs/guides/` (User) and `docs/dev/` (Developer) |

### Quick Reference

```
docs/
├── guides/                    # User Guides
│   ├── component-props-user-guide.md
│   ├── routing-user-guide.md
│   └── styling-user-guide.md
│
└── dev/                       # Developer Guides
    ├── component-props-developer-guide.md
    ├── parser-internals.md
    └── hir-lowering.md
```

### The Golden Rule

> **User Guide**: "Here's how to USE it"
>
> **Developer Guide**: "Here's how it WORKS"

---

## Related Documents

- [Component Props User Guide](guides/component-props-user-guide.md)
- [Component Props Developer Guide](dev/component-props-developer-guide.md)
- [Template Engine](~/template-engine/README.md) - Documentation templates
