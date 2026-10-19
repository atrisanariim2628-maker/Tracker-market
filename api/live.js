const RBI_URL = "https://www.rbi.org.in/home.aspx";
const GDP_URL = "https://mospi.gov.in/themes/product/6-gross-domestic-product";
const CPI_URL = "https://mospi.gov.in/themes/product/9-consumer-price-index-cpi";

function cleanText(html) {
  return html
    .replace(/<(script|style|noscript)[^>]*>[\s\S]*?<\/\1>/gi, " ")
    .replace(/<\/(?:td|th|tr|p|div|h[1-6]|li|section|article|br|main|span)>/gi, " ")
    .replace(/<[^>]*>/g, " ")
    .replace(/&nbsp;|&#160;|&#xA0;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&ndash;|&#8211;/gi, "–")
    .replace(/&mdash;|&#8212;/gi, "—")
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&quot;/gi, '"')
    .replace(/&#(\d+);/g, (_, code) => String.fromCharCode(Number(code)))
    .replace(/\s+/g, " ")
    .trim();
}

async function fetchPage(url) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 9000);
  try {
    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        "User-Agent": "IndiaMacroDashboard/1.0 (public data display)",
        "Accept": "text/html,application/xhtml+xml"
      }
    });
    if (!response.ok) throw new Error("Source returned HTTP " + response.status);
    return cleanText(await response.text());
  } finally {
    clearTimeout(timer);
  }
}

function numberAfter(text, label, percent = false) {
  const escaped = label.replace(/[.*+?^()|[\]\\]/g, "\\$&");
  const match = text.match(new RegExp(
    escaped + "\\s*(?:\\|\\s*)?:?\\s*([0-9][0-9,]*(?:\\.[0-9]+)?)" + (percent ? "\\s*%" : ""),
    "i"
  ));
  return match ? Number(match[1].replace(/,/g, "")) : null;
}

function metricAfter(text, label) {
  const index = text.toLowerCase().indexOf(label.toLowerCase());
  if (index < 0) return { value: null, period: null };
  const section = text.slice(index, index + 320);
  const valueMatch = section.match(/([0-9]+(?:\.[0-9]+)?)\s*%/);
  const periodMatch = section.slice(label.length).match(/\(([^()]{1,100})\)/);
  return {
    value: valueMatch ? Number(valueMatch[1]) : null,
    period: periodMatch ? periodMatch[1].trim() : null
  };
}

function firstMatch(text, pattern) {
  const match = text.match(pattern);
  return match ? match[1].trim() : null;
}

module.exports = async function handler(_request, response) {
  response.setHeader("Content-Type", "application/json; charset=utf-8");
  response.setHeader("Cache-Control", "s-maxage=300, stale-while-revalidate=900");
  const checkedAt = new Date().toISOString();

  const [rbiResult, gdpResult, cpiResult] = await Promise.allSettled([
    fetchPage(RBI_URL),
    fetchPage(GDP_URL),
    fetchPage(CPI_URL)
  ]);

  const data = {
    checkedAt,
    sources: {
      rbi: { url: RBI_URL, ok: rbiResult.status === "fulfilled" },
      gdp: { url: GDP_URL, ok: gdpResult.status === "fulfilled" },
      cpi: { url: CPI_URL, ok: cpiResult.status === "fulfilled" }
    },
    rbi: null,
    gdp: null,
    cpi: null
  };

  if (rbiResult.status === "fulfilled") {
    const text = rbiResult.value;
    const start = text.indexOf("Current Rates");
    const end = text.indexOf("Connect 2 Regulate", start);
    const rates = text.slice(start >= 0 ? start : 0, end > start ? end : undefined);
    const marketStart = rates.indexOf("Capital Market");
    const market = rates.slice(marketStart >= 0 ? marketStart : 0);
    const bondRows = Array.from(rates.matchAll(/([0-9]+(?:\.[0-9]+)?%)\s*GS\s*(20\d{2})\s*[:|]\s*([0-9]+(?:\.[0-9]+)?)\s*%/gi));
    const currentYear = new Date().getUTCFullYear();
    const targetMaturity = currentYear + 10;
    const bondRow = bondRows
      .filter((row) => Number(row[2]) >= currentYear + 8)
      .sort((left, right) => Math.abs(Number(left[2]) - targetMaturity) - Math.abs(Number(right[2]) - targetMaturity))[0];
    const gsecLabel = bondRow ? bondRow[1] + " GS " + bondRow[2] : null;
    const gsec = bondRow ? Number(bondRow[3]) : null;
    data.rbi = {
      updated: firstMatch(text, /Website last updated date\s*:\s*([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4})/i),
      fxAsOf: firstMatch(rates, /As at\s+([^)]{1,100})\)/i),
      marketAsOf: firstMatch(market, /\*\s*as on\s+([A-Za-z]+\s+\d{1,2},?\s+\d{4})/i),
      yieldAsOf: firstMatch(rates, /#\s*as on\s+([A-Za-z]+\s+\d{1,2},?\s+\d{4})/i),
      policy: {
        repo: numberAfter(rates, "Policy Repo Rate", true),
        sdf: numberAfter(rates, "Standing Deposit Facility Rate", true),
        msf: numberAfter(rates, "Marginal Standing Facility Rate", true),
        bank: numberAfter(rates, "Bank Rate", true),
        reverseRepo: numberAfter(rates, "Fixed Reverse Repo Rate", true),
        crr: numberAfter(rates, "CRR", true),
        slr: numberAfter(rates, "SLR", true)
      },
      fx: { usdInr: numberAfter(rates, "INR / 1 USD") },
      market: {
        nifty: numberAfter(market, "Nifty 50"),
        sensex: numberAfter(market, "S&P BSE Sensex"),
        gsecLabel,
        gsecYield: gsec
      }
    };
  }

  if (gdpResult.status === "fulfilled") data.gdp = metricAfter(gdpResult.value, "Real GDP growth rate");
  if (cpiResult.status === "fulfilled") data.cpi = metricAfter(cpiResult.value, "Inflation (CPI based)");

  response.status(200).json(data);
};
