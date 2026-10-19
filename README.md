# India Macro & Markets Dashboard

Vercel serves the dashboard from `index.html` and its live-data endpoint from `api/live.js`. The original Streamlit file, `tracker.py`, remains in the repository as the supplied source.

## Data feeds

- RBI current rates page: policy rates, reserve ratios, the FBIL USD/INR reference rate, selected government-security yields, and the latest published Nifty/Sensex values.
- MoSPI product pages: latest real GDP growth rate and CPI-based inflation.
- TradingView widgets: Nifty 50 and USD/INR charts. Exchange data may be delayed depending on market-data permissions.

The browser checks the endpoint on page load and every five minutes. The endpoint caches source responses for five minutes and includes the publisher's dates where available. RBI figures are published at different frequencies; USD/INR is a daily reference rate, GDP is quarterly, and CPI is monthly. This is not a tick-by-tick trading feed.

When a source is unavailable or its value cannot be parsed, the dashboard shows “Unavailable” rather than falling back to sample numbers. The tax, mutual-fund category-return and scenario examples from the original page were removed; links point to the relevant official references instead.

No API keys or environment variables are required for these public pages. For licensed real-time NSE data or live user-specific fund returns, connect an authorized provider and its credentials separately.

## Deploy on Vercel

Connect this repository to Vercel with the project root set to the repository root. Vercel serves `index.html` and deploys `api/live.js` as a serverless function. New commits to the connected branch trigger deployments.
