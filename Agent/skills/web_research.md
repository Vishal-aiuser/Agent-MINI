# Skill: Deep Web Research

## Purpose
Use this skill when the user asks for in-depth information, current news, product comparisons, or detailed explanations of topics not fully covered in memory.

## Recommended Workflow

1. **Search with Precision (`web_search`)**
   - Break down the user's question into clear, concise keywords.
   - Call `web_search(query)` to find top relevant links and snippets.

2. **Select & Scrape Key Sources (`scrape_webpage`)**
   - Review the URLs returned by the search.
   - Pick the most authoritative or informative link (e.g. Wikipedia, official docs, reputable news).
   - Call `scrape_webpage(url)` to read the full page text.

3. **Synthesize & Cite**
   - Extract facts, figures, and direct answers to the user's question.
   - Summarize the findings clearly using bullet points and headers.
   - Always mention the source URL so the user knows where the information came from.

## Rules & Stopping Condition
- **Limit Searches:** Perform at most 3 to 4 targeted searches. Do NOT loop infinitely.
- **Synthesize Early:** As soon as you have key highlights and facts, STOP calling tools and write the final summary.
