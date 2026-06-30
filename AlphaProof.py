# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class AlphaProof(gl.Contract):
    signals: TreeMap[str, str]        
    parsed_targets: TreeMap[str, str]  
    verdicts: TreeMap[str, str]        

    def __init__(self):
        # GenVM requires explicit memory allocation during initialization
        self.signals = TreeMap()
        self.parsed_targets = TreeMap()
        self.verdicts = TreeMap()

    @gl.public.write
    def submit_signal(self, signal_id: str, post_url: str) -> None:
        """Phase 1: Fetches a social media post and extracts the trade parameters."""
        def get_post() -> str:
            # Safely fetch raw text from the unstructured social media post
            return gl.nondet.web.render(post_url, mode="text")

        # First AI Consensus: Information Extraction
        extracted = gl.eq_principle.prompt_non_comparative(
            get_post,
            task="Extract the trading parameters: Asset, Entry Price, Take Profit (TP), and Stop Loss (SL) from the text.",
            criteria="Output MUST be a strict JSON string with keys: Asset, Entry, TP, SL. Do not return any other text."
        )
        
        # Store the extracted parameters on-chain
        self.signals[signal_id] = post_url
        self.parsed_targets[signal_id] = extracted
        self.verdicts[signal_id] = "PENDING"

    @gl.public.write
    def adjudicate_trade(self, signal_id: str, chart_url: str) -> None:
        """Phase 2: Evaluates the stored parameters against live historical market data."""
        targets = self.parsed_targets.get(signal_id, "")
        if targets == "":
            return

        def get_market_data() -> str:
            # Fetch raw historical price action data natively
            chart = gl.nondet.web.render(chart_url, mode="text")
            return f"TARGETS:\n{targets}\n\nCHART DATA:\n{chart[:2000]}"

        # Second AI Consensus: Data Adjudication
        verdict = gl.eq_principle.prompt_non_comparative(
            get_market_data,
            task="Evaluate the historical chart data against the targets. Determine if the price hit the Take Profit (TP) before the Stop Loss (SL).",
            criteria="Output must be exactly PROFITABLE, STOPPED_OUT, or PENDING."
        )
        
        self.verdicts[signal_id] = verdict

    @gl.public.view
    def get_verdict(self, signal_id: str) -> str:
        """View function to check the final outcome of the trade call."""
        return self.verdicts.get(signal_id, "UNREGISTERED")
