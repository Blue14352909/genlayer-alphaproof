# genlayer-alphaproof
# AlphaProof: Trustless Trade Signal Adjudicator 🧠⚖️

**AlphaProof** is an Intelligent Contract built on the GenLayer protocol. It solves a critical accountability problem in Web3 social finance: the inability to trustlessly verify natural-language market predictions. 

By utilizing the GenLayer Virtual Machine (GenVM) and Optimistic AI Consensus, AlphaProof reads unstructured social media posts, locks the risk parameters on-chain, and later adjudicates the trade outcome against live historical market data.

---

## 🛑 The Problem
Content creators and "crypto gurus" routinely delete losing trade setups, manipulate screenshots, and distort their actual win rates. Currently, there is zero decentralized infrastructure capable of reading a natural-language prediction, extracting its parameters, and objectively verifying the outcome on-chain without relying on a centralized intermediary or oracle.

## 💡 The Solution: A Two-Phase AI Lifecycle
AlphaProof rejects the "single-call wrapper" design. Instead, it implements a multi-stage state machine that manages data across time.

### Phase 1: Data Extraction (`submit_signal`)
When a prediction is made, the contract captures it immediately.
1. **Web Fetching:** Uses `gl.nondet.web.render` to natively pull the raw, unstructured text of the social media post.
2. **AI Consensus:** The validator set parses the natural language and extracts a strict JSON payload containing the Asset, Entry Price, Take Profit (TP), and Stop Loss (SL).
3. **State Lock:** The extracted parameters are locked immutably into a `TreeMap` before the market outcome is known.

### Phase 2: Market Adjudication (`adjudicate_trade`)
Days or weeks later, the market renders its verdict.
1. **Historical Data:** The contract fetches raw price action data from an open market API.
2. **AI Evaluation:** A second, independent consensus pass evaluates the locked targets against the live chart data.
3. **Final Verdict:** The AI determines an absolute truth—did the price hit the Take Profit before the Stop Loss?—and permanently updates the state to `PROFITABLE` or `STOPPED_OUT`.

---

## ⚙️ GenLayer Mechanics Under the Hood
This Intelligent Contract demonstrates advanced GenLayer capabilities:
*   **Python / GenVM SDK:** Written entirely in Python, utilizing GenVM's robust execution environment.
*   **Non-Deterministic Web Access:** Bypasses traditional oracles by directly fetching web data.
*   **Equivalence Principle:** Uses `prompt_non_comparative` primitives to reach consensus on subjective data extraction and historical chart analysis.
*   **Persistent State Management:** Utilizes `TreeMap` to track the lifecycle of multiple independent signals over time.

---

## 🚀 Ecosystem Impact
AlphaProof is a composable data-layer primitive. Its architecture enables:
*   **Decentralized Hedge Funds:** Algorithmically rank signal providers by real, on-chain performance rather than self-reported win rates.
*   **Trustless Copy-Trading:** Capital only follows wallets with a cryptographically provable track record enforced by the contract itself.

---

## 🛠️ Deployment & Testing
This contract is designed to be deployed and tested using **GenLayer Studio** or the **GenLayer CLI**.

1. Deploy `AlphaProof.py` using the GenVM environment.
2. Call `submit_signal(signal_id, post_url)` using a raw text URL (e.g., a Pastebin link of a trade call).
3. Call `adjudicate_trade(signal_id, chart_url)` using a raw text URL of historical market data.
4. Call `get_verdict(signal_id)` to view the final, trustless outcome.
