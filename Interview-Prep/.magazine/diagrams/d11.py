# Hand-built HTML diagrams for 11-behavioral-leadership.md  (key = md5(ascii)[:12])
D = {}

# ---- STAR method time allocation ----
D["a8728b3d16c8"] = r"""
<div class="fig"><div class="figcap">STAR · Time Allocation per Section</div>
<div class="frow" style="flex-wrap:nowrap;align-items:stretch;gap:6px">
  <div class="node soft" style="flex:1;text-align:center">
    <div class="nt">S</div>
    <div class="ns">Situation<br><b>10–15%</b></div>
  </div>
  <span class="ar" style="align-self:center">→</span>
  <div class="node soft" style="flex:1;text-align:center">
    <div class="nt">T</div>
    <div class="ns">Task<br><b>5–10%</b></div>
  </div>
  <span class="ar" style="align-self:center">→</span>
  <div class="node acc" style="flex:2;text-align:center">
    <div class="nt">A</div>
    <div class="ns">Action<br><b>60–70%</b><br><em>← score here</em></div>
  </div>
  <span class="ar" style="align-self:center">→</span>
  <div class="node soft" style="flex:1;text-align:center">
    <div class="nt">R</div>
    <div class="ns">Result<br><b>15–20%</b><br><em>concrete #s</em></div>
  </div>
</div>
<div class="fignote">Spend 60–70% on <b>Action</b> — that is where interviewers score you. Results must be quantified.</div></div>
"""

# ---- Story Bank Matrix ----
D["5cf693bdfe0c"] = r"""
<div class="fig"><div class="figcap">Story Bank Matrix · Stories × Themes</div>
<div class="matrix" style="grid-template-columns:7em repeat(9,1fr);font-size:0.72em">
  <div class="cell hd">Story</div>
  <div class="cell hd">Lead</div>
  <div class="cell hd">Own</div>
  <div class="cell hd">Conflict</div>
  <div class="cell hd">Xteam</div>
  <div class="cell hd">Ambig</div>
  <div class="cell hd">Mentor</div>
  <div class="cell hd">Impact</div>
  <div class="cell hd">Fail</div>
  <div class="cell hd">LP</div>

  <div class="cell hd">A (Proj X)</div>
  <div class="cell on">✓</div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell"></div>
  <div class="cell">LP2, LP14</div>

  <div class="cell hd">B (Conflict)</div>
  <div class="cell"></div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell"></div><div class="cell on">✓</div>
  <div class="cell">LP13, LP9</div>

  <div class="cell hd">C (Ambig)</div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell"></div>
  <div class="cell">LP3, LP9</div>

  <div class="cell hd">D (Mentor)</div>
  <div class="cell"></div><div class="cell"></div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell on">✓</div><div class="cell"></div>
  <div class="cell">LP6, LP11</div>

  <div class="cell hd">E (Failure)</div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell"></div><div class="cell"></div><div class="cell"></div>
  <div class="cell"></div><div class="cell on">✓</div>
  <div class="cell">LP13, LP8</div>

  <div class="cell hd">F (Big Proj)</div>
  <div class="cell on">✓</div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell"></div>
  <div class="cell">LP1, LP14</div>

  <div class="cell hd">G (Collab)</div>
  <div class="cell"></div><div class="cell"></div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell"></div><div class="cell"></div>
  <div class="cell">LP6, LP11</div>

  <div class="cell hd">H (Screwup)</div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell"></div><div class="cell"></div><div class="cell"></div>
  <div class="cell"></div><div class="cell on">✓</div>
  <div class="cell">LP2, LP5</div>
</div>
<div class="fignote">Each story covers multiple themes — no column &lt; 2 checks; no row = only 1 check.</div></div>
"""

# ---- STAR story card template ----
D["3f3aaa361be5"] = r"""
<div class="fig"><div class="figcap">STAR Story Card · Template</div>
<div class="fcol" style="gap:8px">
  <div class="node soft">
    <div class="nt">Story metadata</div>
    <div class="ns">Name · Company / Role · Year</div>
  </div>
  <div class="tiers" style="align-items:stretch">
    <div class="tier" style="flex:0 0 9em">
      <div class="th">S — Situation</div>
      <div class="fcol" style="padding:6px 4px;gap:4px">
        <span class="chip">2 sentences max</span>
      </div>
    </div>
    <div class="tier" style="flex:0 0 9em">
      <div class="th">T — Task</div>
      <div class="fcol" style="padding:6px 4px;gap:4px">
        <span class="chip">Your specific role</span>
      </div>
    </div>
    <div class="tier" style="flex:1">
      <div class="th">A — Actions (4–6 bullets)</div>
      <div class="fcol" style="padding:6px 4px;gap:4px">
        <span class="chip">• What you did</span>
        <span class="chip">• Why you chose it</span>
        <span class="chip">• How you unblocked</span>
      </div>
    </div>
    <div class="tier" style="flex:0 0 9em">
      <div class="th">R — Result</div>
      <div class="fcol" style="padding:6px 4px;gap:4px">
        <span class="chip">≥ 2 numbers</span>
      </div>
    </div>
  </div>
  <div class="frow" style="flex-wrap:wrap;gap:6px;justify-content:flex-start">
    <span class="chip">☐ Leadership</span><span class="chip">☐ Ownership</span>
    <span class="chip">☐ Conflict</span><span class="chip">☐ Cross-team</span>
    <span class="chip">☐ Ambiguity</span><span class="chip">☐ Mentoring</span>
    <span class="chip">☐ Impact</span><span class="chip">☐ Failure/Learn</span>
    <span class="chip">☐ Bias for Action</span>
  </div>
</div>
<div class="fignote">Fill one card per story. LP coverage field maps each story to Amazon Leadership Principles.</div></div>
"""

# ---- STAR Answer Structure (detailed) ----
D["6fe831590d10"] = r"""
<div class="fig"><div class="figcap">STAR Answer Structure · Full Detail</div>
<div class="stack">
  <div class="stk"><span class="si">10%</span><span class="sn">SITUATION</span><span class="sd">Brief context — when, where, what was at stake?</span></div>
  <div class="stk"><span class="si">10%</span><span class="sn">TASK</span><span class="sd">What was <em>your</em> specific job? (Not the team's — yours.)</span></div>
  <div class="stk hl"><span class="si">60%</span><span class="sn">ACTION</span><span class="sd">What did <em>you</em> do, step by step? Why this approach? Alternatives considered? How did you influence / decide / unblock?</span></div>
  <div class="stk"><span class="si">20%</span><span class="sn">RESULT</span><span class="sd">What happened? <b>Give numbers.</b> What would NOT have happened without you? What did you learn?</span></div>
</div>
<div class="fignote">Never say "we" in the Action section. Never give a result without numbers. Action is 60% of your answer.</div></div>
"""

# ---- Story → Theme mapping grid ----
D["08514ef0c780"] = r"""
<div class="fig"><div class="figcap">Story → Theme Coverage Grid · Goals</div>
<div class="matrix" style="grid-template-columns:6em repeat(8,1fr);font-size:0.75em">
  <div class="cell hd">Theme</div>
  <div class="cell hd">A</div><div class="cell hd">B</div><div class="cell hd">C</div>
  <div class="cell hd">D</div><div class="cell hd">E</div><div class="cell hd">F</div>
  <div class="cell hd">G</div><div class="cell hd">H</div>

  <div class="cell hd">Lead</div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell"></div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell on">✓</div>
  <div class="cell"></div><div class="cell"></div>

  <div class="cell hd">Own</div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell"></div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell"></div><div class="cell on">✓</div>

  <div class="cell hd">Conflict</div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell"></div><div class="cell"></div>

  <div class="cell hd">Xteam</div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell on">✓</div><div class="cell"></div>

  <div class="cell hd">Ambig</div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell on">✓</div>
  <div class="cell"></div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell"></div><div class="cell"></div>

  <div class="cell hd">Mentor</div>
  <div class="cell"></div><div class="cell"></div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell"></div>
  <div class="cell on">✓</div><div class="cell"></div>

  <div class="cell hd">Impact</div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell on">✓</div><div class="cell"></div><div class="cell on">✓</div>
  <div class="cell"></div><div class="cell"></div>

  <div class="cell hd">Fail</div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell"></div><div class="cell on">✓</div><div class="cell"></div>
  <div class="cell"></div><div class="cell on">✓</div>
</div>
<div class="fignote">Goal: no column &lt; 2 checkmarks (story covers ≥ 2 themes); no row = only 1 checkmark (theme has ≥ 2 stories).</div></div>
"""

# ---- Behavioral Scoring Rubric ----
D["ec1c3b52647e"] = r"""
<div class="fig"><div class="figcap">Behavioral Scoring Rubric · 4-Point Scale</div>
<div class="stack">
  <div class="stk hl"><span class="si">4</span><span class="sn">STRONG HIRE</span><span class="sd">Specific + detailed, clearly their own action · multiple metrics in result · demonstrates exact LP · shows learning/growth · appropriate scope for level</span></div>
  <div class="stk"><span class="si">3</span><span class="sn">HIRE</span><span class="sd">Specific situation, clear action · some metrics (could be stronger) · demonstrates theme adequately · appropriate level scope</span></div>
  <div class="stk"><span class="si">2</span><span class="sn">NO HIRE</span><span class="sd">Vague situation or "we did" · no metrics, "it went well" · indirectly related to theme · scope seems low for level</span></div>
  <div class="stk"><span class="si">1</span><span class="sn">STRONG NO HIRE</span><span class="sd">Can't produce a relevant example · blames others · no learning from failures · contradicts the LP (e.g. "customer feedback doesn't matter")</span></div>
</div>
<div class="frow" style="margin-top:10px;gap:8px;flex-wrap:wrap">
  <div class="node soft" style="flex:1;min-width:180px">
    <div class="nt">Senior Engineer</div>
    <div class="ns">cross-team influence · measurable impact</div>
  </div>
  <div class="node soft" style="flex:1;min-width:180px">
    <div class="nt">Staff / Principal</div>
    <div class="ns">org-wide influence · sets direction · drives strategy</div>
  </div>
</div>
<div class="fignote">Score is per-story per-theme. Calibrate expected scope to the level being hired.</div></div>
"""

# ---- Influence Without Authority Playbook ----
D["23d556345c4b"] = r"""
<div class="fig"><div class="figcap">Influence Without Authority · 5-Step Playbook</div>
<div class="fcol" style="gap:6px">
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">1</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">Understand their incentives, not yours</div>
      <div class="ns">"What does success look like for your team this quarter?"</div>
    </div>
  </div>
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">2</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">Find the shared goal</div>
      <div class="ns">"What if we framed it as X — does that serve both teams?"</div>
    </div>
  </div>
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">3</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">Build credibility through data first</div>
      <div class="ns">Write the doc. Run the PoC. Show, don't tell.</div>
    </div>
  </div>
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">4</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">Make it easy to say yes</div>
      <div class="ns">Offer to do the work. Give them the win too.</div>
    </div>
  </div>
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">5</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">Accept the decision if overruled</div>
      <div class="ns">Disagree-and-commit. State your view once, clearly, then execute.</div>
    </div>
  </div>
</div>
<div class="fignote">Authority is earned through data and shared wins — not title. Commit fully once a decision is made.</div></div>
"""

# ---- Disagree-and-Commit Protocol ----
D["e3fd4fe4bcf5"] = r"""
<div class="fig"><div class="figcap">Disagree-and-Commit · 5-Step Protocol</div>
<div class="fcol" style="gap:6px">
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">1</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">State your position once, clearly, with data</div>
      <div class="ns">"Here is my concern and here is the evidence."</div>
    </div>
  </div>
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">2</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">Make sure they heard it</div>
      <div class="ns">"I want to make sure I'm being clear — my concern is X."</div>
    </div>
  </div>
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">3</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">Ask to understand their decision</div>
      <div class="ns">"Help me understand what I might be missing."</div>
    </div>
  </div>
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">4</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">If they decide differently, commit fully</div>
      <div class="ns">"I understand. I'll execute this and make it work."</div>
    </div>
  </div>
  <div class="frow sb" style="flex-wrap:nowrap;align-items:flex-start;gap:8px">
    <div class="node acc" style="min-width:2.2em;text-align:center;flex-shrink:0"><div class="nt">5</div></div>
    <div class="node soft" style="flex:1">
      <div class="nt">Document your disagreement privately</div>
      <div class="ns">Keep your own notes. If things go as predicted, revisit professionally.</div>
    </div>
  </div>
</div>
<div class="callout c-warn" style="margin-top:10px">
  <div class="ch">✗ What NOT to do</div>
  <p>Raise it publicly · Go silent / passive-aggressively not-do-the-work · Relitigate at every meeting · Tell your team "I don't agree but we have to do it"</p>
</div>
<div class="fignote">State your view once with data, then execute with full commitment if overruled.</div></div>
"""

# ---- Quick Reference Summary ----
D["3add8449ba47"] = r"""
<div class="fig"><div class="figcap">Behavioral Leadership · Quick Reference</div>
<div class="fcol" style="gap:8px">
  <div class="callout c-key">
    <div class="ch">◆ STAR Formula</div>
    <p>Situation → Task → <b>Action (60%)</b> → Result (numbers)<br>
    3-number rule: <b>Before → Change → Scale</b></p>
  </div>
  <div class="callout c-ana">
    <div class="ch">◆ Story Bank</div>
    <p>6–8 stories × 8 themes matrix. No story covers &lt; 2 themes. No theme has &lt; 2 stories.</p>
  </div>
  <div class="callout c-take">
    <div class="ch">◆ Amazon LPs · 4 Buckets</div>
    <p>
      <b>Customer:</b> Obsession · Ownership · Think Big · Invent+Simplify<br>
      <b>Quality:</b> Are Right · Dive Deep · High Standards · Deliver Results<br>
      <b>People:</b> Hire+Develop · Earn Trust · Learn+Curious · Best Employer<br>
      <b>Judgment:</b> Bias for Action · Backbone · Frugality · Broad Responsibility
    </p>
  </div>
  <div class="frow" style="gap:8px;flex-wrap:wrap">
    <div class="node soft" style="flex:1;min-width:150px">
      <div class="nt">Influence w/o Authority</div>
      <div class="ns">Incentives → shared goal → credibility → make easy → commit</div>
    </div>
    <div class="node soft" style="flex:1;min-width:150px">
      <div class="nt">Disagree-and-Commit</div>
      <div class="ns">State once + data → understand their view → commit fully if overruled</div>
    </div>
    <div class="node soft" style="flex:1;min-width:150px">
      <div class="nt">Senior+ Scope</div>
      <div class="ns">Cross-team influence + measurable business impact<br>Staff+: org-level leverage</div>
    </div>
  </div>
  <div class="callout c-warn">
    <div class="ch">✗ Never</div>
    <p>Say "we" in Action · Give result without numbers · Present a "failure" that isn't actually a failure</p>
  </div>
</div>
<div class="fignote">All 9 LPs map to one of 4 buckets — use this to quickly recall which story addresses which principle.</div></div>
"""
