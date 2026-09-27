# ICP Prospect Finder — Claude Skill

**Turn an Ideal Customer Profile into a scored, outreach-ready prospect list using only public web data.**

Describe who you want to reach (industry, company size, location, decision-maker title) and this skill finds matching businesses, identifies the right person to contact, checks how to reach them, and ranks every prospect by fit.

---

## Why I built this

Finding good-fit leads by hand means hours of Googling, cross-checking LinkedIn, and guessing who the real decision-maker is. This skill automates that research loop inside Claude, so you can go from "I want to reach dental clinic owners in Mumbai" to a prioritized list you can act on.

---

## What it does

- **Finds matching companies** from your ICP (industry, size, geography, decision-maker title)
- **Validates each company** so weak or irrelevant matches are filtered out
- **Identifies the decision-maker** and looks up their LinkedIn profile, with name disambiguation to avoid false matches on common names
- **Falls back to other channels** (WhatsApp, Google Business Profile, Facebook) when LinkedIn isn't available, and gives a clear **Best Contact Method** for each prospect
- **Flags franchise/chain vs independent businesses**, since who makes decisions differs between them
- **Scores every prospect from 1 to 10** for ICP fit, sorts by score, and marks the top ones as priority outreach
- **Remembers previous results** and skips businesses already found in earlier runs, so you never get duplicates
- **Reports honestly.** If it can't find enough strong matches, it tells you the shortfall instead of padding the list with weak fits

---

## How it works

```
Confirm ICP + quantity
        ↓
Search → Collect → Validate → Dedupe → Research decision-maker
        ↓
Find LinkedIn / fallback contact → Score (1–10)
        ↓
Enough strong prospects? ── No → Broaden search (max 3–4 rounds)
        ↓ Yes
Sorted, prioritized prospect list
```

Before running, the skill always confirms how many prospects you want and whether you'd like the results as a chat table or a spreadsheet.

---

## Example

**Input**

> Find 10 independent dental clinic owners in Pune with 1–3 locations.

**Output** *(illustrative sample, fictional data)*

| # | Business | Decision-maker | Type | Best Contact Method | Score | Priority |
|---|----------|----------------|------|--------------------|-------|----------|
| 1 | Smile Studio Dental | Dr. A. Mehta, Owner | Independent | LinkedIn | 9/10 | ⭐ Priority |
| 2 | BrightCare Dental Clinic | Dr. R. Kulkarni, Founder | Independent | WhatsApp (Google Business Profile) | 8/10 | ⭐ Priority |
| 3 | City Dental Hub | Dr. S. Joshi, Director | Chain (3 branches) | LinkedIn | 7/10 | — |

Each prospect also includes the reason for its score and the sources used.

---

## Installation

1. Download or clone this repository.
2. Make sure the skill folder contains `SKILL.md` at its root.
3. Zip the skill folder, or use the packaged `.skill` file.
4. Upload it to Claude through the **Skills** section of Claude's settings (on a plan that supports custom skills).
5. Start a new chat and describe your ICP. The skill triggers automatically.

---

## Usage

Just describe who you're looking for:

- *"Find 15 manufacturing COOs at companies with 50–500 employees in Gujarat."*
- *"Build me a lead list of salon owners in Bengaluru."*
- *"Find independent real estate agencies in Delhi NCR and score them for AI automation fit."*

The skill will ask you to confirm the quantity and output format, then run.

---

## Limitations

- Uses **publicly available web information only**; no paid databases or private data sources
- Results depend on how visible businesses are online; very small or offline businesses may be missed
- Always verify contact details before reaching out

---

## License

**© 2026 Sanjana Kumari. All rights reserved.**

This repository is shared for portfolio and reference purposes only. No permission is granted to copy, modify, distribute, or use this skill, in whole or in part, without written permission from the author.

---

## Author

**Sanjana Kumari**
Builds AI voice agents and workflow automations for businesses.

🔗 [LinkedIn](https://www.linkedin.com/in/sanjana-kumari-7258242a5)

Interested in a custom prospecting setup or automation for your business? Reach out on LinkedIn.
