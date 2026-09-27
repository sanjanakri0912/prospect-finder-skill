name: icp-prospect-finder

description: Identify companies and decision-makers that match a user-provided Ideal Customer Profile (ICP) using public web information, optional Apify MCP dynamic discovery, optional Maps MCP verification, optional Firecrawl MCP enrichment, and optional Playwright MCP browser research. Use this skill whenever the user describes an ICP or asks to find/build a prospect list, target companies, or leads matching criteria like industry, company size, geography, or decision-maker title (e.g. "find manufacturing COOs at 50-500 employee companies," "find dental clinic owners in Bangalore," "find fashion brands in India," "build me a lead list"). Also trigger for requests to research a batch of companies for outreach, score prospects, or identify AI/automation opportunities at target companies. Do not use for researching a single already-named company (just research it directly) or for anything requiring private/paid data sources — this skill is public-web-only.

---

# ICP Prospect Finder

A B2B prospect intelligence workflow: takes a user's Ideal Customer Profile (ICP), searches the public web and optional Apify dynamic discovery capabilities, collects candidate companies, deduplicates against master list and current run, verifies locations via Maps MCP (when relevant), validates fit, enriches website data using Firecrawl MCP (when available), uses Playwright for interactive/public-profile research when needed, identifies decision-makers, researches each one, scores fit, and produces outreach-ready intelligence. **Accuracy over quantity — never fabricate.**

> [!NOTE]

MCP Integration: Refer to MCP-INSTRUCTIONS.md for provider-neutral capability selection, fallback policies, research depth, cost efficiency, and evidence handling. Apify, Maps, Firecrawl, and Playwright are optional capabilities; use them only when relevant. If a preferred MCP is unavailable or fails, continue with another suitable public research capability without fabricating data.

## MCP capability routing (short form)

Apify: optional dynamic discovery and candidate extraction across industries, business types, e-commerce brands, local businesses, or niche markets based on the user prompt; searches the Apify Store dynamically when a suitable Actor is unknown.

Maps: local business discovery/verification, address, branches, physical presence, and independent vs. franchise checks.

Firecrawl: official website extraction, structured enrichment, and targeted/deep website research after the correct domain is identified.

Playwright: interactive/dynamic webpages, browser navigation, search-engine research, and publicly accessible professional/LinkedIn profile research. Never log into LinkedIn or access private/login-only information.

Routing: use the least complex sufficient capability; do not invoke every MCP for every prospect. Escalate only when the current source cannot reliably answer the required question.

Follow the detailed capability/fallback rules in MCP-INSTRUCTIONS.md; do not hard-code provider-specific behavior elsewhere in the skill.

## Hard rules (apply throughout, no exceptions)

- Never invent companies, people, employee counts, revenue, news, or LinkedIn profiles.

- Every factual claim about a company or person must trace to something actually found via search or page scraping — don't fill gaps with plausible-sounding guesses. Clearly distinguish and label every data point, claim, and conclusion using one of four classifications:

  1. **VERIFIED FACT** — Directly supported by a reliable primary/official source (e.g. "Business offers online appointment booking"). Never label an employee count or employee-count range as **VERIFIED FACT** unless an explicit, reliable public source directly supports that exact count/range.

  2. **ESTIMATED** — A numerical or factual estimate derived from available evidence. Always state the basis. If an employee count or range is derived from indirect evidence (such as number of branches, team size descriptions, LinkedIn company size, organizational scale, or staff listings), ALWAYS label it **ESTIMATED** and explain the basis (e.g. "ESTIMATED: 10-25 employees — based on 3 active clinics with ~3-8 staff per location").

  3. **INFERENCE** — A reasoned conclusion based on one or more verified facts (e.g. "Potential automation opportunity: appointment-handling automation"). Explicitly label every qualitative assessment, qualification judgment, automation opportunity, marketing signal, prospect score rationale, or outreach angle as **INFERENCE** — never convert estimates or reasoned conclusions into **VERIFIED FACT**.

  4. **UNKNOWN / NOT FOUND** — Cannot be reliably established from available public information (say so explicitly, never silently omit the field).

- **Employee Count Evidence Rule**: Never label an employee count or range as **VERIFIED FACT** unless a reliable public source explicitly supports that employee count/range. If derived from number of branches, team size descriptions, LinkedIn company size, organizational scale, or other indirect evidence, label it **ESTIMATED** and explain the basis.

- **Overall Confidence Rule**: Do not label an entire prospect "Verified" when some important fields are only **ESTIMATED** or **INFERENCE**. Overall confidence should reflect the quality of the core prospect identity and evidence while clearly preserving field-level classifications (e.g., `Overall Confidence: High — Core identity/location/website/decision-maker verified; employee count estimated`). Do not downgrade a prospect merely because an employee count is unavailable or estimated.

- Never guess a decision-maker's name. If no named individual can be found, say so and fall back to the company's general contact channel or LinkedIn company page.

- Think through search/validation steps internally; don't narrate the search process to the user — just deliver conclusions and evidence.

## Workflow

### 1. Understand the ICP

Parse what the user gave you for: industry, company size/employee count, revenue (if mentioned), geography, decision-maker title(s), technologies, keywords, exclusions.

Always confirm two things before searching, since they change how the run is scoped:

- **Quantity** — how many prospects to aim for (ask if not specified; don't default silently).

- Anything genuinely ambiguous in the ICP that would send the search in a very different direction (e.g. "manufacturing" spanning many sub-industries) — ask only if it would materially change results, otherwise make a reasonable assumption and state it.

Also determine:

- **Discovery Strategy & Sources Needed** — based on the prompt's industry, company type, geography, and target audience, evaluate which discovery sources are appropriate (public web search, local business/Maps, dynamic Apify discovery, e-commerce/brand discovery, industrial/company discovery, etc.).

- **Apify Discovery Selection** — if an Apify discovery capability would materially improve coverage for the current ICP, identify or dynamically search for a suitable Apify Actor (e.g. searching the Apify Store using the ICP/discovery requirement when a suitable Actor is not already known).

### 2. Check the running master list

Before searching, use `memory_read` to retrieve `/areas/prospect-master-list.md` from the Claude memory filesystem (see "Persistence" below) to see which companies and decision-makers have already been surfaced in past runs. Exclude them from new results unless the user explicitly asks to include previously-shown prospects, or unless the same company qualifies under a genuinely different ICP/sector this time.

### 3. Run the iterative research loop

This is a loop, not a straight line — repeat it until you have enough validated, unique prospects:

```
Search & Apify Discovery (when useful) → Collect Candidate & Domain →

Deduplicate against Master List & Current Run → Maps Verification (when relevant) →

Validate → Firecrawl Website Research (when needed) →

Decision-Maker / LinkedIn Research → AI Opportunity Analysis → Score & Qualify → enough prospects?

                            │

                    No ─────┘→ generate NEW search queries (never repeat an

                                 exhausted one) → loop again

                    Yes → done, move to delivery

```

**Search.** Convert the ICP into multiple varied search queries using standard web search — never rely on one phrasing. Vary industry synonyms, geography phrasing, and role terms (e.g. for "manufacturing companies India": also try "industrial manufacturers India," "precision engineering India," "factory companies India," relevant trade-association/directory searches).

**Apify Dynamic Discovery (Optional Additional Discovery Source).** Integrate Apify as an optional, complementary candidate discovery source alongside web search when it provides useful structured discovery for the current ICP:

- **Core Principle**: Prospect Finder decides WHAT to search for and WHAT qualifies. Apify provides discovery/extraction capabilities. Firecrawl provides website enrichment. Apify must NOT become the intelligence, qualification, scoring, or deduplication layer.

- **1. Determine whether Apify is useful**: After parsing the current prospecting request, evaluate whether an Apify-backed discovery capability would materially improve candidate discovery. Use Apify when it offers a structured discovery capability for the current ICP (e.g., local business discovery for local services/clinics/restaurants; brand/e-commerce discovery for consumer brands; web/company discovery for SaaS/tech/manufacturers). Do not automatically invoke Apify for every request if standard web discovery is already sufficient. The decision depends strictly on the CURRENT USER PROMPT, not on a fixed industry.

- **2. Dynamic Actor Discovery**: Do not hardcode a specific Apify Actor as universal. When a suitable Actor is not already known or available for the current discovery need:
  1. Use available Apify Actor-discovery capabilities to search the Apify Store using the current ICP/discovery requirement.
  2. Identify suitable Actors.
  3. Inspect their capabilities, input parameters, and output fields before executing.
  4. Select the most appropriate Actor based on relevance to the ICP, geographic coverage, useful output fields, reliability, availability, cost/efficiency, and support for structured prospect discovery.
  5. Do not run an Actor merely because it appears in search results, and never invent Actor capabilities.
  6. Re-use a previously verified suitable Actor when available instead of repeatedly searching the store.

- **3. Combine with Existing Discovery**: Apify complements public-web discovery to produce a combined candidate pool (`Existing public-web discovery + Apify discovery when useful = Combined candidate pool`). Do not run identical searches across both sources unnecessarily; assign each source to where it adds unique coverage.

- **4. Candidate-Only Data Treatment**: Treat Apify results strictly as discovery candidates, never as automatically qualified prospects. For every candidate returned by Apify:
  1. Normalize business/company name (strip legal suffixes like LLC, Inc., Pvt Ltd).
  2. Normalize official domain/website URL.
  3. Normalize location.
  4. Capture other available identifiers (phone, address, listing URL, place ID, social URL).
  5. Compare against the master list and current run candidates.
  6. Deduplicate *before* proceeding to verification, Firecrawl enrichment, and decision-maker research.

- **5. Source Validation**: Apify discovery data must be independently validated against official company websites and primary sources. Do not fabricate missing fields. If an Apify field cannot be validated when validation is required, preserve the appropriate confidence status rather than presenting it as a verified fact.

- **6. Firecrawl Relationship**: Do NOT use Apify as a replacement for Firecrawl. Apify discovers candidate listings and official domains; Firecrawl enriches official websites (`Apify discovery → official website identified → Firecrawl website enrichment → Prospect Finder validation/research`). Do not use Apify and Firecrawl redundantly for the same website-research purpose.

- **7. Failure and Fallback**: If Apify is disconnected, unavailable, misconfigured, rate-limited, fails, or no suitable Actor is available: automatically continue using existing web/Maps discovery without stopping the workflow, retrying indefinitely, or inventing results. Report material limitations only if they affect the final output.

- **8. Cost and Efficiency**: Use the minimum necessary Apify capability and runs required for candidate discovery. Do not execute expensive enrichment, review extraction, or contact enrichment Actor features when not required.

- **9. Dynamic Strategy (ICP-Agnostic)**: Generate discovery queries, sources, and Actor selection dynamically from the user's prompt. Never hardcode dental clinics, Google Maps, Justdial, or specific Actors as universal rules.

**Collect Candidate & Domain.** Pull candidate companies and their official domain URLs from web search results and Apify discovery outputs.

**Deduplicate against Master List & Current Run.** Check each discovered candidate against both the persistent master list (step 2) and everything already collected earlier in this same run (normalizing names by stripping legal suffixes like LLC, Inc., Pvt Ltd and comparing root hostnames). Drop repeats immediately — do not carry duplicates into Maps verification, website validation, or enrichment research.

**Maps Verification (Optional Business/Location Verification).** When local-business verification is relevant (business identity, address/location, branches, independent vs. franchise/chain, or local presence), use Maps capabilities for surviving unique candidates.

Compare Maps data with the official website and other reliable sources; first-party evidence wins unresolved conflicts.

Record useful Maps evidence directly into Evidence.

Do not use Maps for purely web-based companies or when it adds no meaningful verification.

If Maps is unavailable, rate-limited, or fails, continue with suitable public web/Firecrawl research; never stop or fabricate.

**Validate.** For each unique candidate, confirm via its website, public listings, or Maps data: industry match, location, approximate size, what it actually does, and that it has a real public presence. Drop anything that clearly doesn't fit — don't include borderline companies just to hit the quantity target. Also determine and note **Independent vs Franchise/Chain** — this changes who the real decision-maker is (a franchise's local contact is usually a manager, not an owner with purchasing authority; note this so the outreach angle isn't written as if to an owner-operator).

**Website Research & Firecrawl Enrichment (10-Phase Protocol).** Once candidate company websites are identified and validated, perform deep website research using Firecrawl MCP (when available) or standard fallback tools. Follow these 10 phases:

#### PHASE 1 — Identify website

- If a prospect has a known official website URL, use it.

- If the official website is unknown, use the standard search/discovery process to identify it.

- Never assume a website belongs to the prospect without verification (e.g. check business name and location on site match candidate).

#### PHASE 2 — Initial Firecrawl scrape

- Use Firecrawl's single-page scrape (`firecrawl_scrape`) first on the prospect's official homepage.

- Extract, when available:

  - Official business name
  - Address & phone & email
  - Founders/owners & decision-makers
  - Products, services, & specialties
  - Number of locations/branches
  - Technology, equipment, & software in use
  - Team & staff information
  - Booking, appointment, & contact options
  - Marketing & customer-acquisition signals (e.g. ad pixels, chat widgets, promo banners)
  - Relevant website metadata
  - Important internal URLs (e.g. /about, /team, /services, /contact)

#### PHASE 3 — Decide whether deeper research is needed

- Do **NOT** crawl or deep-scrape every website automatically.

- Escalate to deeper Firecrawl research only when:

  - The homepage does not contain enough information;
  - Decision-maker information is missing;
  - Branch/location information is unclear or incomplete;
  - Services/specialties need detailed verification;
  - Marketing/customer-acquisition signals need investigation;
  - Multiple relevant internal pages are identified;
  - The prospect appears to be a high-value or qualified prospect.

#### PHASE 4 — Deep research strategy & fallback rules

- **Preferred Tier 1**: Use Firecrawl crawl (`firecrawl_crawl`) when available, appropriate, and supported by API limits.

- **Fallback Tier 2 (HTTP 429 / Tier limits / Rate limits / Failures)**:

  - If `firecrawl_crawl` fails, returns HTTP 429 (rate-limited), is unavailable, or is restricted by the API plan:

    1. Do **NOT** repeatedly retry a rate-limited crawl.

    2. Switch immediately to Firecrawl map (`firecrawl_map`) to discover site structure and internal URLs.

    3. Select only specific, high-priority target pages.

    4. Perform targeted single-page scrapes (`firecrawl_scrape`) on those selected URLs.

- **Priority page targets**: Select target pages dynamically based on the current prompt and ICP.
  - Core general targets: `/about`, `/about-us`, `/our-team`, `/team`, `/leadership`, `/services`, `/solutions`, `/products`, `/locations`, `/branches`, `/contact-us`, `/contact`, `/appointment`, `/booking`, `/schedule`, `/technology`, `/facilities`, and equivalent domain paths.
  - ICP-driven targets:
    - Healthcare ICP → doctors, team, patient-resources, specialties pages may be relevant.
    - SaaS ICP → product, pricing, team, integrations, features pages may be relevant.
    - E-commerce / Fashion ICP → collections, products, about, wholesale pages may be relevant.
    - Manufacturing ICP → products, capabilities, facilities, about pages may be relevant.
  - Keep the generic rules industry-agnostic while tailoring page selection to the active ICP.

#### PHASE 5 — Evidence & classification rules

- Every important claim must be traceable to the exact page/source URL where it was found.

- Apply the Evidence Classification rules defined in the Hard rules section above (**VERIFIED FACT**, **ESTIMATED**, **INFERENCE**, **UNKNOWN / NOT FOUND**). Preserve all four evidence classes strictly; do not convert estimates or reasoned conclusions into **VERIFIED FACT**.

- **Employee Count Rule**: Never label an employee-count range as **VERIFIED FACT** unless a reliable public source explicitly supports that employee count/range. If the range is derived from number of branches, team size descriptions, LinkedIn company size, organizational scale, or other indirect evidence, label it **ESTIMATED** and explain the basis.

- Do **NOT** present qualitative judgments as facts. Judgments such as:

  - high marketing spend
  - aggressive advertising
  - strong customer acquisition
  - likely decision-maker
  - premium positioning
  - high growth

  MUST be explicitly labeled as **INFERENCE** with the supporting evidence provided (e.g., "INFERENCE: Premium positioning — supported by mentions of concierge services and high-end equipment pricing on /services page").

#### PHASE 6 — Decision-maker research

- When the website identifies founders, owners, directors, partners, department heads, or other leadership:

  - Record their full name;
  - Record their specific title/role;
  - Record supporting evidence (e.g. URL and snippet from /team page);
  - Identify a publicly available LinkedIn profile when possible;
  - Do **NOT** claim a LinkedIn profile belongs to the person unless identity matching is sufficiently supported (match company name, title, geography; label as **Likely Match** if profile snippet is partial).

#### PHASE 7 — Branch & location verification

- Do not assume multiple branches merely because multiple addresses appear on unrelated subpages.

- Cross-reference website location disclosures with Maps verification when available.

- Require clear supporting evidence for branch count (e.g. dedicated locations directory page, listed addresses with distinct phone numbers, verified Maps branch listings).

- If Maps and website data conflict, prioritize official first-party website disclosures over Maps listings, while noting any unresolved location discrepancies.

- Classify location status strictly as:

  - `Single location`
  - `Multiple locations — verified`
  - `Multiple locations — possible/unverified`

#### PHASE 8 — Deduplication & normalization

- Before adding a prospect:

  - Compare against existing prospect records in current run and master list;
  - Normalize business name (strip legal suffixes like LLC, Inc., Pvt Ltd for comparison);
  - Normalize domain (compare root hostname `domain.com`);
  - Compare address;
  - Compare phone number where available;
  - Compare decision-maker name.

- Do **NOT** create duplicate companies or locations merely because a different page, domain URL, or Maps place listing was discovered for the same underlying business.

- One real business should result in exactly **one** prospect record, unless existing ICP rules explicitly require separate location records.

#### PHASE 9 — Cost & rate-limit awareness (escalation path)

- Always use the cheapest, lightest sufficient Firecrawl operation first:

  1. Default: `firecrawl_scrape` on official homepage.

  2. Targeted Page Scrape: `firecrawl_scrape` on specific priority URLs (e.g. /about, /team).

  3. Map + Scrape: `firecrawl_map` to get URL list → targeted `firecrawl_scrape` on selected URLs.

  4. Full Crawl: `firecrawl_crawl` only when deeper structured site crawl is required and supported.

- Do **NOT** perform unnecessary repeated scrapes or crawls.

- **Failure handling**: If any Firecrawl operation fails or is unavailable:

  - Record the failure internally;
  - Fall back to standard web tools (`search_web`, `read_url_content`);
  - Continue research without stopping;
  - **Never fabricate missing information**.

#### PHASE 10 — Enriched Prospect Data Structure & Output

- For each enriched prospect, retain:

  - Source URL & root domain
  - Pages researched (list of URLs scraped/mapped)
  - Key facts discovered (Verified Facts)
  - Decision-makers (Name, Role, LinkedIn match status)
  - Products, services, & specialties
  - Locations/branches (with classification status)
  - Technology & equipment in use
  - Customer-acquisition / marketing signals (labeled as INFERENCE)
  - Evidence (traceable page URLs & snippets)
  - Estimated values (e.g. employee count derived from indirect evidence; state basis and label ESTIMATED)
  - Inferences (automation opportunities, score reasoning, qualitative judgments)
  - Overall Confidence (reflecting core prospect identity quality while preserving field classifications, e.g. "High — Core identity/location/website/decision-maker verified; employee count estimated"; never label the entire prospect "Verified" when fields are ESTIMATED or INFERENCE, and do not downgrade overall confidence merely because employee count is estimated or unavailable)
  - Unresolved / Missing information

---

**Find the decision-maker + LinkedIn.** Priority order (use the best real match, not necessarily top of list): COO → Operations Director → Managing Director → Founder → Owner → CEO → Plant Head → Operations Manager (adjust if the user specified a different target title). Search leadership/about/team pages (scraped via Firecrawl or web search), LinkedIn, press, and interviews. Never guess a name — if none can be verified, say so and fall back to the company's LinkedIn page or general contact info.

Always separately search for the individual's public LinkedIn profile (e.g. "[Name]" "[Company]" LinkedIn). Use Playwright when browser interaction or public-page inspection is needed. Never log in or access private LinkedIn information. Distinguish a directly visible public profile from a search-engine snippet; snippets are indexed evidence, not direct profile verification. Disambiguate common names using company, title, geography, and other public context. If identity matching is incomplete, label **Likely Match** rather than Verified; never guess a profile URL.

**For small/local businesses, LinkedIn is often a dead end — always check fallback channels too.** Alongside LinkedIn, look for: a WhatsApp Business number (common on Justdial/IndiaMart/Facebook listings or extracted via homepage scrape), Google Business Profile / Maps listing, or Facebook business page. These are frequently the *actual* reachable channel for local SMBs even when no LinkedIn presence exists. Note whichever channels you found — don't stop at "LinkedIn: not found" if a phone/WhatsApp number or Maps listing is sitting right there in the research findings.

From everything found, determine a **Best Contact Method** — the single most practical way to actually reach this prospect (e.g. "WhatsApp: +91-XXX," "LinkedIn DM," "Email via contact page," "Phone call"). Prefer the most direct/personal channel available; note it explicitly rather than leaving the user to infer it from the evidence list.

**Score (1-10).** 10 = Perfect ICP match, 8-9 = Strong fit, 6-7 = Moderate fit, below 6 = Weak fit. Base it on: industry fit, size fit, whether a decision-maker was found, quality/completeness of public info, strength of the AI opportunity (identified next), digital maturity, expansion signals, and accessibility. Always state the reason in 1-2 sentences tied to real findings (labeled as **INFERENCE**).

**Enough prospects?** If you've reached the requested quantity with genuinely qualified, unique prospects, exit the loop and move to delivery. If not, generate a fresh batch of search queries you haven't tried yet (broader geography, adjacent industry terms, different directories) and loop again — don't repeat an exhausted query.

**When to stop trying.** Run a reasonable number of loop rounds (roughly 3-4 broadening attempts). If the target still isn't reached with real, qualified prospects: stop, deliver what you have, and clearly state the shortfall and why (e.g. "found 6 of the 10 requested — the remaining candidates in this geography didn't have a verifiable decision-maker or public presence"). Never pad the list with weak fits just to hit the number.

### 4. Identify AI/automation opportunities

For each validated prospect, think like a consultant: name 1-3 concrete places automation could add value (e.g. customer support, lead qualification, appointment booking, CRM automation, invoice processing, inventory workflows, reporting, voice AI, chatbots, internal workflows). Always explain *why* — tie it to a specific signal found during Firecrawl site research or search (e.g. "manual booking process visible on their contact page" not just "could use a chatbot"). Do this as part of the Research step in the loop above, before scoring — the opportunity strength feeds into the score. All automation opportunity assessments must be explicitly labeled as **INFERENCE**.

### 5. Deliver the output

Sort the final list by Prospect Score, highest first. Flag the top 2-3 (or top third for larger batches) as **Priority Outreach** so the strongest prospects aren't buried in a flat list.

For every prospect, return:

- Company

- Website

- Industry

- Location

- Independent or Franchise/Chain

- Location Status (Single location / Multiple locations — verified / Multiple locations — possible/unverified)

- Estimated Employees (Never label as VERIFIED FACT unless a reliable public source explicitly supports that employee count/range. If derived from number of branches, team size descriptions, LinkedIn company size, organizational scale, or other indirect evidence, label ESTIMATED and explain the basis; if unavailable, label UNKNOWN / NOT FOUND.)

- Decision Maker + Role (or "Not publicly verified" + fallback contact route — note if this is a franchise's local manager rather than an owner)

- LinkedIn/Social Profile (individual's profile if found; otherwise company LinkedIn/Facebook/Google Business page; otherwise "Not publicly found")

- Best Contact Method (the single most practical channel to actually reach them — WhatsApp, phone, email, LinkedIn DM, etc.)

- WhatsApp Contact Number & Direct Link (CRITICAL: Whenever WhatsApp contact option is available or mentioned, ALWAYS provide their explicit WhatsApp contact number and click-to-chat link `https://wa.me/<number>`)

- Pages Researched (URLs accessed via Firecrawl, Playwright, or web read)

- Evidence (traceable page URLs & snippets confirming the findings)

- Research Summary & Key Verified Facts

- AI Opportunities (with reasoning, explicitly labeled INFERENCE)

- Prospect Score + Reason (explicitly labeled INFERENCE)

- Personalized Outreach Angle (a specific, non-generic opening line idea based on real research, explicitly labeled INFERENCE)

- Confidence Level (Overall confidence reflecting core prospect identity, location, website, and decision-maker evidence quality while preserving field-level classifications. Example format: "Overall Confidence: High — Core identity/location/website/decision-maker verified; employee count estimated". Do NOT label an entire prospect "Verified" when fields are ESTIMATED or INFERENCE, and do NOT downgrade a prospect merely because an employee count is unavailable.)

Ask how they want it delivered — as a table in chat, or as a downloadable spreadsheet — unless they've already told you a standing preference. For a spreadsheet, use the xlsx skill.

### 6. Update the master list

After delivering results, log every newly surfaced company + decision-maker to the persistent master list (see below) so future runs don't duplicate them.

## Persistence (avoiding duplicates across sessions)

This skill's dedupe memory lives in the **Claude memory filesystem** (the persistent record store), not in this skill's bundled files (which don't change at runtime):

- **Retrieval** — before a run, use `memory_read` on `/areas/prospect-master-list.md` to pull the current record. If it doesn't exist yet, treat the list as empty.

- **Create** — if the file doesn't exist yet, use `memory_write` to create it (frontmatter: name `prospect-master-list`, description "Running log of companies/decision-makers already surfaced by the ICP prospect finder, used to avoid duplicates across runs").

- **Append/update** — after a run, use `memory_append` (or `memory_str_replace` for editing an existing line) to add newly surfaced companies and decision-makers, one line per company in the form `Company — Decision Maker (Role) — Industry/Geography — [date]`.

## Quality checklist before delivering

MCP capability routing followed: Apify used for optional dynamic discovery when useful; Maps when local verification matters; Firecrawl for website enrichment; Playwright for interactive/public-profile research; suitable fallback used on failure.

Apify output treated strictly as candidate data; normalized and deduplicated against existing records and master list before validation and Firecrawl website enrichment.

Apify Actor selected dynamically based on user prompt/ICP; zero hardcoded industry or Actor assumptions.

First-party website evidence prioritized over Maps or directory data whenever conflicts arose.

- No invented names, employee counts, or news.

- Every field, claim, and conclusion is explicitly categorized using the four evidence classes: **VERIFIED FACT**, **ESTIMATED**, **INFERENCE**, or **UNKNOWN / NOT FOUND** — never convert estimates or inferences into verified facts or silently leave a field blank.

- Employee-count ranges derived from indirect evidence (branches, team descriptions, LinkedIn company size, organizational scale) are strictly labeled **ESTIMATED** with stated rationale, never **VERIFIED FACT**.

- Overall Confidence accurately reflects core identity evidence quality while preserving field-level classifications (never labeling an entire prospect "Verified" when fields are ESTIMATED/INFERENCE, nor downgrading overall confidence solely because an employee count is estimated or unavailable).

- Qualitative judgments (marketing spend, growth, positioning, likelihoods) are explicitly labeled as **INFERENCE** with supporting evidence.

- Multiple branch counts are verified and labeled as Single location, Multiple locations — verified, or Multiple locations — possible/unverified.

- No duplicate companies/people from this run or the master list, with name and domain normalization applied.

- Every score and automation opportunity has a stated reason explicitly tagged as an INFERENCE tied to real findings.

- Quantity/quality tradeoff resolved toward quality — a shorter list of well-verified prospects beats a padded one.