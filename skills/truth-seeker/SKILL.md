---
name: truth-seeker
description: Maximum Truth Seeking Protocol. Use for complex, critical, or ambiguous questions where accuracy and deep reasoning are more important than speed or cost. Orchestrates multiple models (Gemini, Kimi, Ollama) to cross-verify facts and logic.
---

# Maximum Truth Seeking (MTS) Skill

This skill implements a rigorous cross-verification process to minimize hallucinations and maximize logical depth.

## Protocol Steps

1.  **Selection of High-End Models:**
    *   Initialize a sub-session with `google-gemini-cli/gemini-3-pro-preview`.
    *   Initialize another sub-session with `openrouter/moonshotai/kimi-k2.5`.
    *   *Optional:* Add `ollama/kimi-k2.5` (if installed) or `ollama/qwen3-coder-128k` for a grounded local perspective.

2.  **Parallel Querying:**
    *   Send the identical prompt to all selected models.
    *   Ask them to provide reasoning ("chain of thought") and citations where possible.

3.  **Cross-Examination (The Adversarial Step):**
    *   Take the response from Model A and feed it to Model B.
    *   Ask Model B: "Identify weaknesses, factual errors, or logical gaps in this answer."
    *   Repeat vice-versa.

4.  **Deep Research Integration:**
    *   If models disagree on facts, use `google_search` or `web_fetch` to find primary sources or the latest data.
    *   Use ChatGPT (via browser/CLI if available) for a broad general-knowledge check.

5.  **Final Synthesis:**
    *   Synthesize the consensus into a final response for Enric.
    *   Clearly mark areas of uncertainty or where models continue to disagree.
    *   **Goal:** Reach the highest level of truth seeking.

## When to use this Skill
- Strategic decisions.
- Complex architectural choices in code.
- Philosophical or ethical dilemmas.
- Fact-checking controversial or rapidly changing news.

## Tools to use
- `sessions_spawn`: To create model-specific worker agents.
- `web_fetch` / `web_search`: For grounding in current reality.
- `opencode`: For deep technical verification.
- `openrouter`: Access to the world's best models.

## Credits & Efficiency
- Always use `gemini-3-flash-preview` for the initial triage.
- Only trigger MTS if the complexity justifies the cost.
- Mention to Enric: "Executing Truth-Seeking Protocol using [Models]..."
