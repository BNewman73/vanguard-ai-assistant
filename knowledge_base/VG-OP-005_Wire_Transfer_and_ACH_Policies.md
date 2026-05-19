# VG-OP-005 — Wire Transfer and ACH Policies

| Field | Value |
|---|---|
| Document ID | VG-OP-005 |
| Version | v6.4 |
| Effective Date | February 1, 2026 |
| Last Reviewed | January 22, 2026 |
| Owner | Vanguard Banking Operations / Compliance |
| Distribution | Public |

> *Synthetic training content — not for distribution. For RAG training/educational purposes only.*

## 1. Purpose

This document covers Vanguard's policies for moving cash between bank accounts and Vanguard accounts via Automated Clearing House (ACH) and wire transfer, including timing, limits, fees, and fraud-prevention controls.

## 2. ACH Policies

### 2.1 What Is ACH?

ACH (Automated Clearing House) is the U.S. electronic funds transfer network used for direct deposit, recurring payroll, online bill pay, and most retail bank-to-investment transfers. Settlement is batched, not real-time.

### 2.2 ACH Timing

| Direction | Standard Timeframe | Funds Available for Trading |
|---|---|---|
| Bank → Vanguard (incoming) | 1–2 business days | Day 0 (immediately, on most accounts) |
| Vanguard → Bank (outgoing) | 1–2 business days | After 2-day hold release |

Settlements occur Mon–Fri, excluding federal holidays. Cutoff for same-day initiation: 4:00 PM ET. Requests after cutoff are processed the next business day.

### 2.3 ACH Limits

| Type | Limit | Notes |
|---|---|---|
| Incoming (Bank → Vanguard) | $250,000 per day | Higher limits available for verified high-balance clients on request |
| Outgoing (Vanguard → Bank) | **$100,000 per day** | Higher amounts must use wire |
| Per linked external bank | 5 active links | Inactive links may be removed |

### 2.4 ACH Fees

ACH transfers are **free** in both directions. Vanguard does not charge fees for ACH initiation or receipt.

### 2.5 Linking a Bank Account

Methods:
1. **Instant verification** via Plaid or Yodlee — login with online-banking credentials; usable within minutes.
2. **Trial deposits** — Vanguard sends two micro-deposits (under $1.00 each) to the external bank within 1–3 business days; user verifies the amounts to complete linking.
3. **Voided check upload** — manual review; 3–5 business days to activate.

Bank-account ownership must match the Vanguard account ownership (same name(s) on file). Third-party transfers are not permitted via ACH; see Section 4.

## 3. Wire Transfer Policies

### 3.1 Timing

| Type | Initiation Cutoff | Funds Available |
|---|---|---|
| Incoming domestic wire | Anytime (settles same business day) | Same business day |
| Outgoing domestic wire | 2:00 PM ET (Mon–Fri) | Same business day |
| Outgoing international wire | 12:00 PM ET (Mon–Fri) | 2–5 business days |

### 3.2 Wire Limits

- Domestic outgoing: no Vanguard-imposed daily limit, but bank-side limits and verification holds apply.
- International outgoing: $1,000,000 per request (additional limits may apply per country).

### 3.3 Wire Fees

| Type | Vanguard Fee |
|---|---:|
| Incoming wire (domestic or international) | $0 |
| Outgoing domestic wire | $10 (waived for Flagship and Personal Advisor Wealth Management clients) |
| Outgoing international wire | $25 (plus correspondent bank fees, if any) |

The receiving bank may charge inbound fees not controlled by Vanguard.

### 3.4 Wire Fraud Callback Requirement

For all outgoing wires of **$50,000 or more**, Vanguard requires a verbal callback confirmation:

1. Request submitted online or by phone
2. Within 1 hour, a Vanguard agent calls the registered phone number on file
3. Agent verifies identity and confirms wire details (amount, recipient bank, recipient name, account number, purpose)
4. Wire is released only after verbal confirmation

If the callback cannot be completed within 24 hours, the wire request is canceled and must be resubmitted.

For details on additional fraud controls, including transaction-monitoring rules and red flags that trigger holds, see **VG-OP-011 (Security and Fraud Prevention Policy)**.

### 3.5 Wire Instructions for Sending Money to Vanguard

- **Receiving Bank:** Vanguard Brokerage Settlement Bank
- **Routing (ABA) Number:** 021000089 *(synthetic — example for training)*
- **Beneficiary Bank Account:** [Vanguard's omnibus account number — not published in this document; obtain from Brokerage Services]
- **Further Credit (FFC):** [Your Vanguard account number]
- **For Benefit Of (FBO):** [Your full legal name as on Vanguard records]

## 4. Third-Party Transfers

Vanguard generally does not allow ACH or wire transfers between a Vanguard account and a bank account held by a different individual ("third-party transfers"), to reduce fraud and money-laundering risk. Limited exceptions exist for trusts, estates, and authorized power-of-attorney relationships (see VG-OP-013).

## 5. Standing Instructions and Recurring Transfers

Investors may set up:
- **Recurring contributions** from a linked bank account (weekly, biweekly, monthly, quarterly)
- **Recurring withdrawals** to a linked bank account (e.g., for retirement income)
- **Standing wire instructions** to a pre-approved beneficiary bank account (bypasses callback if pre-verified, with annual re-verification)

Recurring instructions can be modified or canceled online or by phone. Changes to standing wire instructions require a notarized form for security.

## 6. Common Issues and Resolutions

### 6.1 ACH Returned for Insufficient Funds (R01)
- The original transfer is reversed
- Vanguard charges a $20 fee on returned ACH
- Repeated returns may result in temporary or permanent ACH privileges suspension

### 6.2 Mismatched Names on Bank Account
- ACH may be rejected by the receiving bank
- Workaround: re-link the bank with verified ownership documentation, or use a wire transfer

### 6.3 Wire Held Pending Callback
- Caller is the registered owner of record? Confirm wire details verbally
- If you don't answer the callback, the wire is held; resubmit if needed

### 6.4 International Wire Returned by Correspondent Bank
- Common causes: incorrect SWIFT/BIC, sanctioned country, incomplete beneficiary information
- Vanguard will notify you within 3 business days; funds typically returned within 5–10 business days

## 7. Frequently Asked Questions

**Q: Can I do same-day ACH?**
Same-day ACH is available for incoming transfers only; outgoing is next-business-day standard.

**Q: What's the difference between ACH and a wire?**
ACH is batched, free, and limited; wire is real-time, fee-based, and uncapped (subject to verification).

**Q: I sent a wire to the wrong account — can I cancel it?**
Wires are generally final once sent. Vanguard will attempt recall, but recovery is not guaranteed. Always double-check details before confirming.

**Q: Can I receive a wire if I don't have my settlement fund set up?**
Yes — incoming wires are credited to your Vanguard account; if no settlement fund is set up, wires post to the brokerage cash sweep. See VG-PR-007 (Federal Money Market Fund) and VG-OP-009 (Margin and Trading Policies) for cash-handling details.

## 8. Related Documents

- **VG-OP-001** — Account Opening and Types Overview (linking banks at account open)
- **VG-OP-009** — Margin and Trading Policies (settlement and cash sweep)
- **VG-OP-011** — Security and Fraud Prevention Policy (wire callback rationale, transaction monitoring)
- **VG-OP-013** — Trusted Contact and Power of Attorney Policy (third-party authorizations)

## 9. Contact

- **Banking Operations:** 800-555-0199 (Mon–Fri 8 AM–10 PM ET; Sat 9 AM–4 PM ET)
- **Fraud Hotline (24/7):** 800-555-0166
- **Web:** investor.vanguard.com → Transfers & Payments

---

© 2026 The Vanguard Group, Inc. **SYNTHETIC TRAINING CONTENT** — Not for distribution. For RAG training/educational purposes only.
