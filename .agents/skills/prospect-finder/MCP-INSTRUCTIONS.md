# MCP Instructions — Prospect Finder

## Purpose

Define how Prospect Finder selects and uses MCP/tool capabilities.

MCPs provide capabilities and evidence. Prospect Finder makes prospecting decisions.

These rules must remain:
- **provider-neutral**
- **capability-based**
- **portable across hosts**
- **evidence-driven**
- **cost-conscious**

Never assume a specific MCP, provider, API, endpoint, or tool exists. Use only capabilities actually available.

---

## Core Rules

- Use the minimum number of tools needed for a reliable result.
- Select by capability, not provider or brand.
- Prefer the simplest sufficient capability first.
- Use multiple tools only when they add meaningful verification, coverage, or accuracy.
- Preserve useful source URLs and evidence.
- Never fabricate tool availability, tool results, or missing facts.
- Never expose credentials, tokens, cookies, passwords, or secrets.
- If a capability fails or is unavailable, use the best reasonable fallback.
- Preserve uncertainty when evidence is incomplete or conflicting.
- MCPs must not override Prospect Finder's ICP, qualification, scoring, deduplication, or stopping rules.

---

## Capability Routing

### 1. Web/Search — Discovery

Use web/search for:
- finding candidate companies
- discovering official domains
- locating public sources
- finding public professional profiles
- generating varied search queries

Use snippets mainly for discovery. Verify important claims from the underlying source when practical.

### 2. Apify — Dynamic Actor Discovery & Candidate Extraction

Use Apify dynamic discovery capabilities when:
- structured discovery across specific industries, local business listings, e-commerce/brand platforms, or company databases materially improves candidate coverage
- the user's prompt calls for discovery sources beyond basic web search
- structured list extraction is appropriate for generating candidate pools

Dynamic Selection Protocol:
- Search the Apify Store dynamically using available capabilities when an appropriate Actor is not already known for the requested ICP.
- Evaluate Actors based on relevance to the prompt, geographic coverage, useful output fields, cost/efficiency, reliability, and availability.
- Never hardcode a single Actor for all requests; selection must depend dynamically on the user's prompt.

Candidate Treatment & Separation of Concerns:
- Apify output is strictly candidate data — never automatically qualified prospects.
- Follow SKILL.md for normalization, deduplication (against master list and current run), and qualification rules before proceeding to validation and research.
- Maintain clear boundaries: Apify discovers candidate listings and official domains; Firecrawl enriches official websites (`Apify discovery → official domain → Firecrawl website enrichment`).
- If Apify fails, rate-limits, or is unavailable, seamlessly revert to standard web/Maps search.

### 3. Maps — Local Business Verification

Use Maps when relevant to:
- discover local businesses
- verify business identity or physical presence
- verify address, phone, rating, reviews, or operational status
- identify branches/multiple locations
- distinguish independent businesses from franchises/chains
- verify requested geography

Do not use Maps for purely web-based companies or when it adds no useful evidence.

### 4. Firecrawl — Website Research

Use website-extraction capabilities when:
- an official domain is identified
- structured website extraction is needed
- multiple relevant pages need research
- services, team, locations, booking, technology, or website signals need verification

Use the lightest sufficient depth:
1. Homepage/targeted page extraction.
2. Targeted priority pages.
3. Site map + selected pages.
4. Full crawl only when genuinely necessary.

Do not deep-crawl every prospect.

### 5. Playwright/Browser — Interactive Research

Use browser automation when:
- a page requires clicking, typing, scrolling, navigation, or interaction
- content is dynamically rendered and normal extraction is insufficient
- important public information is exposed only through browser interaction
- interactive search-engine research is needed
- a public professional profile needs browser-based inspection
- public LinkedIn research requires opening/navigating public pages
- cross-checking requires interaction with multiple public pages

Do not use browser automation merely because it is available.

Never use browser automation to bypass:
- authentication
- CAPTCHAs
- access controls
- paywalls
- private accounts
- other technical restrictions

Use only legitimately accessible public information.

---

## Public LinkedIn / Professional-Profile Research

- Use public search/browser capabilities only.
- Never log into LinkedIn.
- Never use private, connection-only, or login-only information.
- Never bypass access controls or anti-bot protections.
- Search using combinations such as `person + company`, `person + role`, or `company + LinkedIn`.
- When a public profile can be opened, inspect only publicly visible information.
- Cross-check identity using name, company, role/title, geography, and other useful public context.
- A matching name alone is not sufficient.
- A search-engine snippet is indexed evidence, not direct profile verification.
- Information directly visible on a public profile may support a **VERIFIED FACT** for that specific information.
- If identity matching is incomplete, label the profile **Likely Match**, not **Verified**.
- Never construct or guess a LinkedIn URL.
- If no reliable profile is found, report **Not publicly found** and use another public contact channel when available.

---

## Research Escalation

**Default sequence:**
> `Web/Search` + `Apify` (when useful for candidate discovery) → `Maps` (when locally relevant) → `Firecrawl` (for website enrichment) → `Playwright` (for interactive/dynamic/profile research)

- Escalate only when the current source cannot reliably answer the required question.
- Do not invoke every connected MCP for every prospect.

---

## Source Priority

Prefer:
1. Existing user/dataset information
2. Official company source
3. Government/official source
4. Authoritative directory/database
5. Reputable industry source
6. Public professional/social profile
7. Secondary source/aggregator
8. Search snippet

Use corroboration when identity, ownership, branch count, or another important claim is material.

---

## Evidence Handling

For important information preserve:
- value
- source URL
- supporting context/snippet when available
- confidence/status

Classify evidence strictly using the authoritative definitions in SKILL.md (**VERIFIED FACT**, **ESTIMATED**, **INFERENCE**, **UNKNOWN / NOT FOUND**). Never present an inference or qualitative assessment as a verified fact merely because it is derived from factual tool output.

Never upgrade weak evidence into a verified fact.

**Remember:**
- direct page evidence ≠ search snippet
- search snippet ≠ full-profile identity proof
- third-party listing ≠ first-party confirmation
- inference ≠ fact

When sources conflict:
1. Check entity identity.
2. Prefer authoritative/current evidence.
3. Corroborate when material.
4. Preserve unresolved uncertainty.

---

## Decision-Maker Research

MCPs discover and retrieve candidate profile evidence; Prospect Finder evaluates decision-maker hierarchy and qualification following the authoritative rules in SKILL.md.

MCP role:
- Extract publicly visible names, roles, and profile evidence.
- Never log in, bypass anti-bot protections, or guess profile URLs.
- Distinguish indexed search snippets from direct profile verification.
- Provide supporting source URLs and context snippets for verification.
- Follow SKILL.md to distinguish owners/founders/directors from ordinary employees or associated personnel.

---

## Fallback and Failure Handling

If a preferred capability is unavailable, fails, times out, or is rate-limited:
- Do not repeatedly retry a known failure.
- Use the best available alternative.
- Continue unaffected research.
- Mark missing information **UNKNOWN / NOT FOUND**.
- Preserve material limitations.

**Examples:**
- **Apify unavailable or fails** → standard web search + Maps discovery; continue research loop without stopping or fabricating data
- **Maps unavailable** → official website + public web
- **Firecrawl unavailable** → page retrieval/search/browser as appropriate
- **Browser unavailable** → public search/page retrieval; mark unverified information clearly
- **LinkedIn unavailable** → other public professional/company sources

For errors or incomplete results, retry only when useful; otherwise switch capability and preserve uncertainty.

---

## Cost and Efficiency

Optimize for reliable results with the fewest reasonable calls.

Prefer:
- existing information over new searches
- first-party sources over weak aggregators
- targeted extraction over broad scraping
- shallow research before deep research
- one strong call over redundant calls

Before using an intensive capability, ask:
> Can a simpler available source reliably answer this?

If yes, use the simpler source.

---

## Duplicate / Repeated Research Control

Before a new tool call, check current-run/master-list information when applicable.

Avoid:
- exhausted search queries
- repeated page retrieval
- unnecessary re-scraping
- duplicate company/person research
- equivalent MCP calls for the same fact

If more evidence is needed, change the research angle rather than blindly repeating the same call.

---

## Structured Results

Do not pass raw MCP responses directly to the user.

Normalize where practical:
- names
- domains/URLs
- phone numbers
- addresses
- dates
- categories
- confidence/status

Keep useful evidence and remove redundant tool-output noise. Follow Prospect Finder's required output format.

---

## Security and Privacy

Never expose or store in user-visible prospect output:
- API keys
- authentication tokens
- passwords
- session cookies
- private credentials
- secrets

Use only legitimately accessible public information. Never attempt to obtain private or restricted information through bypass methods.

---

## Prospect Finder Responsibility

MCPs support:
- dynamic candidate discovery & extraction
- retrieval
- extraction
- browser interaction
- local-business research
- professional-profile discovery
- verification
- evidence collection

Prospect Finder remains responsible for:
- ICP interpretation
- qualification/exclusions
- decision-maker selection
- scoring/prioritization
- deduplication
- outreach reasoning
- stopping decisions
- final output

---

## Final Rule

> **RIGHT CAPABILITY + RIGHT SOURCE + RIGHT EVIDENCE + RIGHT VALIDATION + LOWEST REASONABLE COST**

Minimize unnecessary tool calls, repeated searches, duplicate retrieval, unsupported claims, unnecessary deep research, and dependence on one provider.
