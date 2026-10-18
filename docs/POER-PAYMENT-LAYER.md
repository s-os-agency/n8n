# Poer Sales Engine — Payment & Broker-Fee Layer (v1)

## Model
Broker-fee only. We do not collect the car price. Title transfer happens directly between buyer and seller through normal RTA / Absher channels. Our revenue is a flat broker fee or agreed spread, captured via Ziina.

## Gateway: Ziina (Z-I-I-N-A)
- Dubai-based, Central Bank of UAE licensed Stored Value Facility.
- Receiving payments: 2.6% + 1 AED per transaction (UAE cards). +1.5% for international cards or non-AED currency.
- No setup fee, no monthly fee, no subscription. First 1,000 AED received is free.
- Settlement: instant to Ziina wallet; 1-2 business days to UAE bank account; often same-day for eligible users.
- Onboarding: minutes, Emirates ID. Supports Apple Pay, Google Pay, Visa, Mastercard, Amex, payment links, QR, Tap to Pay, hosted gateway API.
- Ten currencies accepted, all settle in AED.
- Arabic and English local support.
- Cash-out to bank: free (Ziina side); ~1 AED bank fee may apply from 8 Jan 2026.

## Why Ziina over Telr for v1
- Zero monthly burn while volume is near zero. Telr's advantage only appears above ~25,000 AED/month volume where tiered rates drop to 2.35%.
- Payment-link flow is native to WhatsApp — where UAE car deals actually close.
- Instant wallet settlement suits a broker testing market fit.

## Flow
1. Velocity signal flags a hot listing (Carapis weekly diff).
2. Agent pitches to buyers in pipeline; broker fee agreed (flat or % of listing).
3. Ziina payment link sent via WhatsApp / email.
4. Buyer pays fee. Webhook confirms. Fee lands in Ziina wallet.
5. Broker coordinates title transfer between buyer and seller (RTA Dubai / Absher) — no gateway involvement.
6. Settlement: cash out to merchant/escrow bank account in 1-2 business days.

## Env vars (private, never in repo)
ZIINA_API_KEY=
ZIINA_MERCHANT_ID=
ZIINA_WEBHOOK_SECRET=
ZIINA_SETTLEMENT_ACCOUNT=

## Open items
- Ziina business account KYC (Emirates ID + trade license).
- Webhook endpoint on n8n for payment confirmation.
- Fee schedule per vehicle segment (SUV / sedan / luxury).
- Chargeback / refund policy for broker fees.
