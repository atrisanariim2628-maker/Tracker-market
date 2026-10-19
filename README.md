# India Macro & Markets Dashboard

This repository contains the original Streamlit source (`tracker.py`) and a self-contained static page (`index.html`) that Vercel can serve.

## Important data note

The figures, dates, tax examples, fund returns, yields, indicator signals, and scenario text are hard-coded sample content copied from the supplied Python file. There is no live NSE/BSE connection or prediction model. Verify any figures against official sources before relying on them.

## Deploy on Vercel

The root `index.html` is a static site and does not need a build command or environment variables. Import this GitHub repository into Vercel and use the repository root as the project root. Vercel will redeploy when commits reach the connected branch.

The original `tracker.py` is retained as the source reference. Vercel Functions do not provide the WebSocket server required to run a Streamlit app directly.

