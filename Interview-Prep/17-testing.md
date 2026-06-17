# Testing & Code Quality

> **How to use this file:** Read top-to-bottom for deep understanding of how to build, structure, and reason about test suites. Jump to §Common Interview Questions + §Revision Cheat Sheet for last-minute revision. *How* you test is a direct code-quality signal in coding rounds and a constant on the job — interviewers read your tests as carefully as your implementation.

---

## Table of Contents

- [Overview — What It Is](#overview--what-it-is)
- [Why It Exists](#why-it-exists)
- [Why FAANG Cares](#why-faang-cares)
- [Core Concepts](#core-concepts)
- [The Test Pyramid](#the-test-pyramid)
- [Unit Testing & Test Doubles](#unit-testing--test-doubles)
- [TDD & BDD](#tdd--bdd)
- [Integration & Contract Testing](#integration--contract-testing)
- [End-to-End Testing](#end-to-end-testing)
- [Advanced Techniques](#advanced-techniques)
- [Testing Hard Things (async, concurrency, time, legacy)](#testing-hard-things-async-concurrency-time-legacy)
- [Code Quality & CI](#code-quality--ci)
- [Architecture / Diagrams](#architecture--diagrams)
- [Real-World Examples](#real-world-examples)
- [Real-Life Analogies](#real-life-analogies)
- [Memory Tricks / Mnemonics](#memory-tricks--mnemonics)
- [Common Interview Questions](#common-interview-questions)
- [Senior-Level Discussion Points](#senior-level-discussion-points)
- [Typical Mistakes Candidates Make](#typical-mistakes-candidates-make)
- [How This Connects to Other Topics](#how-this-connects-to-other-topics)
- [FAANG Interview Tips](#faang-interview-tips)
- [Revision Cheat Sheet](#revision-cheat-sheet)

---

## Overview — What It Is

**Testing** is the disciplined practice of executing code with known inputs and asserting that the observed behavior matches the expected behavior. **Code quality** is the broader engineering hygiene — static analysis, type checking, linting, code review, and CI — that keeps a codebase changeable over years.

Testing is fundamentally about **confidence under change**. A test suite is not a quality stamp you apply once; it is a *safety net* that lets you refactor, add features, and upgrade dependencies without fear. The real question a test answers is not "does this code work?" but "if I change this code six months from now, will I find out before my users do?"

The discipline spans several layers:

- **Unit tests** — verify a single function/class in isolation, microsecond-to-millisecond fast.
- **Integration tests** — verify that two or more components collaborate correctly (your code + a real database, a real message broker).
- **Contract tests** — verify that two services agree on their API shape *without* spinning up both.
- **End-to-end (E2E) tests** — drive the whole system as a user would, through the UI or public API.
- **Property-based / mutation / fuzz / load / chaos** — advanced techniques that attack the suite's blind spots.

And the surrounding code-quality machinery:

- **Coverage** — what fraction of code your tests execute (a floor, not a goal).
- **Static analysis & linters** — find bugs and style violations *without running* the code.
- **Type checking** — catch whole categories of errors at compile/check time.
- **CI pipelines** — run all of the above automatically on every change, fail fast.
- **Code review** — a human safety net for design, intent, and readability.

The central discipline mirrors performance engineering: **understand the behavior you want, encode it as an executable expectation, run it continuously.** A test you do not run is documentation that rots. A test you cannot trust is worse than no test at all.

---

## Why It Exists

Software is the only engineering discipline where the cost of a change is theoretically zero (just edit text) but the *risk* of a change is enormous. Without tests:

- A one-line change to a date-formatting helper silently breaks invoice generation in three other modules (**no regression net**).
- Nobody dares touch the 4,000-line `OrderService` because "it works and we don't know why" (**fear of change → ossification**).
- A bug shipped to production is found by a customer, escalated, hot-fixed at 2 a.m., and costs 100× what it would have cost to catch in a unit test (**late detection**).
- A refactor that should take an afternoon takes two weeks of manual clicking through the app to make sure nothing broke (**no automated verification**).

Tests exist to convert *implicit, tribal, fragile* knowledge ("this is how the discount engine is supposed to behave") into *explicit, executable, permanent* specifications. They produce code that is:

| Goal | What Tests Give You |
|---|---|
| **Changeable** | Refactor freely; the suite tells you the moment behavior drifts. |
| **Documented** | A well-named test is the most accurate documentation that exists — it cannot lie, because CI runs it. |
| **Designable** | Hard-to-test code is almost always badly-designed code; the pain of testing is a design smell detector. |
| **Debuggable** | A failing test localizes a bug to a few lines; a production incident localizes it to "somewhere in the system." |
| **Shippable** | Continuous deployment is *only* possible with a trustworthy automated suite. |

### The cost-of-a-bug-by-stage curve

The single most important economic fact about testing: **the cost of fixing a defect grows roughly an order of magnitude per stage it escapes.** The numbers below are the canonical figures cited from IBM Systems Sciences Institute / NIST-style studies — interviewers expect you to know the *shape* and the *order of magnitude*, not exact constants.

```
Cost to fix a single bug (relative units)

Production  |                                         ##########  ~100×
            |
QA / E2E    |                          ######  ~15×
            |
Integration |                  ####  ~6×
            |
Code review |            ##  ~3×
            |
Unit test   |       #  ~1.5×
            |
Design/type |   .  ~1×  (caught before code even runs)
            +----------------------------------------------------
              cheapest                                  most expensive
```

The lesson is not "test more." It is **"shift left"** — push detection as early (leftward) as possible. A type checker catches the bug before the code runs; a unit test catches it in milliseconds on your laptop; a production incident catches it after it has cost revenue, on-call sleep, and customer trust.

**Interview takeaway: The justification for testing is economic, not moral. Every stage a bug survives multiplies its cost ~10×. Tests are a leverage instrument for shifting detection left.**

---

## Why FAANG Cares

| Company | Evidence | Lesson |
|---------|----------|--------|
| **Google** | Authored *Software Engineering at Google* (the "test certified" program, the test pyramid, the "Beyoncé Rule" — *if you liked it you shoulda put a test on it*). Code cannot merge without tests. The monorepo runs millions of tests per commit via the Blaze/Bazel build graph. | Tests are the entry fee for changing shared code. |
| **Amazon** | "Operational excellence" LP. Every service owns its tests; deployment pipelines (CodePipeline) gate on automated test stages. Bar raisers probe whether you'd write tests for the code you just wrote in the interview. | If it's not tested, it's not done. |
| **Meta** | Built **Sapienz** (automated test-input generation) and **Infer** (static analysis for null/leak bugs) and runs them on every diff in Phabricator. Continuous deployment of web at scale demands automated confidence. | Static analysis + tests enable "move fast" *without* breaking things. |
| **Netflix** | Invented **Chaos Engineering** (Chaos Monkey, the Simian Army). They test resilience in *production* by injecting failure. | Testing isn't just correctness; it's verifying behavior under failure. |
| **Microsoft** | Strong TDD/unit-test culture; the .NET and TypeScript ecosystems were built with testability as a first-class concern. | Type systems + tests are complementary, not competing. |

**FAANG interview reality:** In a coding round, after you write a solution, expect *"how would you test this?"* A senior candidate doesn't say "I'd write some tests" — they enumerate equivalence classes, boundary conditions, the empty/null/overflow cases, and explain which deserve a unit test vs. an integration test. In system design, when you propose a microservice split, the follow-up is often *"how do you stop service A's deploy from breaking service B?"* — the expected answer involves **contract testing**. Testing knowledge is a *seniority signal*: juniors test happy paths; seniors test the boundaries, the failures, and the contracts.

---

## Core Concepts

### Verification vs. Validation

Two words interviewers use interchangeably but that mean different things:

- **Verification** — "Are we building the product *right*?" Does the code meet its spec? (Unit/integration tests answer this.)
- **Validation** — "Are we building the *right* product?" Does the spec meet the user's actual need? (Acceptance/E2E/user testing answer this.)

A function can be perfectly verified (passes every unit test) and completely invalid (computes the wrong thing because the requirement was misunderstood). This is why E2E and acceptance tests, written in the language of the business, matter even when unit coverage is high.

### The four properties every test asserts about

Every test, regardless of level, is checking one of these:

1. **Correctness** — right output for given input.
2. **Behavior on the boundaries** — empty, null, zero, max-int, off-by-one.
3. **Error handling** — does it fail the way it's supposed to (throw, return error, retry)?
4. **Side effects / interactions** — did it write the row, send the message, call the gateway exactly once?

### System Under Test (SUT) and Collaborators

```
            +-------------------------------------------+
            |              TEST                          |
            |                                            |
            |   Arrange: build inputs & doubles          |
            |   Act:     call the SUT                    |
            |   Assert:  check output / interactions     |
            +--------------------+----------------------+
                                 |
                                 v
        +------------------------------------------------+
        |          System Under Test (SUT)               |
        |   the one unit of behavior you are testing     |
        +-----+----------------+-----------------+-------+
              |                |                 |
              v                v                 v
        +-----------+   +-------------+   +------------+
        |Collaborator|  |Collaborator |   |Collaborator|
        |  (real)   |   |  (DOUBLE)   |   |  (real)    |
        +-----------+   +-------------+   +------------+

   A "test double" replaces a real collaborator to make the test
   fast, deterministic, and focused on the SUT.
```

The key vocabulary: the **SUT** is the thing you're testing; its **collaborators** are everything it talks to. The art of unit testing is deciding which collaborators to use *for real* and which to replace with **test doubles**.

### Determinism: the non-negotiable

A test must produce the same result every time it runs, anywhere, in any order. The four enemies of determinism — memorize these, they are the root cause of nearly every flaky test:

```
   T - Time      (wall clock, timezones, "now()")
   O - Order     (test A leaves state that test B depends on)
   R - Random    (unseeded RNG, UUIDs, hash iteration order)
   N - Network/  (real HTTP, DNS, shared DB, message brokers,
       Concurrency thread scheduling / races)
```

(Mnemonic: **TORN** — a test that depends on Time, Order, Random, or Network/concurrency will eventually be *torn* apart by flakiness.)

**Interview takeaway: A non-deterministic test is a liability. It trains the team to ignore red builds ("just re-run it"), which destroys the entire value of the suite. Fixing flakiness is a first-class engineering task, not a nuisance.**

---

## The Test Pyramid

The **Test Pyramid** (Mike Cohn, 2009) is the canonical model for *how many* of each kind of test to write. It is a shape, a cost model, and an anti-pattern detector all at once.

```
                       /\
                      /  \         E2E / UI tests
                     / E2E\        - few (5-10%)
                    /------\       - slow (seconds-minutes)
                   /        \      - flaky, expensive
                  / Integr.  \     Integration tests
                 /------------\    - some (15-30%)
                /              \   - medium speed (10ms-1s)
               /     Unit       \  Unit tests
              /------------------\ - many (60-80%)
             /____________________\- fast (<10ms), cheap, stable

    As you go UP:  slower, more brittle, more realistic, fewer
    As you go DOWN: faster, more stable, less realistic, more
```

### Why a pyramid and not a rectangle?

The proportions follow directly from a cost/value trade-off:

| Layer | Speed | Stability | Realism | Cost to write & maintain | Target % |
|---|---|---|---|---|---|
| **Unit** | µs–ms | Very high | Low (isolated) | Low | 60–80% |
| **Integration** | 10ms–1s | Medium | Medium-high | Medium | 15–30% |
| **E2E** | seconds–minutes | Low (flaky) | Highest | High | 5–10% |

You want **many cheap, fast, stable tests** at the bottom that pinpoint *exactly* which function broke, and **few expensive, slow, realistic tests** at the top that verify the whole thing hangs together. A unit test failure says "function `applyDiscount` is wrong." An E2E failure says "checkout is broken somewhere" — you still have to debug.

### What each layer actually catches

```
Unit:        logic bugs, off-by-one, bad conditionals, wrong formula
Integration: serialization mismatches, SQL/schema errors, wrong API
             usage, transaction boundary bugs, config wiring
E2E:         broken user journeys, routing, auth flows, the "all the
             pieces are individually fine but together they don't work"
```

A bug in your discount *formula* is best caught by a unit test (fast, precise). A bug where your ORM generates the wrong SQL is invisible to unit tests (you mocked the DB) — only an integration test against a *real* database catches it. A bug where the login button's POST goes to the wrong route is invisible to both — only E2E catches it.

### Anti-pattern: the Ice-Cream Cone

The most common pathology in real codebases is the **inverted pyramid**, a.k.a. the **Ice-Cream Cone**:

```
             ____________________
            \    Manual QA       /   <- huge, all clicking by hand
             \__________________/
              \    E2E / UI     /     <- many, slow, flaky
               \______________/
                \  Integration /      <- some
                 \____________/
                  \   Unit    /        <- few, neglected
                   \________/
                    \______/
                       \/   <- "automation" as an afterthought

    Symptoms: builds take 45 min, half the E2E suite is red and
    ignored, every release needs a 2-day manual regression pass.
```

Teams arrive here because E2E tests *feel* more valuable ("they test the real thing!") and unit tests *feel* like busywork. But the inverted pyramid is slow, flaky, and expensive: a 1-line change forces a 40-minute E2E run, and a third of those runs fail for unrelated infra reasons. The team learns to ignore red, and the suite dies.

### Alternative: the Testing Trophy (Kent Dodds)

For front-end and many service codebases, Kent Dodds popularized the **Testing Trophy**, arguing the *integration* layer (in the front-end sense: a component + its real children, with only the network mocked) gives the best confidence-per-effort:

```
            ___________
           (   E2E     )      few
            -----------
        /                 \
       (   Integration     )  MOST — the fat middle, best ROI
        \                 /
         -----------------
        (      Unit        )  some
         -----------------
        [  Static (types,  ]  the base — lint + TypeScript catch
        [  lint) — free    ]  a whole class of bugs for ~free
         -----------------
```

His thesis: *"Write tests. Not too many. Mostly integration."* The reasoning: heavily-mocked unit tests on the front end pass while the app is broken (because you mocked the thing that was wrong). Tests that render a real component tree and assert on what the user sees give more confidence. The **static** layer (TypeScript + ESLint) is the foundation because it catches typos and type errors with zero test-writing effort.

**Pyramid vs. Trophy is not a contradiction** — they're tuned for different domains. Backend logic-heavy services lean pyramid (lots of pure-function unit tests). UI/glue-heavy code leans trophy (integration-heavy). The shared truth: **few E2E, and a solid static base.**

**Interview takeaway: Know the pyramid, name the ice-cream-cone anti-pattern, and be able to argue the testing-trophy nuance for front-end / glue code. Senior signal: "the right shape depends on where your bugs come from — logic-heavy code wants more unit tests, integration-heavy code wants more integration tests."**

---

## Unit Testing & Test Doubles

### What a unit test is (and isn't)

A **unit test** exercises one *unit of behavior* in isolation — usually one public method or one small class — with all slow/non-deterministic collaborators replaced by doubles. "Unit" means *isolated and fast*, not literally "one class." Two schools:

- **Solitary (London/mockist):** mock *every* collaborator; test the SUT alone.
- **Sociable (Detroit/classicist):** use real collaborators when they're fast and deterministic; only double the slow/external ones.

Most experienced engineers are sociable by default and reach for mocks only when a collaborator is slow, non-deterministic, or has side effects.

### The AAA structure

Every unit test should have three visually distinct phases — **Arrange, Act, Assert** (a.k.a. Given-When-Then):

```python
def test_apply_percentage_discount():
    # Arrange — set up inputs and the SUT
    cart = Cart(items=[Item("book", price=Money("20.00"))])
    discount = PercentageDiscount(percent=10)

    # Act — exercise ONE behavior
    total = discount.apply(cart)

    # Assert — one logical assertion
    assert total == Money("18.00")
```

One Act per test. If you find yourself with two Acts, you have two tests.

### FIRST — the properties of a good unit test

```
   F - Fast        milliseconds; a 10k-test suite must finish in seconds
   I - Isolated    no dependence on other tests or shared state
   R - Repeatable  same result every run, every machine (deterministic)
   S - Self-validating  pass/fail is automatic; no human eyeballing logs
   T - Timely       written with (ideally before) the code, not "later"
```

If a test violates FIRST it will eventually be deleted or ignored. Slow tests get skipped locally; order-dependent tests fail randomly; tests that need a human to read output get rubber-stamped.

### The taxonomy of test doubles

Gerard Meszaros' *xUnit Test Patterns* gives the precise vocabulary. Interviewers love this because most candidates blur "mock" and "stub" together. There are **five** distinct doubles:

| Double | Provides canned answers? | Records calls? | Has real logic? | Use it to... |
|---|---|---|---|---|
| **Dummy** | no | no | no | fill a required parameter you never use |
| **Stub** | yes (fixed) | no | no | feed the SUT a specific input from a collaborator |
| **Spy** | yes | **yes** | no | verify the SUT *called* a collaborator (after the fact) |
| **Mock** | yes | **yes (pre-programmed expectations)** | no | assert interactions *as a specification* |
| **Fake** | n/a | n/a | **yes (lightweight)** | a working but simplified impl (in-memory DB) |

#### Dummy — a placeholder you never use

```java
// The constructor needs a Logger, but this test never logs.
Logger dummyLogger = null;          // or Mockito.mock(Logger.class)
OrderService svc = new OrderService(realRepo, dummyLogger);
// We only care about repo behavior; the logger is a dummy.
```

#### Stub — canned return values to drive a code path

A stub *answers* but doesn't *assert*. Use it to put the SUT into the state you want.

```python
# pytest — stub the clock so "expired?" is deterministic
class StubClock:
    def now(self):
        return datetime(2026, 1, 1, 12, 0, 0)

def test_token_is_expired():
    token = Token(expires_at=datetime(2026, 1, 1, 11, 0, 0))
    assert token.is_expired(clock=StubClock()) is True
```

#### Spy — record calls, assert afterwards

A spy is a stub that *also remembers* how it was called.

```python
class EmailSpy:
    def __init__(self):
        self.sent = []
    def send(self, to, subject, body):
        self.sent.append((to, subject))   # record

def test_welcome_email_sent_on_signup():
    spy = EmailSpy()
    service = SignupService(emailer=spy)

    service.register("ada@x.com", "pw")

    assert len(spy.sent) == 1
    assert spy.sent[0][0] == "ada@x.com"   # assert AFTER the fact
```

#### Mock — interaction expectations set *before* the act

A mock is pre-programmed with the calls it *expects* and fails if they don't happen exactly. This is **interaction testing** as a specification.

```java
// Mockito — verify the SUT charged the gateway exactly once
@Test
void chargesGatewayExactlyOnce() {
    PaymentGateway gateway = mock(PaymentGateway.class);
    when(gateway.charge(any(), eq(1000)))
        .thenReturn(ChargeResult.success("ch_123"));

    CheckoutService svc = new CheckoutService(gateway);
    svc.checkout(cartWith(1000));

    verify(gateway, times(1)).charge(any(), eq(1000)); // interaction assertion
    verifyNoMoreInteractions(gateway);
}
```

#### Fake — a real but lightweight implementation

A fake has *working logic* but cuts corners unsuitable for production (in-memory instead of on-disk, no durability).

```python
class InMemoryUserRepo:           # a FAKE of a real DB-backed repo
    def __init__(self):
        self._db = {}
    def save(self, user):
        self._db[user.id] = user
    def find(self, user_id):
        return self._db.get(user_id)

def test_signup_then_login():
    repo = InMemoryUserRepo()      # fast, deterministic, real behavior
    svc = AccountService(repo)
    svc.signup("ada", "pw")
    assert svc.login("ada", "pw") is True
```

Fakes are underrated. A well-built in-memory fake of your repository gives you near-integration realism at unit-test speed, and (unlike mocks) it doesn't couple your tests to the exact call sequence.

### State testing vs. interaction testing

This is *the* conceptual fork:

- **State (classicist) testing** — exercise the SUT, then assert on the *resulting state* / return value. "After I deposit \$50, the balance is \$50." Robust to refactoring because it asserts *what*, not *how*.
- **Interaction (mockist) testing** — assert that the SUT *made the right calls* to its collaborators. "When I withdraw, it calls `auditLog.record()`." Necessary when the *side effect itself* is the behavior (sending an email, charging a card) — there's no return value to inspect.

```python
# STATE testing — assert outcome
def test_deposit_increases_balance():
    acct = Account(balance=0)
    acct.deposit(50)
    assert acct.balance == 50          # WHAT happened

# INTERACTION testing — assert the call happened
def test_withdrawal_is_audited(mocker):
    audit = mocker.Mock()
    acct = Account(balance=100, audit=audit)
    acct.withdraw(30)
    audit.record.assert_called_once_with("withdraw", 30)  # HOW it happened
```

Prefer **state testing** by default. Reach for interaction testing only when the side effect *is* the point (you cannot observe "an email was sent" via return value).

### The over-mocking trap

The most damaging anti-pattern in unit testing:

```python
# BAD — over-mocked, tests the mock not the code
def test_total(mocker):
    cart = mocker.Mock()
    cart.subtotal.return_value = 100
    cart.tax.return_value = 10
    cart.shipping.return_value = 5
    # we mocked everything; if total() is "return 999" this still
    # passes against our mock expectations -> we tested nothing real
```

Over-mocking produces tests that are:

1. **Tautological** — they assert the SUT calls the methods you decided it calls; they pass even when the real collaborators are broken or the wiring is wrong.
2. **Brittle to refactoring** — change *how* the code computes a result (without changing the result) and every interaction assertion breaks. The test fights the refactor instead of protecting it.
3. **False confidence** — green tests, broken integration. The classic "all unit tests pass, production is down" because the mock didn't match reality.

Rule of thumb: **mock across architectural boundaries (network, DB, clock, randomness), not within your own domain logic.** If you're mocking your own value objects, stop — use the real ones.

### Parametrized tests

When the *same logic* must hold across many inputs, don't copy-paste — parametrize. This turns a table of cases into a test each, with individual pass/fail reporting.

```python
import pytest

@pytest.mark.parametrize("n, expected", [
    (1,  "1"),
    (3,  "Fizz"),
    (5,  "Buzz"),
    (15, "FizzBuzz"),
    (0,  "FizzBuzz"),   # boundary: 0 is divisible by everything
])
def test_fizzbuzz(n, expected):
    assert fizzbuzz(n) == expected
```

```java
// JUnit 5 parametrized
@ParameterizedTest
@CsvSource({"1, 1", "3, Fizz", "5, Buzz", "15, FizzBuzz"})
void fizzBuzz(int n, String expected) {
    assertEquals(expected, FizzBuzz.of(n));
}
```

### Fixtures & setup/teardown

Tests need consistent starting state. **Fixtures** build it; **teardown** cleans it. The danger is *shared* fixtures leaking state between tests (an Order/Isolation violation).

```python
import pytest

@pytest.fixture
def empty_account():
    acct = Account(balance=0)        # fresh instance per test (good!)
    yield acct                       # test runs here
    # teardown after yield (close files, drop temp data) if needed

def test_a(empty_account):
    empty_account.deposit(10)
    assert empty_account.balance == 10

def test_b(empty_account):
    # gets its OWN fresh account — no leakage from test_a
    assert empty_account.balance == 0
```

```java
// JUnit 5 lifecycle
@BeforeEach void setUp()  { account = new Account(0); }  // per-test fresh
@AfterEach  void tearDown(){ /* close resources */ }
@BeforeAll static void once() { /* expensive shared setup, e.g. start container */ }
```

Prefer **function-scoped** fixtures (fresh per test) for isolation; use **class/module-scoped** only for genuinely expensive, *read-only* setup (e.g., a started Testcontainer).

**Interview takeaway: Know all five doubles by name, prefer state over interaction testing, and be loud about the over-mocking trap. The senior insight is "mock at the boundary, not inside your domain" — it shows you've felt the pain of brittle, tautological tests.**

---

## TDD & BDD

### Test-Driven Development: the Red-Green-Refactor loop

TDD inverts the usual order: you write a *failing* test first, make it pass with the simplest code, then clean up. The cycle:

```
        +-----------------------------------------+
        |                                         |
        v                                         |
   [ RED ] write a small failing test  -->  [ GREEN ] write the
   (it fails because the code            minimal code to make it
    doesn't exist yet)                   pass (even if ugly)
                                              |
                                              v
                                        [ REFACTOR ] clean up
                                        with the test as a net;
                                        tests stay green
                                              |
                                              +--> back to RED
```

The three rules (Uncle Bob's strict TDD):
1. Write no production code except to make a failing test pass.
2. Write only enough of a test to fail (a compile error counts).
3. Write only enough production code to pass the one failing test.

### A full worked example: the Roman Numeral kata

Let's build `int_to_roman(n)` the TDD way, several iterations, watching the design *emerge*.

**Iteration 1 — RED:** the simplest possible test.

```python
def test_one_is_I():
    assert int_to_roman(1) == "I"
```
Run it: `NameError: int_to_roman is not defined`. Red.

**Iteration 1 — GREEN:** the *simplest* thing that passes. Yes, hard-code it.

```python
def int_to_roman(n):
    return "I"
```
Green. This feels absurd — but it proves the test harness works and resists over-engineering.

**Iteration 2 — RED:** force generality.

```python
def test_two_is_II():
    assert int_to_roman(2) == "II"
```
Red (`"I" != "II"`).

**Iteration 2 — GREEN:**

```python
def int_to_roman(n):
    return "I" * n
```
Both tests green. (Works for 1, 2, 3.)

**Iteration 3 — RED:** introduce a new symbol.

```python
def test_five_is_V():
    assert int_to_roman(5) == "V"
```
Red (`"IIIII" != "V"`).

**Iteration 3 — GREEN:** the simplest pass — a lookup-and-subtract loop. The general structure now *emerges* from the pressure of the tests:

```python
def int_to_roman(n):
    numerals = [(5, "V"), (1, "I")]
    result = ""
    for value, symbol in numerals:
        while n >= value:
            result += symbol
            n -= value
    return result
```
All green (1,2,3,5). Note 4 would give `"IIII"` — but no test demands `"IV"` yet, so we don't write it (rule 3).

**Iteration 4 — RED:** the subtractive case.

```python
def test_four_is_IV():
    assert int_to_roman(4) == "IV"
```
Red (`"IIII" != "IV"`).

**Iteration 4 — GREEN:** add the subtractive pair to the table. The *same algorithm* handles it — beautiful.

```python
def int_to_roman(n):
    numerals = [(5, "V"), (4, "IV"), (1, "I")]   # order matters: high->low
    result = ""
    for value, symbol in numerals:
        while n >= value:
            result += symbol
            n -= value
    return result
```
All green.

**Iteration 5 — RED + GREEN:** scale up with a parametrized test; just extend the table.

```python
@pytest.mark.parametrize("n, roman", [
    (9, "IX"), (40, "XL"), (90, "XC"),
    (400, "CD"), (900, "CM"), (1994, "MCMXCIV"),
])
def test_complex(n, roman):
    assert int_to_roman(n) == roman

# GREEN: just complete the table — algorithm unchanged
def int_to_roman(n):
    numerals = [
        (1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),
        (100,"C"),(90,"XC"),(50,"L"),(40,"XL"),
        (10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I"),
    ]
    result = ""
    for value, symbol in numerals:
        while n >= value:
            result += symbol
            n -= value
    return result
```

**REFACTOR:** the code is already clean. We could extract `numerals` to a module constant, add a guard for `n <= 0`, etc. — done with green tests covering us.

What TDD *taught us here*: the table-driven algorithm wasn't designed up front — it was the simplest response to escalating tests, and it turned out to be the elegant general solution. TDD pushed us toward simplicity.

### Benefits and criticisms of TDD

| Benefits | Criticisms |
|---|---|
| Forces testable, decoupled design (you feel coupling immediately) | Doesn't fit exploratory/spike work where you don't yet know the API |
| 100% of code is covered by a *reason to exist* | Can lead to over-testing trivial getters; mock-heavy TDD breeds brittleness |
| Tests act as a precise spec & living docs | Slower for the first version (faster over the lifetime) |
| Tiny steps → bugs localized to the last few lines | Bad at finding *integration* and *emergent* bugs (it's unit-focused) |
| Refactoring is safe and continuous | Requires discipline; easy to "cheat" and write code first |

A balanced view (held by most seniors): TDD is a *fantastic design tool* for algorithmic and domain logic, *awkward* for UI and exploratory work, and *insufficient on its own* (you still need integration, E2E, property, and exploratory testing).

### BDD: Behavior-Driven Development

BDD reframes tests as *executable specifications of behavior* written in business language, so non-engineers (PMs, QA) can read and even write them. The structure is **Given-When-Then** (the same as Arrange-Act-Assert, but in natural language).

```gherkin
# features/withdrawal.feature  (Gherkin syntax, run by Cucumber)
Feature: ATM cash withdrawal

  Scenario: Successful withdrawal within balance
    Given the account balance is $100
    And the card is valid
    When the customer requests $40
    Then the ATM should dispense $40
    And the new balance should be $60

  Scenario: Withdrawal exceeding balance is rejected
    Given the account balance is $30
    When the customer requests $40
    Then the ATM should refuse the transaction
    And the balance should remain $30
```

The Gherkin steps are wired to code via **step definitions**:

```python
# steps/withdrawal_steps.py  (behave / pytest-bdd)
@given('the account balance is ${amount:d}')
def step_balance(context, amount):
    context.account = Account(balance=amount)

@when('the customer requests ${amount:d}')
def step_request(context, amount):
    context.result = context.atm.withdraw(context.account, amount)

@then('the ATM should dispense ${amount:d}')
def step_dispense(context, amount):
    assert context.result.dispensed == amount
```

**BDD vs TDD:** TDD is a *developer* discipline (drives design, code-level). BDD is a *collaboration* discipline (drives shared understanding, business-readable). BDD's value is the conversation it forces between dev, QA, and product *before* coding — the `.feature` file becomes the agreed contract. Its cost is the indirection layer (Gherkin → step defs); overused on internal logic it's pure ceremony.

**Interview takeaway: Be able to walk a red-green-refactor cycle live, including the "hard-code it first" step that signals you understand TDD's discipline. Frame BDD as Given-When-Then for cross-functional collaboration, not just "tests in English."**

---

## Integration & Contract Testing

### Why integration tests exist

Unit tests mock the database, so they *cannot* catch: a typo'd SQL column, an ORM that generates the wrong JOIN, a transaction that doesn't actually commit, a JSON field your deserializer ignores, or a migration that didn't run. Integration tests wire your code to **real** infrastructure (a real Postgres, a real Kafka) and verify the seams.

### Testcontainers: real dependencies, disposable

The old way of integration testing — a shared "test database" everyone connects to — is an Order/Isolation nightmare (tests pollute each other, one schema drift breaks everyone). **Testcontainers** spins up a *throwaway Docker container* per test run: a real Postgres, isolated, gone when the test ends.

```python
# pytest + testcontainers — a REAL Postgres, ephemeral
import pytest
from testcontainers.postgres import PostgresContainer
import sqlalchemy

@pytest.fixture(scope="session")
def pg_engine():
    with PostgresContainer("postgres:16") as pg:
        engine = sqlalchemy.create_engine(pg.get_connection_url())
        run_migrations(engine)        # apply real schema
        yield engine
        # container auto-destroyed on exit

def test_order_persists_and_reloads(pg_engine):
    repo = OrderRepository(pg_engine)
    order = Order(customer="ada", total=Money("42.00"))
    repo.save(order)

    loaded = repo.find(order.id)
    assert loaded.total == Money("42.00")   # round-trips through REAL SQL
```

```java
// JUnit 5 + Testcontainers — real Kafka
@Testcontainers
class OrderEventsIT {
    @Container
    static KafkaContainer kafka =
        new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.6.0"));

    @Test
    void publishesOrderCreatedEvent() {
        var producer = new OrderEventProducer(kafka.getBootstrapServers());
        producer.publish(new OrderCreated("o-1"));

        var consumed = consumeOne(kafka.getBootstrapServers(), "orders");
        assertThat(consumed.orderId()).isEqualTo("o-1");  // real serialization
    }
}
```

Testcontainers gives you the realism of production infra with the isolation of a unit test — the bug where your Avro schema doesn't match the consumer's gets caught here, never in production.

### Database testing strategies: keeping tests isolated

Each integration test must start from a known DB state. Three strategies, by trade-off:

| Strategy | How | Speed | Isolation | When |
|---|---|---|---|---|
| **Transactional rollback** | Open a transaction in setup, run test, **roll back** in teardown — nothing persists | Fastest | Excellent | Default for most repo tests |
| **Truncate / delete** | Wipe relevant tables between tests | Fast | Good | When the SUT manages its own transactions/commits |
| **Fresh schema / DB per test** | Recreate schema (or spin a new container) per test | Slow | Perfect | When tests need DDL or test migrations themselves |

```python
@pytest.fixture
def db_session(pg_engine):
    conn = pg_engine.connect()
    txn = conn.begin()              # START transaction
    session = Session(bind=conn)
    yield session                   # test does its work
    session.close()
    txn.rollback()                  # ROLL BACK — DB is pristine again
    conn.close()
```

The transactional-rollback trick is the workhorse: each test runs inside a transaction that is *never committed*, so the database is automatically clean for the next test with zero teardown cost. Caveat: it can't be used when the code under test commits or uses its own transactions.

### Consumer-Driven Contract Testing (Pact)

The microservices problem: Service A (consumer) calls Service B (provider). Spinning up *both* services for every test is slow and flaky (full E2E). But if you only unit-test A against a *mock* of B, your mock can drift from B's real behavior — B renames a field, A's tests stay green, **production breaks**.

**Contract testing** solves this. The consumer declares the *exact requests it makes and responses it expects* — that declaration is the **contract (pact)**. The provider then verifies it can satisfy that contract, *independently*, without both running together.

```
  CONSUMER side (Service A's repo)        PROVIDER side (Service B's repo)
  ----------------------------------      --------------------------------
  1. Write a test against a Pact          3. Pact replays the recorded
     MOCK of B. Pact records every           requests against the REAL B
     request A makes + expected resp.        and checks B's real responses
              |                                match the expected ones.
              v                                        ^
        +-----------+   publishes contract   +-----------+
        |  pact.json | ------------------->  | Pact      |
        +-----------+    (Pact Broker)       | verifies  |
                                             +-----------+

  If B changes a field A depends on, B's verification FAILS in B's CI,
  BEFORE B is deployed -> the breakage is caught at the source.
```

**Consumer side** — define the expectation:

```javascript
// consumer.pact.test.js  (Pact JS)
const provider = new PactV3({ consumer: 'OrderUI', provider: 'PricingService' });

provider
  .given('product P1 exists')
  .uponReceiving('a price request for P1')
  .withRequest({ method: 'GET', path: '/price/P1' })
  .willRespondWith({
    status: 200,
    body: { productId: 'P1', amount: like(1999), currency: 'USD' },
  });

await provider.executeTest(async (mockServer) => {
  const client = new PricingClient(mockServer.url);
  const price = await client.getPrice('P1');
  expect(price.amount).toBe(1999);
  // this run RECORDS the contract -> published to the broker
});
```

**Provider side** — verify it honors every published contract:

```java
// PricingServiceProviderTest.java  (Pact JVM)
@Provider("PricingService")
@PactBroker(url = "https://broker.internal")
class PricingContractVerificationTest {
    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void verifyContracts(PactVerificationContext ctx) {
        ctx.verifyInteraction();   // replays consumer expectations vs REAL provider
    }

    @State("product P1 exists")
    void seedP1() { repo.save(new Product("P1", 1999, "USD")); }
}
```

Why this prevents microservice breakage: the provider's CI fails the *instant* it would break any consumer's expectation, before deploy — and it does so **without the consumer running**. You get the safety of E2E coupling with the speed and independence of unit tests. The Pact Broker also enables "can-i-deploy" gating: "can PricingService v2 deploy without breaking any consumer currently in prod?"

**Interview takeaway: When the interviewer splits a system into microservices and asks "how do you keep service A from breaking service B," the senior answer is consumer-driven contract testing (Pact): the consumer publishes its expectations; the provider verifies them independently in its own CI — catching breakage at the source without full E2E.**

---

## End-to-End Testing

### What E2E is and why you want *few* of them

An **E2E test** drives the *fully assembled system* the way a real user does — through the browser UI or the public API — across all real services and databases. It is the only test that proves "a user can actually check out." It is also the slowest, flakiest, and most expensive test you own, which is exactly why the pyramid caps it at 5–10% and you reserve it for **critical user journeys**: sign-up, login, checkout, the one or two flows that, if broken, mean lost revenue.

### Tools: Selenium, Cypress, Playwright

| Tool | Architecture | Strengths | Weaknesses |
|---|---|---|---|
| **Selenium** | WebDriver protocol, multi-language, real browsers | Mature, broad browser/grid support | Verbose, slower, manual waits → flaky |
| **Cypress** | Runs *inside* the browser event loop | Great DX, auto-wait, time-travel debugger | Single-tab, weaker cross-origin/multi-domain |
| **Playwright** | Out-of-process via CDP/WebSocket | Fast, auto-wait, multi-browser/tab/origin, parallel | Newer; smaller (but growing) ecosystem |

Modern default for new projects: **Playwright** (auto-waiting kills the #1 source of flake — manual sleeps).

```javascript
// Playwright — a critical-path E2E with the Page Object pattern
test('user can complete checkout', async ({ page }) => {
  const login = new LoginPage(page);
  const cart  = new CartPage(page);

  await login.goto();
  await login.signIn('ada@x.com', 'pw');     // auto-waits for nav

  await cart.addItem('Clean Code');
  await cart.checkout();

  await expect(page.getByText('Order confirmed')).toBeVisible();
});
```

### Page Object Model: don't duplicate selectors

The **Page Object** pattern wraps each screen in a class that exposes *user intentions* (`signIn`, `addItem`) and hides the brittle CSS/XPath selectors. When the markup changes, you fix one place, not 50 tests.

```javascript
class LoginPage {
  constructor(page) { this.page = page; }
  goto()  { return this.page.goto('/login'); }
  async signIn(email, pw) {
    await this.page.getByLabel('Email').fill(email);
    await this.page.getByLabel('Password').fill(pw);
    await this.page.getByRole('button', { name: 'Sign in' }).click();
  }
}
```

### Sources of E2E flakiness (and fixes)

```
  Flake source                  Fix
  ----------------------------  -------------------------------------------
  Fixed sleeps (sleep 2s)       Auto-wait / wait-for-condition, never sleep
  Race with async rendering     Assert on visible state, not timers
  Shared test data / ordering   Seed fresh data per test; unique IDs
  Animations / transitions      Disable animations in test env
  Network nondeterminism        Stub 3rd-party calls; retry only network layer
  Brittle selectors (CSS path)  Use stable test-ids / roles / labels
  Test interdependence          Each test self-contained (create+teardown)
```

The golden rule: **never `sleep`**. A fixed sleep is either too short (flaky) or too long (slow) — always wait for a *condition* (element visible, network idle).

### Visual / snapshot testing

Two flavors:

- **Snapshot testing** (Jest): serialize a component's rendered output to a stored snapshot file; future runs diff against it. Cheap regression net for DOM/JSON structure — but easy to "just update the snapshot" mindlessly, which erodes its value.
- **Visual regression** (Percy, Playwright `toHaveScreenshot`, Chromatic): capture a *pixel screenshot* and diff it. Catches CSS/layout regressions invisible to DOM assertions (a button shifted off-screen, a color regression). Needs tolerance thresholds and a baseline-approval workflow to manage false positives from font rendering.

```javascript
// Playwright visual regression
await expect(page).toHaveScreenshot('checkout.png', { maxDiffPixels: 100 });
```

**Interview takeaway: E2E = few, critical-path only; Page Objects to fight selector churn; and the cardinal rule is never sleep, always wait-for-condition. Cite Playwright's auto-wait as the modern flake antidote.**

---

## Advanced Techniques

### Property-Based Testing

Example-based tests check specific inputs you thought of. **Property-based testing** checks an *invariant* against *hundreds of machine-generated inputs*, including the weird edge cases you'd never think of — and when it finds a failure, it **shrinks** it to the minimal reproducing case.

The classic invariant: `decode(encode(x)) == x` (round-trip), or `sort(sort(x)) == sort(x)` (idempotence), or `len(sorted(x)) == len(x)` (sorting preserves length).

```python
# Hypothesis — find an edge case in a "merge sorted lists" function
from hypothesis import given, strategies as st

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_merge_is_sorted_and_complete(a, b):
    a.sort(); b.sort()
    result = merge_sorted(a, b)

    # INVARIANT 1: output is sorted
    assert result == sorted(result)
    # INVARIANT 2: output is a permutation of all inputs
    assert sorted(result) == sorted(a + b)
```

Suppose `merge_sorted` has a bug handling duplicates across lists. Hypothesis generates thousands of pairs, finds `a=[0], b=[0]` fails, and *shrinks* it: it reports the **minimal** failing case `merge_sorted([0], [0])` rather than the giant random list that first triggered it. That minimal counterexample is the gift — it points straight at the bug.

```java
// jqwik (JVM) — same idea
@Property
void mergedListStaysSorted(@ForAll List<@From("sortedInts") Integer> a,
                           @ForAll List<@From("sortedInts") Integer> b) {
    var merged = Merger.merge(a, b);
    assertThat(merged).isSorted();
    assertThat(merged).hasSize(a.size() + b.size());
}
```

Property testing shines for: parsers/serializers (round-trip), data structures (invariants), pure algorithms, and anything with an algebraic law (commutativity, associativity, idempotence).

### Mutation Testing: how good is your suite *really*?

Coverage tells you which lines *ran*; it does **not** tell you whether your assertions would *catch a bug* in those lines. **Mutation testing** answers the real question: it deliberately introduces small bugs ("mutants") into your code — flip `>` to `>=`, `+` to `-`, `true` to `false` — and reruns your tests. If a test *fails*, the mutant is "killed" (good — your suite caught it). If all tests still *pass*, the mutant "survived" (bad — your suite is blind to that bug).

```
   Original:   if (age >= 18)  return ADULT;
                       |
                       v   mutate >= to >
   Mutant:     if (age > 18)   return ADULT;

   Re-run tests:
     - If a test fails -> MUTANT KILLED  (your suite catches the boundary)
     - If all pass     -> MUTANT SURVIVED (you have NO test for age == 18!)

   Mutation score = killed / total mutants
```

The killer insight: you can have **100% line coverage and a 40% mutation score** — every line runs, but your assertions are too weak to notice when the logic is wrong. Mutation score is a far truer measure of suite *effectiveness* than coverage. Tools: **PIT/Pitest** (Java), **mutmut**/**cosmic-ray** (Python), **Stryker** (JS).

```bash
# PIT (Java) — reports surviving mutants per class
mvn org.pitest:pitest-maven:mutationCoverage
# => "Line coverage: 92%   Mutation coverage: 61%"  <- the gap is the truth
```

Mutation testing is slow (it reruns the suite per mutant), so run it on critical modules or in nightly CI, not every commit.

### Fuzzing

**Fuzzing** throws malformed, random, or adversarial input at a program looking for crashes, hangs, memory-safety violations, or unhandled exceptions — invaluable for parsers, decoders, and anything touching untrusted bytes. **Coverage-guided fuzzers** (AFL, libFuzzer, Go's native `testing.F`, Atheris for Python) mutate inputs *and watch which new code paths they reach*, evolving toward inputs that explore more of the program.

```go
// Go native fuzzing — finds inputs that crash the parser
func FuzzParseConfig(f *testing.F) {
    f.Add([]byte("key=value"))          // seed corpus
    f.Fuzz(func(t *testing.T, data []byte) {
        // The contract: ParseConfig must NEVER panic, only return err.
        _, _ = ParseConfig(data)         // a panic here = a found bug
    })
}
```
Run `go test -fuzz=FuzzParseConfig`; it evolves inputs and saves any crashing case to the corpus as a permanent regression test.

### Load / Performance Testing

Functional tests prove *correctness*; load tests prove the system holds its **latency/throughput SLOs under realistic concurrency**. Tools: **k6** (script in JS), **JMeter** (GUI/XML), **Gatling**, **Locust**.

```javascript
// k6 — ramp to 200 virtual users, assert p95 latency SLO
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 200 },   // ramp up
    { duration: '3m', target: 200 },   // sustain
    { duration: '1m', target: 0 },     // ramp down
  ],
  thresholds: { http_req_duration: ['p(95)<300'] },  // SLO: p95 < 300ms
};

export default function () {
  const res = http.get('https://api.example.com/feed');
  check(res, { 'status 200': (r) => r.status === 200 });
}
```

Distinguish the four flavors: **load** (expected peak), **stress** (beyond peak, find the breaking point), **soak** (sustained, find leaks/degradation over hours), **spike** (sudden surge, test autoscaling).

### Chaos Engineering

Pioneered by Netflix, **chaos engineering** tests *resilience* by deliberately injecting failure into (often production) systems — killing instances, adding latency, severing network links — and verifying the system degrades gracefully and recovers. **Chaos Monkey** randomly terminates production instances during business hours, forcing engineers to build services that survive instance death. The discipline: form a hypothesis ("if we kill one AZ, p99 stays under SLO"), inject the failure in a controlled blast radius, measure, and either confirm resilience or find the weakness *before* a real outage does.

```
   Chaos experiment loop:
   1. Define steady state (the metric that means "healthy", e.g. p99 < 300ms)
   2. Hypothesize it holds under failure F (kill an instance / AZ / add 200ms)
   3. Inject F into a SMALL blast radius (one cell, low-traffic window)
   4. Observe: did steady state hold?  -> confirmed resilient
                did it break?          -> found a weakness, fix it
   5. Widen blast radius gradually as confidence grows
```

**Interview takeaway: Property-based testing finds edge cases you didn't think of (and shrinks them); mutation testing measures whether your assertions are strong enough (coverage can't); chaos engineering tests failure behavior, not just correctness. Name-dropping these signals you test beyond the happy path.**

---

## Testing Hard Things (async, concurrency, time, legacy)

These are the topics that separate a candidate who has only written textbook `add(2,2)` tests from someone who has fought real production code.

### Testing async / await

The pitfall: a test finishes *before* the async work does, so it passes without ever asserting anything ("the test forgot to wait"). Always `await` the operation and use your framework's async support.

```python
# pytest-asyncio — properly awaited
import pytest

@pytest.mark.asyncio
async def test_fetch_user():
    repo = FakeAsyncRepo({1: User(1, "ada")})
    user = await get_user(repo, 1)        # MUST await
    assert user.name == "ada"
```

```javascript
// Jest — return/await the promise so Jest waits for the assertion
test('resolves to the user', async () => {
  await expect(getUser(1)).resolves.toEqual({ id: 1, name: 'ada' });
});

test('rejects unknown id', async () => {
  await expect(getUser(999)).rejects.toThrow('not found');
});
```

For code that schedules work on timers, use **fake timers** so you don't actually wait:

```javascript
jest.useFakeTimers();
const cb = jest.fn();
scheduleRetry(cb, 5000);
jest.advanceTimersByTime(5000);   // jump forward instantly
expect(cb).toHaveBeenCalledTimes(1);
```

### Testing concurrency / races

Concurrency bugs are *non-deterministic* — the test passes 99 times and fails once, when the scheduler interleaves threads differently. Strategies, weakest to strongest:

1. **Stress / loop it** — run the concurrent operation thousands of times across many threads to make races likely. Weak (probabilistic) but cheap.
2. **Race detectors** — instrument runs to flag data races *even if no failure occurs*: Go's `-race`, Java's jcstress, ThreadSanitizer. Far more reliable than hoping a race manifests.
3. **Deterministic scheduling** — control thread interleaving explicitly so you can reproduce a specific race every time.

```go
// Go's race detector — catches the data race even without a wrong result
func TestCounterConcurrent(t *testing.T) {
    c := &Counter{}
    var wg sync.WaitGroup
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() { defer wg.Done(); c.Inc() }()
    }
    wg.Wait()
    if c.Value() != 1000 { t.Fatalf("got %d", c.Value()) }
}
// run:  go test -race    <- flags the unsynchronized write on c.count
```

```java
// CountDownLatch to maximize contention deterministically
@Test
void incrementIsThreadSafe() throws Exception {
    var counter = new Counter();
    int threads = 50;
    var start = new CountDownLatch(1);
    var done  = new CountDownLatch(threads);
    var pool  = Executors.newFixedThreadPool(threads);
    for (int i = 0; i < threads; i++) {
        pool.submit(() -> {
            start.await();                  // all threads release together
            for (int j = 0; j < 1000; j++) counter.inc();
            done.countDown();
            return null;
        });
    }
    start.countDown();                      // fire simultaneously -> max contention
    done.await();
    assertEquals(50_000, counter.get());
}
```

The senior point: **a passing concurrency test proves little; a race detector proving the *absence* of races is what you want.** Better still, *design out* the concurrency (immutability, message passing) so there's nothing racy to test.

### Testing with time

Code that calls `now()` directly is untestable ("it's expired if `now > expiry`" — how do you test that deterministically?). The fix is **dependency-inject a clock** (or freeze time).

```python
# Inject a clock — the clean, design-driven way
from datetime import datetime

class Clock:                      # production: real clock
    def now(self): return datetime.utcnow()

def is_expired(token, clock):
    return clock.now() > token.expires_at

class FixedClock:
    def __init__(self, t): self.t = t
    def now(self): return self.t

def test_token_expired():
    token = Token(expires_at=datetime(2026, 1, 1))
    assert is_expired(token, FixedClock(datetime(2026, 6, 1))) is True
```

```python
# freezegun — when you can't refactor to inject a clock (legacy)
from freezegun import freeze_time

@freeze_time("2026-06-17 12:00:00")
def test_report_uses_frozen_now():
    report = generate_daily_report()
    assert report.date == date(2026, 6, 17)   # now() is frozen everywhere
```

(JS: `jest.useFakeTimers()` + `jest.setSystemTime()`; Java: inject a `java.time.Clock`, the JDK's built-in seam — `Clock.fixed(...)` for tests.) Always test the nasty time cases: **timezone boundaries, DST transitions, leap seconds/years, midnight rollover.**

### Testing legacy code — Michael Feathers' approach

Feathers' definition (*Working Effectively with Legacy Code*): **"legacy code is simply code without tests."** The catch-22: you can't safely change it without tests, but it's untestable *because* of its tangled dependencies (it news up a DB connection in the constructor, calls static singletons, has 200-line methods).

The escape, step by step:

**1. Characterization tests** — before changing anything, pin down what the code *currently does* (bugs included) so your refactor can't change behavior unknowingly. You write a test, run it, and let the *actual output* tell you the assertion:

```python
def test_characterize_legacy_pricing():
    # We don't know the "right" answer — we capture the CURRENT one.
    result = legacy_calculate_price(qty=10, code="BULK")
    assert result == 87.50   # <- whatever it actually returns today
    # Now we have a net: refactors must keep this value (or we decide
    # intentionally to change it).
```

**2. Find a seam** — a *seam* is a place you can alter behavior without editing the code in that place. The most common is replacing a dependency. The enabling technique is **dependency-breaking**: extract the hard dependency behind an interface / a parameter so a test can substitute a fake.

```java
// BEFORE: untestable — news up the gateway internally (no seam)
class OrderProcessor {
    void process(Order o) {
        var gw = new RealPaymentGateway();   // hard-wired -> can't fake
        gw.charge(o.total());
    }
}

// AFTER: "Extract and Override" / constructor injection -> a SEAM appears
class OrderProcessor {
    private final PaymentGateway gw;
    OrderProcessor(PaymentGateway gw) { this.gw = gw; }   // inject -> seam
    void process(Order o) { gw.charge(o.total()); }
}
// Now a test passes a FakeGateway. We changed the wiring, not the logic,
// guarded by the characterization test we wrote first.
```

The cycle: **characterize → find/create a seam (dependency-break) → write real tests against the seam → refactor safely → repeat.** This is how you tame a 4,000-line untested service without a big-bang rewrite.

**Interview takeaway: For legacy code, lead with Feathers — "code without tests." Characterization tests pin current behavior; seams + dependency-breaking (extract an interface, inject the dependency) make it testable; then you refactor under the net. This is a top senior signal.**

---

## Code Quality & CI

### Coverage: a floor, never a goal

**Coverage** measures what fraction of code your tests *execute*. Know the three kinds, increasing in strength:

```
  Line/Statement coverage: did each line run?            (weakest)
  Branch coverage:         did each if/else branch run?  (stronger)
  Path coverage:           did each combination of branches run?  (strongest,
                                                            usually intractable)
```

Why **100% coverage is a vanity metric**:

```java
int classify(int age) {
    if (age >= 18) return ADULT;     // a test with age=20 covers this LINE
    return MINOR;                    // a test with age=10 covers this LINE
}
// -> 100% line coverage with two tests.
// But NEITHER tests age == 18 (the boundary) or age == 17.
// Coverage says "done"; the actual bug risk (off-by-one) is untested.
```

Coverage proves a line *ran*, not that an *assertion would catch a bug* in it. You can hit 100% with zero `assert` statements. Use coverage as a **floor** (e.g., "new code must not drop coverage below 80%") to catch *entirely untested* code, and use **mutation testing** for the real signal of whether your assertions bite. Chasing 100% drives developers to write assertion-free tests for trivial getters — pure cost, zero value.

### Flaky tests: root causes and the iron rule

A **flaky test** passes and fails non-deterministically on the same code. Flakiness is corrosive: it teaches the team to ignore red builds ("just re-run CI"), which destroys trust in the *entire* suite. Root causes map exactly to the TORN enemies of determinism:

| Root cause | Example | Fix |
|---|---|---|
| **Time** | asserting on `now()`, timezone, sleep-based timing | inject/freeze the clock; wait-for-condition not sleep |
| **Order** | test B relies on data test A created | isolate state; fresh fixtures; randomize order to *expose* it |
| **Shared state** | a static/global mutated across tests | reset between tests; avoid shared mutable singletons |
| **Random** | unseeded RNG/UUID in assertions | seed the RNG; assert on shape not exact value |
| **Network** | real HTTP/DNS to a flaky 3rd party | stub external calls; Testcontainers for owned infra |
| **Async/concurrency** | race between assert and background work | proper await; race detectors; deterministic scheduling |

The **iron rule: never blind-retry to make flakiness "go away."** Blind retries (auto-rerun-3-times-and-pass) hide real intermittent bugs and let flake accumulate. The disciplined response:

```
   1. Detect: track per-test pass/fail history; flag the flaky ones.
   2. Quarantine: move the flaky test out of the blocking suite so it
      stops blocking deploys -- but DON'T delete it (that loses coverage).
   3. Root-cause and FIX it (find which TORN cause it is).
   4. De-quarantine once it's stable.
   Re-running blindly is step 0 of giving up -- avoid it.
```

### Linters, static analysis, type checking

The cheapest, leftmost layer — catches bugs **without running the code**:

| Tool class | Examples | Catches |
|---|---|---|
| **Linters** | ESLint, Pylint, RuboCop, Checkstyle | style, unused vars, simple anti-patterns |
| **Static analysis** | SonarQube, Infer (Meta), CodeQL, SpotBugs | null derefs, resource leaks, security holes, complexity |
| **Type checkers** | mypy, TypeScript, Flow | type mismatches, missing-None handling, wrong signatures |
| **Formatters** | Prettier, Black, gofmt | consistent style (no human review of formatting) |

Type checking deserves emphasis: a static type system eliminates an *entire category* of tests. In a typed language you never write a test asserting "this function rejects a string argument" — the compiler guarantees it. This is the base of Kent Dodds' Testing Trophy: types + lint give enormous bug-catching leverage for near-zero test-authoring cost.

### The CI pipeline: cheap first, fail fast

CI runs the whole quality machine automatically on every push. The crucial design principle: **order stages cheapest-and-most-likely-to-fail first, so feedback is fast and you don't burn 30 minutes of E2E to discover a lint error.**

```
   git push / open PR
        |
        v
   [ 1. Lint + format check ]   seconds   -- fail here = instant feedback
        |  (pass)
        v
   [ 2. Type check ]            seconds
        |
        v
   [ 3. Unit tests ]           seconds    -- the fast pyramid base
        |
        v
   [ 4. Integration tests ]    1-3 min    -- Testcontainers spin up
        |
        v
   [ 5. Contract tests ]       ~1 min     -- Pact verification
        |
        v
   [ 6. E2E (critical path) ]  minutes    -- few, slowest, last
        |
        v
   [ 7. Coverage gate + build artifact ]
        |
        v
   merge / deploy

   FAIL FAST: a lint error must NOT wait for E2E to report. Each stage
   gates the next. Parallelize within a stage (shard tests across runners).
```

This mirrors the cost curve: catch the cheap-to-find problems with the cheap-to-run checks, and only pay for the expensive E2E run on code that already passed everything below it.

### Test naming and structure

A test's name is documentation. The best pattern: **what is being tested, under what condition, with what expected result.**

```python
# GOOD: reads as a spec sentence
def test_withdraw_with_insufficient_funds_raises_error(): ...
def test_apply_discount_at_exactly_100_percent_yields_zero(): ...

# BAD: tells you nothing when it fails in CI
def test_1(): ...
def test_withdraw(): ...
```

Pattern: `test_<unit>_<scenario>_<expected>` or the BDD `should_<expected>_when_<scenario>`. When `test_withdraw_with_insufficient_funds_raises_error` goes red in CI, you know *exactly* what broke without opening the file.

### Code review as a quality gate

Automated checks catch the mechanical; **code review** catches design, intent, naming, missing edge cases, and "is this even the right approach." Effective review (Google's standards): focus on *correctness, design, tests, readability*; review small diffs (big PRs get rubber-stamped); be specific and kind; and crucially — **a reviewer should check that the tests actually test the change, not just that tests exist.**

### Worked scenario: how you'd test a payment service

This is the canonical "test this whole feature" question. Layer by layer, matching the pyramid:

```
   PAYMENT SERVICE — test strategy by layer
   ----------------------------------------------------------------
   UNIT (many, fast)
     - fee/amount calculation: rounding, currency, min/max
     - state machine: PENDING -> AUTHORIZED -> CAPTURED -> REFUNDED
       (and illegal transitions, e.g. CAPTURED -> AUTHORIZED rejected)
     - validation: negative amount, zero, unsupported currency
     - idempotency-key dedup logic (pure function on the key store)

   INTEGRATION (some, Testcontainers)
     - repository round-trips against REAL Postgres (txn rollback per test)
     - gateway client against a FAKE gateway (in-memory) for success,
       decline, timeout, and network-error responses
     - the outbox/event publish to a real Kafka container

   CONTRACT (Pact)
     - consumer contract vs the external payment GATEWAY's API shape,
       so a gateway field rename is caught before deploy

   E2E (few, critical path only)
     - one happy-path: "user checks out -> card charged -> order CONFIRMED"

   PROPERTY-BASED
     - invariant: refund(amount) <= captured(amount) for all amounts
     - invariant: sum of partial captures == total authorized

   IDEMPOTENCY tests (CRITICAL for payments)
     - SAME idempotency key twice -> charged ONCE, second returns the
       first result (assert gateway.charge called exactly once)
     - concurrent duplicate requests -> exactly one charge (concurrency test)

   EDGE / FAILURE cases
     - gateway timeout after charge succeeded -> reconcile, don't double-charge
     - partial failure: charge ok, DB write fails -> outbox/retry, no lost money
     - currency rounding at boundaries; expired card; insufficient funds
```

The senior framing: for a payment service, **correctness is necessary but not sufficient — idempotency and failure behavior are where money is lost.** You test the happy path with one E2E, but you spend most of your effort on *duplicate-charge prevention* (idempotency under concurrency and retries) and *partial-failure reconciliation* (the charge succeeded but the DB write failed). That's the difference between "I tested it works" and "I tested it doesn't lose money."

**Interview takeaway: Coverage is a floor (100% is vanity; mutation testing is the real signal). Never blind-retry flaky tests — detect, quarantine, root-cause, fix. CI orders stages cheap-first to fail fast. For a payment service, the hard part isn't the happy path — it's idempotency and partial-failure.**

---

## Architecture / Diagrams

### The complete testing & quality stack

```
   +-----------------------------------------------------------+
   |                     DEVELOPER LAPTOP                       |
   |  edit -> [type check] -> [lint] -> [unit tests] (seconds)  |
   +----------------------------+------------------------------+
                                | git push / PR
                                v
   +-----------------------------------------------------------+
   |                      CI PIPELINE (fail fast)               |
   |  lint -> types -> unit -> integration -> contract -> e2e   |
   |   (s)     (s)     (s)      (min, TC)      (min)     (min)   |
   |                                                            |
   |  + coverage gate (floor)   + mutation (nightly)            |
   +----------------------------+------------------------------+
                                | all green
                                v
   +-----------------------------------------------------------+
   |                       DEPLOY PIPELINE                      |
   |  can-i-deploy? (Pact broker)  ->  canary  ->  full rollout |
   +----------------------------+------------------------------+
                                | in production
                                v
   +-----------------------------------------------------------+
   |              PRODUCTION TESTING & RESILIENCE              |
   |  synthetic monitoring  +  load/soak  +  chaos engineering  |
   +-----------------------------------------------------------+
```

### Test double decision tree

```
   Need to replace a collaborator?
        |
        +-- Just need to fill a param you never use? ---------> DUMMY
        |
        +-- Need it to RETURN specific data to drive a path? -> STUB
        |
        +-- Need to assert the SUT CALLED it?
        |        |
        |        +-- assert AFTER the fact (record then check) -> SPY
        |        +-- pre-program expectations as the spec ------> MOCK
        |
        +-- Need real-ish behavior, but fast/in-memory? ------> FAKE

   Default bias: use the REAL thing if it's fast & deterministic.
   Reach for a double only at a boundary (network/DB/clock/random).
```

### State vs interaction testing

```
   STATE TEST                         INTERACTION TEST
   (classicist / Detroit)             (mockist / London)
   -------------------------          --------------------------
   act on SUT                         pre-program mock expectations
   inspect resulting state            act on SUT
   assert the OUTCOME                 assert the CALLS happened

   robust to refactor (asserts WHAT)  brittle to refactor (asserts HOW)
   default choice                     use when side-effect IS the behavior
                                      (email sent, card charged)
```

---

## Real-World Examples

### Google: the monorepo and "test certified"

Google's monorepo runs an enormous test graph: a commit triggers only the tests *affected* by the change (computed from the Bazel/Blaze build dependency graph), running massively in parallel. The "Beyoncé Rule" — *if you liked it, you shoulda put a test on it* — means any behavior you care about must be guarded by a test, or you can't complain when someone breaks it. Flaky tests are tracked and quarantined automatically; a test that flakes too often is removed from the blocking set and assigned back to its owner.

### Netflix: chaos in production

Netflix's Chaos Monkey randomly terminates production EC2 instances during business hours. This *forces* every service to be resilient to instance death — you cannot ship a service that falls over when one node dies, because Chaos Monkey will kill a node and page you. The broader Simian Army adds Latency Monkey (injects delays), Chaos Gorilla (kills a whole availability zone), and more. The philosophy: the best way to verify your failure handling works is to *continuously cause failures* in a controlled way, rather than discovering on the night of a real outage that your fallback was never wired up.

### Meta: static analysis at diff time

Meta runs **Infer** (interprocedural static analysis catching null-deref, resource leaks, concurrency issues) and **Sapienz** (automated UI test-input generation that finds crashes) on essentially every code change in Phabricator, *before* it lands. The bet: at billions of users and continuous deployment, you cannot rely on humans to catch null-pointer bugs — you automate the detection and surface it as an inline review comment, shifting detection as far left as possible.

### Stripe / payments: idempotency keys

Payment APIs (Stripe being the canonical example) require **idempotency keys** precisely because networks retry. A client sends `Idempotency-Key: abc123`; if the request is retried (timeout, then resend), the server recognizes the key and returns the *original* result instead of charging again. The test suite for such a service spends enormous effort proving "the same key never charges twice, even under concurrent duplicate requests" — the exact idempotency + concurrency tests from the payment scenario above.

---

## Real-Life Analogies

| Concept | Analogy |
|---|---|
| **Test pyramid** | Building inspection: many cheap material checks (unit), some assembly checks (integration), one final walkthrough (E2E). You don't do a full walkthrough to verify a single brick. |
| **Ice-cream cone** | Skipping all component checks and only doing a final walkthrough — you find problems too late, when fixing means tearing down finished walls. |
| **Unit test** | Testing one Lego brick clicks and holds, before building the castle. |
| **Integration test** | Checking two bricks actually snap together — individually fine, but the studs might not align. |
| **E2E test** | Walking the finished castle the way a visitor would. |
| **Test double / mock** | A stunt double in a film — stands in for the expensive/dangerous real actor for a specific shot. |
| **Stub** | A cardboard cutout that says one fixed line. |
| **Mock** | An actor with a script you check they followed exactly. |
| **Fake** | A driving simulator — real controls, real feedback, but no actual road. |
| **TDD red-green-refactor** | Sculpting: rough out the shape (red→green), then refine (refactor), checking against the reference photo (the test) constantly. |
| **Property-based testing** | Hiring a chaos-loving QA tester who tries thousands of weird inputs *and* hands you the single simplest one that broke it. |
| **Mutation testing** | A fire drill for your alarm system: deliberately start small "fires" (mutants) to check the alarms (tests) actually go off. |
| **Coverage** | A checklist of rooms you *entered* — says nothing about whether you *inspected* anything in them. |
| **Flaky test** | A smoke detector that beeps randomly — soon everyone ignores it, including when there's a real fire. |
| **Contract test** | A pre-agreed wiring diagram between two contractors, each verifying their side independently before the walls go up. |
| **Chaos engineering** | A fire drill for the whole building, run on purpose, so the real fire isn't the first time you find the exits are locked. |
| **Characterization test** | Photographing an old machine's exact output before you repair it, so you can prove you didn't change its behavior. |

---

## Memory Tricks / Mnemonics

- **AAA** — *Arrange, Act, Assert*. The skeleton of every test.
- **FIRST** — *Fast, Isolated, Repeatable, Self-validating, Timely*. The five virtues of a unit test.
- **TORN** — *Time, Order, Random, Network/concurrency*. The four enemies of determinism = the four root causes of flaky tests.
- **Given-When-Then** — the BDD phrasing of AAA; the language of contracts.
- **Red-Green-Refactor** — the TDD heartbeat.
- **Dummy / Stub / Spy / Mock / Fake** — the five doubles. Mnemonic order of increasing capability: *"Dumb Stubs Spy on Mocking Fakes."*
- **Pyramid shape** — *many at the bottom, few at the top*. If it's inverted (ice-cream cone), it's broken.
- **"Mock at the boundary, not in the middle"** — the over-mocking antidote.
- **"Coverage is a floor, mutation is the truth."**
- **"Never sleep, always wait."** — E2E flakiness rule.
- **"Never blind-retry flake."** — detect → quarantine → root-cause → fix.
- **Beyoncé Rule** — *"if you liked it you shoulda put a test on it."* (Google.)
- **Feathers' definition** — *"legacy code is code without tests."*

---

## Common Interview Questions

### Q1: "What is the test pyramid, and what goes wrong when it's inverted?"

**Model answer:** The pyramid (Mike Cohn) prescribes *many* fast, isolated unit tests at the base (~60–80%), *some* integration tests in the middle (~15–30%), and *few* slow, realistic E2E tests at the top (~5–10%). The shape follows a cost/value trade-off: unit tests are fast, stable, and pinpoint the broken function; E2E tests are slow, flaky, and only tell you "something in checkout broke." Inverting it — the **ice-cream cone** (mostly E2E + manual QA, few unit) — produces 40-minute builds where a third of runs fail on infra, so the team learns to ignore red and the suite dies. The right shape depends on where bugs come from: logic-heavy backends lean pyramid; integration/glue-heavy front-ends lean toward Kent Dodds' testing trophy (fat integration middle).

**Follow-ups:**
- *"How many E2E tests should a service have?"* → Few — only critical revenue paths (login, checkout). They're the most expensive to maintain.
- *"What's the testing trophy?"* → Front-end-oriented variant: static (types+lint) base, mostly integration, some unit, few E2E. "Write tests. Not too many. Mostly integration."

### Q2: "Explain the difference between a mock, a stub, and a fake."

**Model answer:** All three are *test doubles*, but they differ in purpose. A **stub** provides canned return values to drive the SUT down a path — it answers but never asserts. A **mock** is pre-programmed with the interactions it *expects* and fails if they don't happen — it's a *specification of behavior*, used for interaction testing. A **fake** has real, working logic but cuts production corners (an in-memory repository instead of a real DB) — fast and deterministic with real behavior. (Plus *dummy* — a never-used placeholder — and *spy* — records calls to assert after the fact.) Default bias: use the real collaborator if it's fast and deterministic; reach for a double only at a boundary.

**Follow-ups:**
- *"When would you prefer a fake over a mock?"* → When the call *sequence* shouldn't be coupled to the test — a fake lets you assert on resulting *state* (robust to refactor), whereas a mock locks in *how* the SUT calls collaborators (brittle).
- *"What's the over-mocking trap?"* → Mocking your own domain objects produces tautological tests that pass even when integration is broken and shatter on every refactor.

### Q3: "Walk me through TDD with a concrete example."

**Model answer:** Red-green-refactor. I write the smallest failing test first — say `int_to_roman(1) == "I"` — it fails because the function doesn't exist (RED). I make it pass with the *simplest* code, even hard-coding `return "I"` (GREEN). Then a new test `int_to_roman(2) == "II"` forces generality → `"I" * n`. A test for `5 == "V"` forces a lookup-and-subtract loop, which a test for `4 == "IV"` extends with a subtractive pair — and that same table-driven algorithm scales to the whole numeral system. The design *emerged* from the tests rather than being designed up front, and it stayed minimal. Each step I refactor with green tests as a net.

**Follow-ups:**
- *"Isn't hard-coding `return 'I'` silly?"* → It proves the harness works and resists over-engineering; the next test forces real logic. Tiny steps mean bugs are localized to the last few lines.
- *"When is TDD a bad fit?"* → Exploratory spikes where you don't yet know the API, and UI work. TDD is also unit-focused — it won't find integration/emergent bugs.

### Q4: "How would you test code that depends on the current time?"

**Model answer:** Never call `now()` directly inside logic — it's non-deterministic and untestable. The clean fix is to **inject a clock** abstraction; production uses the real clock, tests pass a `FixedClock` returning a known instant, so "is this token expired?" becomes deterministic. If I can't refactor (legacy), I use a time-freezing library — `freezegun` in Python, `jest.setSystemTime` in JS, `Clock.fixed` in Java. I'd also explicitly test the nasty cases: timezone boundaries, DST transitions, leap years, and midnight rollover.

**Follow-ups:**
- *"Same question for randomness?"* → Inject a seeded RNG, or assert on the *shape* of the output, not the exact value.
- *"What if a downstream library calls `now()` internally?"* → Freeze at the system-clock level (freezegun patches `datetime.now`), or wrap the library behind a seam you can fake.

### Q5: "What's the difference between code coverage and mutation testing?"

**Model answer:** Coverage measures which lines/branches your tests *execute* — it proves a line *ran*, not that an assertion would *catch a bug* in it. You can have 100% line coverage with zero `assert` statements. Mutation testing measures suite *effectiveness*: it injects small bugs (mutants) — flip `>=` to `>`, `+` to `-` — reruns the tests, and checks whether any test *fails* (kills the mutant). Surviving mutants reveal logic your assertions can't detect. It's common to see 100% coverage with a 60% mutation score — the 40% gap is your real blind spot. So: coverage is a *floor* to find entirely-untested code; mutation score is the *truth* about assertion strength.

**Follow-ups:**
- *"Why not run mutation testing on every commit?"* → It reruns the suite per mutant — too slow. Run it on critical modules or nightly.
- *"Why is chasing 100% coverage harmful?"* → It drives assertion-free tests on trivial getters: pure cost, false confidence.

### Q6: "You have a flaky test. What do you do?"

**Model answer:** First, I do **not** blind-retry it — auto-rerunning until green hides real intermittent bugs and trains the team to ignore red, which destroys trust in the whole suite. Instead: (1) **detect** — confirm it's flaky from pass/fail history; (2) **quarantine** — move it out of the blocking suite so it stops gating deploys, but don't delete it (that loses coverage); (3) **root-cause** — it's almost always one of TORN: Time, Order/shared-state, Random, or Network/concurrency; (4) **fix** the underlying cause — inject the clock, isolate the fixture, seed the RNG, stub the network, fix the await/race; (5) **de-quarantine** once stable.

**Follow-ups:**
- *"What's the most common cause?"* → Order/shared state (a test depending on another's leftover data) and time. Randomizing test order *exposes* order dependence.
- *"How do you catch a race that only fails 1-in-1000?"* → A race detector (`go test -race`, jcstress, ThreadSanitizer) flags the race *even when no failure manifests* — far better than hoping it surfaces.

### Q7: "Two microservices, A calls B. How do you stop B's deploy from breaking A — without running both?"

**Model answer:** Consumer-driven contract testing, e.g. Pact. On the consumer (A) side, I write tests against a Pact *mock* of B; Pact records the exact requests A makes and responses it expects into a **contract** published to a broker. On the provider (B) side, B's CI replays those recorded expectations against the *real* B and fails if it can't satisfy them. So if B renames a field A depends on, B's *own* CI goes red before deploy — catching the breakage at the source, with neither service running the other. The broker also enables "can-i-deploy" gating: B v2 can't ship if it breaks any consumer currently in production.

**Follow-ups:**
- *"Why not just E2E both services?"* → Slow, flaky, and combinatorial as services multiply; contract tests give the same safety at unit-test speed and independence.
- *"What about async/event contracts?"* → Pact and similar tools support message contracts — the producer's published event shape vs the consumer's expectations.

### Q8: "How do you test a payment service?"

**Model answer:** Layer by layer. **Units** for the pure logic: fee/rounding math, the PENDING→AUTHORIZED→CAPTURED→REFUNDED state machine (including rejecting illegal transitions), and validation. **Integration** (Testcontainers): repository round-trips against real Postgres with transactional rollback, and the gateway client against a *fake* gateway covering success/decline/timeout/network-error. **Contract** (Pact) against the external gateway's API so a field rename is caught pre-deploy. **One E2E** for the happy path. **Property-based** invariants (refund ≤ captured; partial captures sum to authorized). But the real focus for payments is **idempotency** — same idempotency key charges exactly once, even under concurrent duplicate requests — and **partial-failure reconciliation** — gateway charge succeeds but the DB write fails, and we must not lose or double-charge money. Correctness is necessary; *not losing money under retries and failures* is the point.

**Follow-ups:**
- *"How do you test the duplicate-charge case under concurrency?"* → Fire concurrent requests with the same idempotency key and assert `gateway.charge` was called exactly once (interaction test) plus a race detector / contention harness.
- *"Charge succeeds but your DB write fails — how do you test the recovery?"* → Simulate the failure (fake DB throws after the fake gateway returns success), assert the outbox/retry reconciles to a single consistent charge.

### Q9: "When do you mock versus use the real thing?"

**Model answer:** Default to the **real** collaborator when it's fast and deterministic — including your own value objects and domain logic. Reach for a double only at an *architectural boundary*: the network, the database, the clock, randomness, or anything with slow/irreversible side effects (sending email, charging a card). Mocking inside your own domain produces tautological, refactor-brittle tests that pass while integration is broken — the over-mocking trap. So the rule is "mock at the boundary, not in the middle," and prefer **state** assertions (assert the outcome) over **interaction** assertions (assert the calls) unless the side effect itself is the behavior.

**Follow-ups:**
- *"Mockist vs classicist?"* → Mockist (London) mocks everything; classicist (Detroit) uses real collaborators when cheap. Most seniors lean classicist for robustness to refactoring.
- *"Downside of a fake DB vs a real one?"* → A fake can drift from real SQL/transaction semantics; that's why you *also* keep a thin layer of integration tests against a real Postgres (Testcontainers).

### Q10: "How do you make code that wasn't written to be testable, testable?"

**Model answer:** Michael Feathers' playbook — "legacy code is code without tests." First I write **characterization tests** that pin down current behavior (capturing whatever it actually outputs today, bugs included) so any refactor is guarded. Then I find or create a **seam** — a place to alter behavior without editing that code — typically by **dependency-breaking**: extract a hard-wired dependency (a `new RealGateway()` in a constructor) behind an interface and inject it, so a test can substitute a fake. Now I write real tests against the seam, refactor safely under the characterization net, and repeat. This tames a huge untested class incrementally instead of a risky big-bang rewrite.

**Follow-ups:**
- *"What if the dependency is a static singleton or global?"* → Wrap it behind an instance interface (a thin adapter) and inject the adapter; or use a "extract and override" subclass for testing.
- *"How do you know your refactor didn't change behavior?"* → The characterization tests stay green; if one changes, it's an intentional decision, not an accident.

### Q11: "What is property-based testing and when would you use it?"

**Model answer:** Instead of asserting on specific examples, you assert an *invariant* that must hold for *all* inputs, and the framework (Hypothesis, jqwik) generates hundreds of random inputs to try to falsify it — then **shrinks** any failure to the minimal reproducing case. Great invariants: round-trip (`decode(encode(x)) == x`), idempotence (`sort(sort(x)) == sort(x)`), or "merge of two sorted lists is sorted and a permutation of the inputs." It excels at parsers/serializers, data structures, and pure algorithms with algebraic laws, and routinely finds edge cases (empty, duplicates, extreme values) that humans forget. The shrinking is the magic — it hands you `merge([0],[0])` instead of the giant random list that first failed.

**Follow-ups:**
- *"Downsides?"* → You need to *find* a good invariant (sometimes hard); failures can be intermittent across seeds, so you pin the failing seed as a regression test.
- *"How is it different from fuzzing?"* → Fuzzing typically hunts crashes/security on untrusted bytes; property testing asserts *semantic* invariants. They overlap (both generate inputs) but answer different questions.

### Q12: "What's the difference between integration and E2E testing?"

**Model answer:** Both exercise more than one component, but at different scope and cost. An **integration test** verifies *your code* against a *real* slice of infrastructure — your repository against a real Postgres (Testcontainers), your producer against a real Kafka — catching serialization, SQL, schema, and transaction-boundary bugs that unit tests miss because they mocked the DB. An **E2E test** drives the *fully assembled system* as a user does, through the UI or public API across all real services, catching broken user journeys, routing, and auth flows. Integration tests are medium-speed and you have a fair number; E2E are slow and flaky, so you keep them few and reserved for critical paths.

**Follow-ups:**
- *"How do you keep integration DB tests isolated?"* → Transactional rollback per test (open a txn, never commit), or truncate/fresh-schema per test depending on whether the code manages its own transactions.
- *"Why are E2E flaky and how do you reduce it?"* → Timing, async rendering, shared data, brittle selectors, third-party networks. Fix with auto-wait (never sleep), fresh seeded data, stable test-ids, and stubbing external services.

---

## Senior-Level Discussion Points

- **Tests are a design tool, not just a verification tool.** Hard-to-test code is badly-designed code: if you need 20 mocks, your class has too many responsibilities. The *pain* of writing the test is the most honest design-smell detector you have. A senior treats "this is hard to test" as "this needs to be redesigned," not "I'll skip the test."

- **The cost of a test is its maintenance, not its authoring.** A brittle, over-mocked test that breaks on every refactor has *negative* value — it slows you down more than the bug it might catch. Optimize for tests that fail *only* when behavior actually changes. Asserting on *what* (state) rather than *how* (interactions) is the main lever.

- **Confidence-per-effort is the real metric.** Not coverage, not test count. Kent Dodds' point: the question is "what gives me the most confidence per unit of effort and maintenance?" — and the answer skews toward integration tests for glue code and unit tests for logic, with few E2E.

- **Determinism is a property of the architecture.** Flakiness isn't bad luck; it's leaked non-determinism (TORN). The fix is often *design*: inject clocks, isolate state, make domain objects immutable, push side effects to the edges. A codebase designed for testability is rarely flaky.

- **Testing in production is legitimate.** Synthetic monitoring, canary analysis, feature flags, shadow traffic, and chaos engineering test things you *cannot* fully replicate in staging (real scale, real data distributions, real failure modes). Mature orgs test *both* pre- and post-deploy.

- **Mutation testing exposes the coverage lie at the team level.** When a team is proud of 95% coverage, run mutation testing once and watch the score come back at 55%. It reframes the conversation from "are lines covered" to "would we actually catch a bug" — a more honest, motivating metric.

- **Contract testing is an organizational tool.** It decouples teams: each service team can deploy independently, confident they haven't broken consumers, *without* coordinating an integrated E2E environment. As the org scales to hundreds of services, full E2E becomes combinatorially impossible — contracts are what make independent deployment safe.

- **You cannot test quality in; you build it in.** Tests *reveal* quality, they don't *create* it. Pairing tests with type systems, static analysis, small reviewed diffs, and good design is what produces quality — testing is one pillar, not the whole building.

- **Flaky tests have an org-level cost: they erode trust in red.** Once "the build is red but it's probably just flaky" becomes acceptable, *every* real failure is at risk of being ignored. Maintaining a green, trustworthy `main` is a cultural asset worth aggressive quarantine policies to protect.

---

## Typical Mistakes Candidates Make

- **Only testing the happy path.** Juniors test `add(2,2)==4`. Seniors immediately enumerate empty, null, zero, negative, max-int, and the *boundary* (the exact `==18` case). The boundaries are where bugs live.

- **Over-mocking.** Mocking everything — including their own domain objects — producing tautological tests that pass while the system is broken and shatter on every refactor. (The #1 testing anti-pattern.)

- **Confusing mock and stub.** Saying "I'll mock the database to return a user" when they mean *stub* (canned return, no interaction assertion). Interviewers notice the imprecision.

- **Treating 100% coverage as the goal.** Not realizing coverage proves a line *ran*, not that an assertion would *catch a bug*. Chasing 100% with assertion-free tests.

- **Asserting on `now()` / random / order** and then being surprised the test is flaky. Not recognizing TORN as the root cause.

- **Blind-retrying flaky tests** to get a green build — hiding real intermittent bugs and normalizing red.

- **Inverting the pyramid** by reaching for E2E ("test the real thing!") for logic that belongs in a fast unit test — ending up with a slow, flaky suite.

- **Using `sleep` in E2E tests** instead of waiting for a condition — guaranteeing either flake (too short) or slowness (too long).

- **Writing tests *after* the fact as an afterthought** rather than alongside the code — leading to tests that merely echo the implementation instead of specifying behavior.

- **For microservices, proposing full E2E** to prevent breakage instead of contract testing — not realizing it's combinatorially unscalable.

- **Forgetting idempotency and failure cases** for money/critical flows — testing that a charge works, but not that a *retry* doesn't double-charge.

- **Saying "I'd write tests" without specifics** when asked how to test their solution — instead of enumerating equivalence classes, boundaries, and which layer each case belongs to.

---

## How This Connects to Other Topics

- **Low-Level Design (06):** Testability *is* good design. SOLID — especially Dependency Inversion — is what makes code mockable; a class that depends on an *interface* can be tested with a fake. The over-mocking trap is a symptom of poor cohesion. "Hard to test" ≡ "bad LLD."

- **System Design / HLD:** Contract testing is the answer to "how do services evolve independently." Idempotency, retries, and timeouts (designed at the HLD level) are exactly what the test suite must verify. Testability shapes architecture (hexagonal/ports-and-adapters exists largely to make the core testable).

- **Performance Engineering (09):** Load, stress, soak, and spike tests are performance testing applied as a *gate*. The same percentile discipline (p95/p99 SLOs) shows up as load-test thresholds. Chaos engineering tests resilience, the failure side of performance.

- **Concurrency / Multithreading:** Race detectors, deterministic scheduling, and "design out the concurrency" all live at the intersection. A concurrency test that passes proves little; a race detector proving *absence* of races is the goal — and immutable design makes both easier.

- **CI/CD & DevOps:** The test suite is the engine of continuous deployment. Fail-fast pipeline ordering, can-i-deploy gating, canary analysis, and feature flags are all test-and-quality machinery. No trustworthy suite → no continuous deployment.

- **Distributed Systems:** Testing partial failure, network partitions, and idempotency under retries is core to both distributed-systems design *and* its test strategy. Chaos engineering directly tests the fallacies of distributed computing.

- **Security:** Fuzzing and static analysis (CodeQL, Infer) overlap heavily with security testing — both hunt for the unhandled input that crashes or exploits the system.

---

## FAANG Interview Tips

1. **After you code, volunteer the tests.** Don't wait to be asked. "Let me note the test cases: empty input, single element, the boundary at N, the overflow case, and the null case." This is a strong seniority signal.

2. **Always name the boundary.** For any logic, the off-by-one boundary (`==`, the exact threshold) is the highest-value test. Saying "and critically, the `age == 18` case" shows you know where bugs hide.

3. **Use precise vocabulary.** Say *stub* when you mean canned-return, *mock* when you mean interaction-assertion, *fake* for in-memory. Imprecision reads as inexperience.

4. **Reach for the pyramid by name** and the ice-cream-cone anti-pattern. If front-end, mention the testing trophy. It frames your whole answer.

5. **For microservices, say "consumer-driven contract testing (Pact)"** the moment independent deployment comes up. It's the senior answer to "stop A breaking B."

6. **Know the over-mocking trap cold.** "I'd mock at the boundary — the gateway and the DB — but use real domain objects, to avoid tautological tests that break on refactor." Instant credibility.

7. **Frame coverage correctly.** "I use coverage as a floor to find untested code, but mutation testing for the real signal of assertion strength." Sets you apart from "we hit 90% coverage."

8. **Handle flaky tests with the disciplined process,** never "re-run it." Detect → quarantine → root-cause (TORN) → fix.

9. **For time/random/async, lead with dependency injection** (inject a clock/RNG), falling back to freeze-libraries for legacy.

10. **For payments / money / critical flows, emphasize idempotency and partial-failure**, not just the happy path. "The hard part isn't that it charges — it's that a retry doesn't charge twice."

11. **For legacy code, cite Feathers:** characterization tests → seams → dependency-breaking → refactor under the net.

12. **Connect to design.** "This was hard to test, which tells me the class has too many responsibilities — I'd extract the gateway behind an interface." Testing as a design signal lands well at the senior bar.

---

## Revision Cheat Sheet

### 10-Minute Summary

Testing buys **confidence under change**. The cost of a bug grows ~10× per stage it escapes — so **shift left**. The **test pyramid** says many fast unit tests, some integration, few slow E2E; the inverted **ice-cream cone** (mostly E2E + manual) is the anti-pattern; the **testing trophy** (integration-heavy + static base) is the front-end alternative.

A good unit test follows **AAA** (Arrange-Act-Assert) and **FIRST** (Fast, Isolated, Repeatable, Self-validating, Timely). **Five doubles:** dummy (placeholder), stub (canned return), spy (records calls), mock (interaction spec), fake (in-memory real logic). Prefer **state** over **interaction** testing; **mock at the boundary, not in the middle** (over-mocking trap).

**TDD** = red-green-refactor: failing test → simplest pass → clean up. **BDD** = Given-When-Then in business language (Gherkin/Cucumber) for cross-functional contracts.

**Integration** tests use real infra via **Testcontainers** (ephemeral Postgres/Kafka), isolated by **transactional rollback**. **Contract testing (Pact)** lets the consumer publish expectations the provider verifies independently — stops microservice breakage without full E2E.

**E2E:** few, critical-path only; **never sleep, always wait** (Playwright auto-wait). **Advanced:** property-based (invariants + shrinking, Hypothesis/jqwik), mutation testing (kills mutants → real assertion strength, beats coverage), fuzzing, load/k6, chaos engineering (Netflix).

**Hard things:** inject a **clock** for time (freezegun fallback); **race detectors** (`go test -race`) for concurrency; proper **await** for async; **characterization tests + seams + dependency-breaking** (Feathers) for legacy.

**Quality:** coverage is a **floor** (100% is vanity); mutation testing is the truth. **Flaky** tests → detect, quarantine, root-cause (**TORN**), fix — **never blind-retry**. CI runs **cheap-first, fail fast** (lint → types → unit → integration → contract → e2e).

### Key Points

- **Shift left** — every stage a bug survives costs ~10× more.
- **Pyramid** — many unit, some integration, few E2E. Inverted = ice-cream cone (bad).
- **FIRST + AAA** — the anatomy of a good unit test.
- **5 doubles** — dummy, stub, spy, mock, fake. Know each precisely.
- **State > interaction**; **mock at the boundary** — the over-mocking antidote.
- **TDD** — red-green-refactor; design emerges, stays minimal.
- **Testcontainers** for real-infra integration; **transactional rollback** for DB isolation.
- **Contract testing (Pact)** — independent deployment without combinatorial E2E.
- **Never sleep** in E2E; auto-wait for conditions.
- **Property-based** finds + shrinks edge cases; **mutation** measures assertion strength.
- **Coverage = floor; mutation = truth.** 100% coverage with weak asserts is vanity.
- **TORN** — Time, Order, Random, Network = the four causes of flakiness.
- **Never blind-retry flake** — detect → quarantine → root-cause → fix.
- **Inject the clock**; **race detectors** for concurrency; **Feathers** for legacy.
- **Payments** — idempotency + partial-failure, not just the happy path.

### Cheat Sheet Table

| Concept | Rule / Mnemonic | Key Insight |
|---|---|---|
| Cost of a bug | ~10× per stage escaped | Shift detection left |
| Test pyramid | many unit / some integ / few E2E | Inverted = ice-cream cone |
| Testing trophy | static / integration-heavy / few E2E | Front-end alternative |
| Good unit test | AAA + FIRST | Fast, Isolated, Repeatable, Self-validating, Timely |
| 5 doubles | Dummy, Stub, Spy, Mock, Fake | Increasing capability |
| Mock vs stub | mock asserts calls; stub returns data | Don't conflate |
| State vs interaction | assert WHAT vs assert HOW | Prefer state (refactor-robust) |
| Over-mocking | mock at boundary, not in middle | Avoid tautological tests |
| TDD | Red → Green → Refactor | Simplest pass first |
| BDD | Given-When-Then (Gherkin) | Cross-functional contract |
| Integration | Testcontainers (real infra) | Catches SQL/serialization bugs |
| DB isolation | transactional rollback | Open txn, never commit |
| Contract test | Pact, consumer-driven | Independent deploy, no E2E |
| E2E | few + critical path; never sleep | Auto-wait (Playwright) |
| Property test | invariant + shrink (Hypothesis) | Finds edge cases you forgot |
| Mutation test | kill mutants | Truer than coverage |
| Coverage | line < branch < path | A floor, not a goal |
| Flaky causes | **TORN** | Time/Order/Random/Network |
| Flaky process | detect→quarantine→fix | Never blind-retry |
| Time testing | inject clock / freezegun | Deterministic now() |
| Concurrency | race detector (`-race`) | Proves absence of races |
| Legacy | Feathers: characterize + seams | Dependency-breaking |
| CI order | cheap-first, fail fast | lint→types→unit→integ→e2e |
| Payments | idempotency + partial-failure | Don't lose money on retry |
| Chaos | Netflix Chaos Monkey | Test failure, not just correctness |

### Most Important Concepts

1. **Shift left** — bugs cost ~10× more per stage; catch them early.
2. **Test pyramid** — many unit, few E2E; avoid the ice-cream cone.
3. **AAA + FIRST** — the anatomy of a trustworthy unit test.
4. **Five doubles, used precisely** — stub returns, mock asserts, fake runs.
5. **Mock at the boundary** — avoid the over-mocking trap; prefer state testing.
6. **TDD red-green-refactor** — design emerges, stays minimal.
7. **Contract testing (Pact)** — independent microservice deployment.
8. **Coverage is a floor; mutation testing is the truth.**
9. **TORN** — the four causes of flakiness; never blind-retry.
10. **Idempotency + partial-failure** — the real test of any money/critical flow.

---
