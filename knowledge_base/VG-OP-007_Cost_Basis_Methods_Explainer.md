# VG-OP-007 — Cost Basis Methods Explainer

| Field | Value |
|---|---|
| Document ID | VG-OP-007 |
| Version | v4.6 |
| Effective Date | February 1, 2026 |
| Last Reviewed | January 22, 2026 |
| Owner | Vanguard Tax Operations / Compliance |
| Distribution | Public |

> *Synthetic training content — not for distribution. For RAG training/educational purposes only.*

## 1. What Is Cost Basis?

Cost basis is the amount you paid for an investment, including reinvested dividends and capital gain distributions. When you sell, your **gain (or loss)** is the difference between sale proceeds and cost basis. Cost basis affects how much tax you owe on a sale — choosing the wrong method can leave thousands of dollars on the table.

This document covers the methods Vanguard supports, how to elect or change them, and how cost basis is reported on Form 1099-B (see VG-OP-010).

## 2. Covered vs Non-Covered Securities

Federal law (the Cost Basis Reporting rules under the Emergency Economic Stabilization Act) requires brokerages to track and report cost basis to the IRS for **covered** securities. Coverage depends on purchase date:

| Security Type | Covered If Acquired On or After |
|---|---|
| Equities (stocks) | January 1, 2011 |
| Mutual fund shares (including ETFs) | January 1, 2012 |
| Less complex bonds, options | January 1, 2014 |
| Complex bonds | January 1, 2016 |

For non-covered securities, Vanguard may track basis at your request, but the IRS does not receive direct broker reporting. **You** are responsible for reporting accurate basis on your tax return.

## 3. Cost Basis Methods Vanguard Supports

### 3.1 First In, First Out (FIFO) — Default for Stocks/ETFs

The oldest shares are sold first. Simple, transparent, but often produces the largest taxable gain in a long-held appreciating position.

**Example:** You bought 100 shares of VTMS at $80 in 2018, then 100 shares at $230 in 2024. Today VTMS is $260. You sell 50 shares.
- Under FIFO: basis = $80/share, gain = $260 - $80 = $180/share = $9,000 gain (long-term)

### 3.2 Last In, First Out (LIFO)

The most recently acquired shares are sold first. Often produces a smaller gain in an appreciating market but may produce a short-term gain (taxed at ordinary income rates) on shares held under a year.

Same example, LIFO: basis = $230/share, gain = $260 - $230 = $30/share = $1,500 gain (long-term, since 2024 lots are now over a year old as of mid-2026).

### 3.3 Highest In, First Out (HIFO)

The lots with the **highest cost basis** are sold first, regardless of acquisition date. Maximizes basis used; minimizes gain. Often produces the smallest tax bill in an appreciating market with multiple lot purchases.

### 3.4 Average Cost — Default for Mutual Funds

Vanguard calculates a single weighted-average basis across all shares of the same fund in the same account. Required for the Average Cost method to apply uniformly. Once you sell shares using Average Cost, you generally must continue with that method for that fund unless you make a formal election to switch (see Section 5).

**Example:** You own 1,000 shares of the Total Stock Market Index Fund (Investor Shares) with a total cost basis of $124,500. Average cost = $124.50/share. If you sell 100 shares for $145/share, your gain is ($145 - $124.50) × 100 = $2,050.

Average Cost is simple and works well for ongoing dollar-cost-averaging contributions, but it does not let you choose specific lots for tax optimization.

### 3.5 Specific Identification (Spec ID)

You designate which exact share lots to sell. Maximum control; usually produces the lowest possible tax bill. Requires designating lots **before** trade settlement (typically by 4:00 PM ET on settlement date).

To use Spec ID at Vanguard:
1. Set the account default to "Specific Identification" before placing trades
2. At trade time (or before settlement), specify lot(s) — by purchase date and number of shares
3. Vanguard mails or e-delivers a written confirmation showing the lots designated

For investors who actively manage taxes (e.g., tax-loss harvesting), Spec ID is the strongest method.

### 3.6 Methods Comparison Table

| Method | Best For | Trade-Off |
|---|---|---|
| FIFO | Simplicity, default for most | May produce largest gain |
| LIFO | Down markets, lots-recently-bought are losers | Less common; not optimal in most appreciation |
| HIFO | Tax minimization without lot-selection effort | Available only on covered securities |
| Average Cost | Mutual fund DCA, simplicity | No lot-level optimization |
| Specific Identification | Active tax management, tax-loss harvesting | Most administrative effort |

## 4. How to View and Change Your Cost Basis Method

### 4.1 View Current Method

Online: **My Accounts → Cost Basis → Method by Holding**.
The method may differ across funds — for example, mutual funds default to Average Cost while ETFs default to FIFO.

### 4.2 Change Method (Pre-Sale)

Before selling shares, you may change the method as often as you want. The new method applies to **future** sales only.

Online: **Cost Basis → Edit Method** for each holding. Changes are immediate.

### 4.3 Change Out of Average Cost

If you've already sold shares from a mutual fund using Average Cost, IRS rules treat that as a binding election. To switch:

1. Submit a written request to Vanguard
2. The change is **prospective** — already-sold lots stay on Average Cost; future purchases can use a different method
3. Existing unsold shares retain their average cost basis — you cannot retroactively re-bucket basis

This restriction is the principal reason careful investors avoid Average Cost on funds where they expect to do tax-loss harvesting.

## 5. Reporting on Form 1099-B

Each sale of a covered security is reported on Form 1099-B with:
- Acquisition date(s)
- Sale date
- Sale proceeds
- Cost basis (per the method used)
- Gain or loss
- Long-term vs short-term classification

For full Form 1099-B detail, see **VG-OP-010 (Tax Document Guide)**.

## 6. Wash Sale Rule

If you sell a security at a loss and purchase the same or "substantially identical" security within 30 days before or after, the loss is **disallowed** and added to the basis of the replacement shares.

Vanguard tracks wash sales **within a single account** for the same security. Cross-account or cross-spouse wash sales are **your responsibility** to track. A common pitfall: selling a fund in a taxable account at a loss while reinvesting dividends in the same fund in an IRA — the IRA purchase triggers a wash sale that **permanently** disallows the loss (you cannot add basis to an IRA holding).

## 7. Distributions and Reinvestment

Reinvested dividend and capital-gain distributions create new lots. Each lot has its own acquisition date and price. This:
- Increases your total cost basis (you've effectively reinvested taxed dollars)
- Creates short-term lots that age into long-term lots over 12 months
- Can complicate Spec ID selection if there are many small lots

## 8. Tax-Loss Harvesting Quick Guide

1. Identify lots with unrealized losses (use Spec ID)
2. Sell those specific lots
3. Buy a similar-but-not-substantially-identical replacement (e.g., sell VTMS, buy V500 — different indices)
4. Wait at least 31 days before buying back the original holding to avoid wash sale
5. Use the realized loss to offset realized gains (and up to $3,000/year of ordinary income)
6. Carry forward any excess losses

Vanguard does not provide tax advice; consult a tax professional. For ongoing tax-loss harvesting at scale, see **VG-OP-008 (Personal Advisor Services Overview)** — the Personal Advisor Wealth Management tier offers managed tax-loss harvesting.

## 9. Frequently Asked Questions

**Q: What's the default method on a new Vanguard account?**
Mutual funds: Average Cost. Stocks/ETFs: FIFO.

**Q: Can I use different methods for different funds?**
Yes. Method is set at the holding level.

**Q: Does Vanguard report cost basis to my state tax authority?**
Federal reporting is automatic via Form 1099-B; state reporting follows whatever your state requires (typically pulled from your federal return).

**Q: Can I change methods for prior tax years?**
Generally no — each year's tax return is filed based on the method in effect when the sales occurred. Amendments are possible but require professional tax help and IRS Form 8949 corrections.

**Q: What happens to cost basis when I gift securities?**
The recipient generally inherits your cost basis (and holding period for long-term/short-term classification) for future gain, with special rules for losses. Keep records of original purchase dates and prices.

**Q: What about inherited securities?**
Inherited securities receive a **stepped-up basis** to fair market value as of the date of death (or alternate valuation date). This often eliminates accumulated capital gains for heirs.

## 10. Related Documents

- **VG-OP-001** — Account Opening and Types Overview
- **VG-OP-008** — Personal Advisor Services Overview (managed tax-loss harvesting)
- **VG-OP-010** — Tax Document Guide (Form 1099-B detail)
- **VG-PR-001** — Total Stock Market Index Fund Prospectus (example of mutual fund cost basis context)

## 11. Contact

- **Tax Reporting Group:** 800-555-0199 (Mon–Fri 8 AM–10 PM ET)
- **Web:** investor.vanguard.com → Cost Basis

---

© 2026 The Vanguard Group, Inc. **SYNTHETIC TRAINING CONTENT** — Not for distribution. For RAG training/educational purposes only.
