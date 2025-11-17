# Research Session: Data Privacy Regulations (GDPR & CCPA/CPRA)

**Date:** 2025-11-14

## Overview

This document provides a high-level overview of two major data privacy regulations relevant to SaaS companies: the EU's General Data Protection Regulation (GDPR) and the California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA). Compliance is not just a legal necessity but also a key factor in building customer trust.

---

## 1. GDPR (General Data Protection Regulation)

- **Applicability:** Applies to any company that processes the personal data of individuals residing in the European Union (EU), regardless of the company's location.
- **Core Principles:**
  - **Lawful Basis for Processing:** You must have a valid legal reason to process data (e.g., user consent, contractual necessity). Consent must be explicit and freely given (opt-in).
  - **Data Minimization:** Collect only the data that is absolutely necessary for a specific, stated purpose.
  - **Privacy by Design & by Default:** Build data protection into the core architecture of your systems and processes.
- **Key User Rights (Data Subject Rights):**
  - **Right to Access:** Users can request a copy of all their personal data you hold.
  - **Right to Erasure ("Right to be Forgotten"):** Users can request that you delete their personal data.
  - **Right to Data Portability:** Users can request their data in a machine-readable format to take to another service.
- **Obligations for SaaS Companies:**
  - **Data Processing Agreements (DPAs):** You must have DPAs with any third-party vendors (sub-processors) that handle user data on your behalf.
  - **Breach Notification:** You must notify data protection authorities of a data breach within 72 hours of becoming aware of it.

---

## 2. CCPA / CPRA (California's Privacy Laws)

- **Applicability:** Applies to for-profit businesses that collect personal data from California residents and meet certain revenue or data processing thresholds.
- **Core Principles:**
  - **Broad Definition of Personal Information:** Includes a very wide range of data that can be linked to a household or individual.
  - **"Sale" and "Sharing" of Data:** Has a broad definition that includes sharing data for targeted advertising.
- **Key User Rights:**
  - **Right to Know:** Users can request to know what personal information is being collected about them and whether it's sold or shared.
  - **Right to Delete:** Similar to GDPR's Right to Erasure.
  - **Right to Opt-Out:** Users have the right to opt out of the sale or sharing of their personal information.
- **Obligations for SaaS Companies:**
  - **"Do Not Sell or Share My Personal Information" Link:** Must be provided on the website homepage.
  - **Honor Opt-Out Signals:** Must respect signals from browsers or plugins, like the Global Privacy Control (GPC).
  - **Limits on Use of Sensitive Personal Information:** Users can limit the use and disclosure of sensitive data (e.g., passwords, precise geolocation).

---

## 3. Practical Compliance Checklist for a New Project

This is a starting point for building a compliant SaaS product.

1.  **Data Mapping:**
    - [ ] Identify and document every piece of personal data you plan to collect.
    - [ ] For each piece, document *why* you need it, *where* it will be stored, and *how long* you will keep it.

2.  **Develop a Clear Privacy Policy:**
    - [ ] Write a comprehensive but easy-to-understand privacy policy.
    - [ ] Clearly state what data you collect, your legal basis for collecting it, and how users can exercise their rights.

3.  **Implement "Privacy by Design":**
    - [ ] Build features that allow users to manage their privacy settings.
    - [ ] Ensure security measures like encryption (in transit and at rest) and access controls are in place from day one.

4.  **Establish a Consent Management System:**
    - [ ] Implement a clear process for obtaining and recording user consent (opt-in).
    - [ ] Make it just as easy for users to withdraw consent as it is to give it.

5.  **Vet Third-Party Vendors:**
    - [ ] Create a list of all third-party services you will use (e.g., analytics, cloud hosting, email providers).
    - [ ] Ensure they are all GDPR/CCPA compliant and sign Data Processing Agreements (DPAs) with them.

6.  **Create a User Rights Workflow:**
    - [ ] Design a process for handling user requests for access, deletion, or portability of their data.
    - [ ] This could be a manual email-based process to start, but should be reliable and able to meet the 30-day response deadline.

7.  **Plan for Data Breaches:**
    - [ ] Create a simple incident response plan that outlines the steps to take if a data breach occurs, including the 72-hour notification requirement.
