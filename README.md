# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

The domain I chose was running shoes. This knowledge is valuable because a good pair of running shoes gives you the confidence and comfortability to perform well, whether it's recreationally or competitively. The problem that most people encounter is choosing the "right" pair of running shoes. This is because there are many factors to take into consideration: price, material, sizing, etc. Aggregating all of this data together with a RAG model can give users the best personalized choice for what running shoes to buy.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Running Warehouse | A forum regarding the best running shoes to buy as of June 2026, depending on the attribute you're looking for (stability, max cushion, etc.). | https://www.runningwarehouse.com/learningcenter/gear_guides/footwear/best_running_shoes.html?from=gsearch&from=gshop&gad_source=1&gad_campaignid=12650333882&gbraid=0AAAAADka_jhmEg-nu7NFxDiE42FIF1OMo&gclid=CjwKCAjw857RBhAgEiwAI-1yKOeFY64em7jvIQ-xl6UMniLLAzjv49wGpzZZs3AA9OcFtjIMvoL0khoCT84QAvD_BwE
 |
| 2 | Runner's World | A list of the best running shoes curated by Runner's World, a renowned global magazine and website for runners. | https://www.runnersworld.com/gear/a19663621/best-running-shoes/
 |
| 3 | Reddit | A Reddit forum about the worst running shoes Redditors have ever bought. r/RunningShoeGeeks is an active running community with over 200K members. | https://www.reddit.com/r/RunningShoeGeeks/comments/16szb4e/worst_shoes_you_have_ever_bought/ |
| 4 | Reddit | A Reddit forum about the least favorite running shoes Radditors have ever bought. r/RunningShoeGeeks is an active running community with over 200K members. | https://www.reddit.com/r/RunningShoeGeeks/comments/16lwot2/what_are_your_least_favorite_running_shoes/ |
| 5 | Runrepeat | A guide on the best shoes for cross-country running, curated by Runrepeat. Runrepeat is a legitimate, highly trusted platform for athletic footwear reviews. | https://runrepeat.com/guides/best-cross-country-shoes |
| 6 | Reddit | A Reddit forum about the best shoes for cross country running. r/CrossCountry is an active running community with over 11K weekly visitors. | https://www.reddit.com/r/CrossCountry/comments/162zmd9/shoes_for_cross_country/ |
| 7 | Runrepeat | A guide on the best shoes for indoor/treadmill running, curated by Runrepeat. Runrepeat is a legitimate, highly trusted platform for athletic footwear reviews. | https://runrepeat.com/guides/best-treadmill-running-shoes |
| 8 | Reddit | A Reddit forum about the best budget running shoes. r/AdvancedRunning is an active running community with over 152K weekly visitors. | https://www.reddit.com/r/AdvancedRunning/comments/1ivvygy/for_budgetconscious_runners_what_are_the_most/ |
| 9 | Runner's World | A list of the most affordable running shoes curated by Runner's World, a renowned global magazine and website for runners. | https://www.runnersworld.com/gear/a24228881/affordable-running-shoes/ |
| 10 | Supwell | A list of the most expensive running shoes from every athletic brand, curated by Supwell. Supwell is an established digital platform designed for hobby joggers and running shoe enthusiasts. | https://www.supwell.com/supbeat/rating-the-most-expensive-race-shoes-from-every-brand |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 200 tokens

**Overlap:** 50 tokens

**Why these choices fit your documents:** After examining all of the documents I selected, the average review always falls below 200. The only exception are the reviews posted by Runner's World, which are usually about 250-300 words (tokens). To account for this, I have set the overlap to 50 tokens. The longest review I recorded in all of the documents is 309 words, which is significantly longer than the average. Since I'd rather accurately capture 200 majority of the reviews, I have set the Chunk size to 200 tokens, which is a more reasonable measure for the other reviews.

**Final chunk count:** 155 chunks across 10 documents

---

## Sample Chunks

- source9.txt | chunk 3 | 200 tokens | Brooks Launch 12 review from Runner's World affordable shoes
- source5.txt | chunk 11 | 200 tokens | On Cloudspike XC durability section from Runrepeat XC guide
- source2.txt | chunk 26 | 200 tokens | Racing/stability shoe explainer from Runner's World
- source7.txt | chunk 19 | 200 tokens | Shoe width/energy return data table from Runrepeat treadmill guide
- source5.txt | chunk 0 | 200 tokens | Intro to the Runrepeat XC guide
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 with a Top-k value of 20. This is a sentences-transformers model that maps sentences & paragraphs to a 384 dimensional dense vector space. This is essentially the baseline model for sentence embeddings, and was the one recommended by CodePath for this assignment. The only caveat was that input text longer than 256 word pieces were truncated (though this only affected a very small portion of the data).

**Production tradeoff reflection:** If I were deploying this system for real users and cost wasn't a constraint, I was consider swapping the current embedding model for one with more accurate domain-specific text and low-latency. That way, users can get more precise answers for their questions at a reasonable pace. The ultimate goal would be to make the RAG pipeline so precise, it can essentially pinpoint the "perfect shoe" for the user.

---

## Relevant Chunks Returned for Queries
__Query__: What are the most expensive shoes offered by Nike?
  [1] source2.txt (dist=0.4047)
       the bunch. These runners of various experience levels, gait patterns, ages, and arch types make our testing all-inclusiv...
  [2] source8.txt (dist=0.4121)
       available in DSW, retails in 60-70 dollars range. I'm on my 2nd pair and I put in 100+ miles a week so I'm cost consciou...
  [3] source8.txt (dist=0.4156)
       EZ_Company For budget-conscious runners, what are the most economical shoe per mile? Gear For budget-conscious runners, ...

__Relevance__: Chunks returned are partially relevant, both sources mentioned Nike running shoes a fair amount. 

__Query__: According to Supwell, are On Cloudboom Strike LS worth the $330 price tag?
  [1] source10.txt (dist=0.4597)
       $250 and can often be found at a massive discount in certain colorways. On Cloudboom Strike LS for $330 The Cloudboom St...
  [2] source10.txt (dist=0.6024)
       Rating the Most Expensive Race Shoes from Every Brand Every major running shoe brand now has at least one marathon race ...
  [3] source8.txt (dist=0.6309)
       of On Cloudswifts have lasted me anywhere from 300 mi to 600+. I think it depends far more on the terrain and running co...

__Relevance__: Chunks returned are relevant, 2/3 chunks returned are from source10, which was the exact source I was looking for. This is because my query specifically mentions Supwell, and so I wanted that source to be specifically retrieved.

__Query__: Best daily trainers according to Running Warehouse (looking for Brooks Adrenaline GTS 25)
[1] source2.txt dist=0.2958
holding back on easy days. The only flaw? Our testers point to its outsole. "It does not have the best traction over different surfaces and rounding some turns," said shoe tester Greg Jaindl. "[I foun

[2] source2.txt dist=0.4141
more foam, 1 mm in the heel, 3 mm in the forefoot. Nitrogen-infused DNA Loft v3 delivers high rebound and absorbs shock. The Adrenaline GTS is a comfy choice when you're looking for a workhorse traine

[3] source1.txt dist=0.4619
Ghost 17, the HOKA Clifton 10, and the Nike Vomero 18. The Nike Vomero 18 wins our top pick because of the way it facilitates easy rolling strides, and the combination of ReactX and ZoomX foams for pr

[4] source1.txt dist=0.4820
way that feels natural to your footstrike. Top to bottom, the Brooks Adrenaline GTS represents dependable stability, durability, and just enough cushioning to trust mile after mile. At a glance: Brook

[5] source2.txt dist=0.5218
collaborated with Brooks on earlier models, the trainer wins Best Overall Trail for its comfortable fit and stable ride over uneven terrain. The Cascadia 19 is updated with more DNA Loft v3 cushioning


__Relevance__: Chunks are partially relevant. 2/5 chunks are from the correct source (source1 aka Running Warehouse). More specifically chunk 4 mentions the Brooks Adrenaline GTS as a shoe that represents "dependable stability, durability, and just enough cushioning...", which is what I was looking for. 

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** Here is the system prompt I used: You are a running shoe assistant. Answer questions using ONLY the numbered passages \
provided by the user. Do not use your general training knowledge about running shoes \
or any information not present in the passages.

Rules:
- If the answer is clearly stated in the passages, answer directly and concisely.
- If the answer is not in the passages, say exactly: \
"I don't have enough information in my sources to answer that."
- Do not invent shoe names, prices, specifications, or opinions.
- Every claim you make must be traceable to one of the provided passages.\

I limited the LLM to using only the numbered passages provided by the user. If the LLM could not successfully find an answer in the passages, I told it exactly how to respond. 

**How source attribution is surfaced in the response:** "Every claim you make must be traceable to one of the provided passages." I also gave each source a label, so that the LLM could respond with the exact sources it retrieved from in order to generate its answer.

**Example System Responses:**
#### Q: What are the most expensive shoes offered by Nike?

**Answer:**
The most expensive running shoes offered by Nike mentioned in the passages are the Alphafly 3 at $295 and the Alphafly 4 (price not specified, but mentioned as an upcoming release).

**Retrieved from:**
- Runner's World — Best Affordable Running Shoes
- Runner's World — 15 Best Running Shoes of 2026
- Supwell — Most Expensive Race Shoes by Brand
- Reddit r/AdvancedRunning — Budget running shoes
- Running Warehouse — Best Running Shoes of 2026

#### Q: What are the best daily trainers for stability, according to Running Warehouse?

**Answer:**
The best daily trainers for stability are the Brooks Adrenaline GTS 25, according to the passages.

**Retrieved from:**
- Runrepeat — Best Treadmill Running Shoes
- Runner's World — 15 Best Running Shoes of 2026
- Running Warehouse — Best Running Shoes of 2026
- Reddit r/AdvancedRunning — Budget running shoes

**Out-of-scope query example**
#### Q: What running shoes does Usain Bolt wear?

**Answer:** I don't have enough information in my sources to answer that.

**Retrieved from:**
- Runner's World — 15 Best Running Shoes of 2026
- Running Warehouse — Best Running Shoes of 2026
- Runner's World — Best Affordable Running Shoes
- Supwell — Most Expensive Race Shoes by Brand
- Reddit r/AdvancedRunning — Budget running shoes
- Runrepeat — Best Treadmill Running Shoes
---

## Query Interface
When executed, app.py yields a simple interface. It has:
- a title ("Running Shoe Guide")
- a subtitle ("Answers are grounded in 10 curated sources only.")
- a question box where users input their queries, an "Ask" button
- an "Answer" box where the LLM generates its response
-  a "Retrieved from" box where the LLM gives its source attribution.

__Sample Interaction Transcript__:

#### Q: What are the best running shoes offered by Adidas?

**Answer:**
According to the passages, the best running shoes offered by Adidas are:

1. Adidas Adizero Evo SL (Best Overall) — [passage 2]
2. Adidas Adizero Adios Pro 4 (Best Racing Shoes, Best Overall Racer) — [passage 11]
3. Adidas Adizero Adios Pro Evo 2 — [passage 12]
4. Adidas Takumi Sen 11 — [passage 16]
5. Adidas Adizero SL2 — [passage 15]

*Note: The answer is based on the information provided in the passages and may not be a comprehensive list of all the best Adidas running shoes.*

**Retrieved from:**
- Running Warehouse — Best Running Shoes of 2026
- Runner's World — 15 Best Running Shoes of 2026
- Runner's World — Best Affordable Running Shoes
- Reddit r/RunningShoeGeeks — Least favorite shoes
- Supwell — Most Expensive Race Shoes by Brand
- Reddit r/AdvancedRunning — Budget running shoes
- Runrepeat — 7 Best Cross Country Shoes 2026
- Runrepeat — Best Treadmill Running Shoes

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are the most expensive shoes offered by Nike? | Nike Alphafly 3 at $295 | Alphafly 3 at $295 | Relevant | Accurate |
| 2 | What are the best running shoes offered by Adidas? | Adidas Adizero Evo SL | A list of 5 shoes, Adidas Adizero Evo SL ranked "Best Overall" | Relevant | Partially accurate |
| 3 | According to Supwell, are On Cloudboom Strike LS worth the $330 price tag? | No | No, the Cloudboom Strike are a better deal | Relevant | Accurate |
| 4 | What are the best lightweight cross-country shoes according to Runrepeat? | Nike Zoom Victory Waffle 5 | 2 shoes mentioned, neither one being the Nike Zoom Victory Waffle 5 | Relevant | Inaccurate |
| 5 | What are the best daily trainers for stability, according to Running Warehouse? | Brooks Adrenaline GTS 25 | Brooks Adrenaline GTS 25 | Partially relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** Q4: What are the best lightweight cross-country shoes according to Runrepeat?

**What the system returned:** "According to passage [4], the On Cloudspike XC is mentioned, but it's described as "heavier than its main rivals." Passage [15] mentions the Salomon Zinal 2, describing it as "crazy lightweight" and "exceptionally fast." Therefore, the Salomon Zinal 2 can be considered one of the best lightweight cross-country shoes according to the provided passages."

**Root cause (tied to a specific pipeline stage):**  Retrieval works fine (source5 appears in the top-20). However, the specific chunk that mentions the Nike Zoom Victory Waffle 5 is not in the top-20. Instead, LLM receives information about a different shoe (Salomon Zinal 2) which has "Crazy lightweight" listed as one of its pros. The root cause is the chunking. The section header ("Best lightweight cross-country shoes") and the shoe name ("Nike Zoom Victory Waffle 5") sit at lines 210-211. Since I have 200-token chunks with a 50-token overlap, the header and the shoe description were split into two separate chunks. With these chunks split up, they aren't relevant enough to score in the top-20, which is why a different shoe that was chunked in retrieved.

**What you would change to fix it:** The most straightforward change would be to increase the chunk size, so that each embedding has more context. If I were to do this, the header and the shoe name mentioned above would likely be chunked  together.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** planning.md pretty muched guided my entire implementation. It gave me a structure to follow and without it, I would have probably gone in the completely wrong direction with this project. The spec also helped me evaluate the model throughout different iterations. More specifically, I found that forming the Evaluation Plan before implementation was a good way to check if the result I produced matched the result I was aiming for.

**One way your implementation diverged from the spec, and why:** Originally didn't consider testing grounded generation in my spec (if I had, I would've likely put it in my Evaluation Plan). But as I went forward with the implementation, I realized that I needed to ground responses in order to accurately compare my respones with the Evaluation Plan. I was afraid that the LLM would respond with knowledge that was outside of the sources provided.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I gave Claude my planning.md and specifically told it to use Documents and Chunking Strategy sections to come up with ingest.py and chunker.py files. 
- *What it produced:* It produced a chunker.py file (which takes a string, returns a list of 200-word strings with 50-word overlap) and an ingest.py file (which reads every .txt from documents/, normalizes whitespace and calls chunk_text() on each document to print a table to verify the output).
- *What I changed or overrode:* Some chunks yielded very small amounts of tokens (1 and 7), so I added a minimum token filter in build_chunks() to get rid of these.

**Instance 2**

- *What I gave the AI:* I gave Claude my planning.md and specifically told it to use my Retrieval Approach to generate an embedder.py file and retriever.py file
- *What it produced:* Claude produced an embedder.py file (which loads chunks from ingest.py, embeds with my specified model, and stores in ChromaDB) and a retriever.py file (which embeds a question, asks ChromaDB for top-20 matches, and returns results)
- *What I changed or overrode:* Claude used some broad placeholder queries that didn't match what I was looking for, so I replaced them with the queries from my evaluation plan (which were more specific and targeted).
