# 🎯 FAANG Interview Prep — Master Notes

Comprehensive, first-principles, interview-focused notes across 11 core SDE/Senior-SDE topics.

Each topic follows the same structure:
**Overview → Why it exists → Why FAANG cares → Core concepts → Architecture/diagrams → Real-world examples → Real-life analogy → Memory tricks → Common interview questions → Senior-level discussion → Interview tips → Revision cheat sheet.**

## ⚡ Night-Before Cram
**[CHEATSHEET.md](CHEATSHEET.md)** — one-page all-topics recall (all 11 topics condensed, ~20 min read). Start here the night before.

## 📚 Topics

| # | Topic | File |
|---|-------|------|
| 1 | Concurrency & Multithreading | [01-concurrency-multithreading.md](01-concurrency-multithreading.md) |
| 2 | Operating Systems | [02-operating-systems.md](02-operating-systems.md) |
| 3 | Computer Networks | [03-computer-networks.md](03-computer-networks.md) |
| 4 | Cloud & Infrastructure | [04-cloud-infrastructure.md](04-cloud-infrastructure.md) |
| 5 | System Design | [05-system-design.md](05-system-design.md) |
| 6 | Low-Level Design (LLD) | [06-low-level-design.md](06-low-level-design.md) |
| 7 | Distributed Systems | [07-distributed-systems.md](07-distributed-systems.md) |
| 8 | Databases | [08-databases.md](08-databases.md) |
| 9 | Performance Engineering | [09-performance-engineering.md](09-performance-engineering.md) |
| 10 | Security Fundamentals | [10-security-fundamentals.md](10-security-fundamentals.md) |
| 11 | Behavioral / Leadership / Googleyness | [11-behavioral-leadership.md](11-behavioral-leadership.md) |

## 🔗 How topics connect

```
        OS ◄──────► Concurrency & Multithreading
        │                    │
        ▼                    ▼
   Networks ◄──────► System Design ◄──────► Distributed Systems
        │                    │                      │
        ▼                    ▼                      ▼
  Cloud & Infra ◄──► Performance Eng.        Databases
        │                                          │
        ▼                                          ▼
   Security ◄────────────────────────────► Low-Level Design

  Behavioral / Leadership wraps ALL of the above (how you communicate them).
```

## ⏱️ Suggested revision order (last-week-before-interview)
1. System Design (5) + Distributed Systems (7) — highest signal for senior loops
2. Databases (8) + Concurrency (1) — deep technical follow-ups
3. Networks (3) + OS (2) — fundamentals screens
4. LLD (6) + Cloud (4) + Performance (9) + Security (10)
5. Behavioral (11) — review your STAR stories nightly
