# India Macro & Markets Dashboard

Vercel serves the dashboard from `index.html` and its data endpoint from `api/live.js`. The original Streamlit file, `tracker.py`, remains in the repository as the supplied source.

## Data sources and coverage

- RBI current rates page: policy rates, reserve ratios, the FBIL USD/INR reference rate, government-security yields, and the latest published Nifty/Sensex values.
- MoSPI GDP and CPI pages: the endpoint requests these official pages, but their headline values are rendered through interactive page widgets that the serverless parser cannot read. The dashboard shows “Unavailable” for those two cards and links directly to the current MoSPI pages instead of showing old examples.
- TradingView charts: USD/INR and India 10-year government-bond yield are embedded; the Nifty chart links to TradingView because its index cannot be embedded in this page.

The browser requests data on page load and every five minutes. The endpoint caches source responses for five minutes and shows publisher dates where available. RBI figures have different update schedules; USD/INR is a daily reference rate, GDP is quarterly, and CPI is monthly. This is not a tick-by-tick NSE feed.

The old tax examples, mutual-fund category-return averages, indicator samples, and scenario text were removed. Links point to the relevant official references instead.

No API keys or environment variables are required for the RBI data. Licensed real-time NSE data or user-specific fund returns require an authorized provider and credentials.

## Deploy on Vercel

Connect this repository to Vercel with the project root set to the repository root. Vercel serves `index.html` and deploys `api/live.js` as a serverless function. New commits to the connected branch trigger deployments.
