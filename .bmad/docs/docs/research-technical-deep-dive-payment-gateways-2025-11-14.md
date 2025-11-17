# Technical Deep Dive: Payment Gateway Integration

**Date:** 2025-11-14

## Overview

Choosing a payment provider is a critical decision for a SaaS business. The choice impacts not only the checkout experience but also fundamental operational areas like tax compliance, invoicing, and international sales. This document compares two leading solutions, Stripe and Paddle, focusing on their core models and suitability for a hybrid billing SaaS.

---

## 1. The Core Difference: Payment Processor vs. Merchant of Record (MoR)

This is the most important distinction to understand.

- **Stripe is a Payment Processor:** When you use Stripe, you are selling directly to your customer. Stripe provides the tools to process the payment, but your company is the legal seller. This means **you are responsible** for all the complexities of the sale, including calculating, collecting, and remitting sales taxes (like VAT) in every jurisdiction where you have customers.

- **Paddle is a Merchant of Record (MoR):** When you use Paddle, you sell your product in bulk to Paddle, and **Paddle legally resells it to the end customer**. Paddle becomes the legal seller in the transaction. This means **Paddle is responsible** for handling all sales tax, VAT, fraud liability, and compliance for every transaction, worldwide.

---

## 2. Stripe

- **Model:** Payment Processor
- **Pros:**
  - **Unmatched Flexibility:** Provides a powerful, developer-centric API that offers granular control over every aspect of the payment and subscription lifecycle.
  - **Vast Ecosystem:** Huge number of third-party integrations and extensive documentation.
  - **Modular:** You can pick and choose from a suite of products (Payments, Billing, Tax, Invoicing) to build the exact stack you need.
- **Cons:**
  - **Tax & Compliance Burden:** The biggest drawback. You are legally responsible for global sales tax and VAT. This is a significant and complex operational burden that can involve registering in dozens of countries. While `Stripe Tax` can help calculate taxes, it's an additional cost and you are still responsible for filing and remittance.
  - **Complexity:** The modularity means you often have to integrate and manage several different Stripe products, each with its own pricing.

---

## 3. Paddle

- **Model:** Merchant of Record (MoR)
- **Pros:**
  - **Automated Global Tax & VAT:** This is Paddle's killer feature. It completely abstracts away the nightmare of tax compliance. They handle calculation, collection, and remittance for you, everywhere.
  - **Simplicity:** One platform and one all-inclusive fee for payments, subscriptions, invoicing, taxes, and fraud protection. This massively reduces administrative overhead.
  - **Reduced Liability:** As the MoR, Paddle takes on the liability for chargebacks and tax compliance.
- **Cons:**
  - **Less Flexibility:** The API is less flexible than Stripe's, and the checkout experience is less customizable.
  - **Higher Fee:** The percentage fee (e.g., 5% + $0.50) looks higher than Stripe's base rate (e.g., 2.9% + $0.30), but it's important to remember that Paddle's fee includes services that are add-on costs in the Stripe ecosystem (like subscription management and tax).

---

## 4. Comparison for Hybrid Billing

Both platforms have strong support for the hybrid subscription + usage-based model that we plan to use.

- **Stripe:** With `Stripe Billing`, you can create subscriptions and report metered usage to add usage-based charges to an invoice. This is highly customizable but requires more development work to track and report usage accurately.
- **Paddle:** Also has built-in support for metered billing on top of subscriptions. It is designed specifically for common SaaS use cases and can be easier to get started with, as it's a more integrated system.

---

## 5. Recommendation

The decision boils down to a trade-off: **developer control (Stripe) vs. operational simplicity (Paddle).**

For a large company with a dedicated finance and legal team, the control offered by Stripe might be preferable.

However, for a startup or a lean team, the time and money spent on managing global sales tax, invoicing, and compliance is a massive distraction from the core mission of building a great product. The risk of getting compliance wrong is also significant.

**Recommendation: Start with Paddle.**

The MoR model is a superpower for a new SaaS business. Offloading the entire burden of global tax and compliance is a huge strategic advantage. It allows the team to focus 100% on product and customers. The slightly higher fee is a small price to pay for this level of operational peace of mind. We can always re-evaluate and migrate to Stripe in the future if we scale to a point where the trade-offs change, but Paddle is the superior choice for getting started quickly and safely.
