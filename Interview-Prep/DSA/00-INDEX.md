# 💻 DSA / Coding-Round Pack

The coding interview is the #1 filter at FAANG. These three files cover **pattern recognition**, **data structures**, and **algorithms** — everything you need to recognize and solve LeetCode-style problems fast.

| File | What's inside |
|------|---------------|
| [01-patterns-and-templates.md](01-patterns-and-templates.md) | **Start here.** 22 coding patterns with "when you see X → use Y" triggers + copy-pasteable Python templates. The pattern-recognition cheat table is the core. |
| [02-data-structures.md](02-data-structures.md) | Every DS from first principles: internals, ASCII diagrams, operation-complexity tables, when-to-use, language container mapping. |
| [03-algorithms-and-complexity.md](03-algorithms-and-complexity.md) | Big-O & Master Theorem, sorting/searching, all graph algorithms, DP families, greedy, backtracking, bit tricks, number theory. |

## How to use
1. **Learn the patterns** (file 01) — recognition is 80% of the battle.
2. **Drill the complexity tables** (files 02 + 03) — interviewers always ask "what's the time complexity?"
3. **Map every LeetCode problem you do back to a pattern** in file 01's cheat table.

## The universal coding-interview loop
```
Clarify → Examples/edge cases → Brute force (state complexity)
   → Optimize (pick a pattern) → Code cleanly → Test/dry-run → State final complexity
```

> **Acceptable complexity vs N** (memorize): N≤20 → 2^N/N! ok · N≤500 → O(N³) · N≤5000 → O(N²) · N≤10⁶ → O(N log N) · N>10⁷ → O(N) or O(log N).
