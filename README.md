# Music Generator Company – Minimal Prototype

## What This Is

This is a **200-line proof of concept** that demonstrates the multi-agent architecture proposed for CloudWalk's Level 2.3 challenge.

This is **not**:
- A production system
- A complete music generator
- A real billing platform
- A social media automation tool

This **is**:
- An architecture validation
- A demonstration of agent separation
- An example of selective RAG usage
- A pragmatic engineering exercise

## Why So Small?

Previous CloudWalk challenges tested reasoning, not implementation scale. Level 2.3 is about **system design thinking**, not building production code.

The 200-line constraint forces:
- Clear separation of concerns
- Selective use of AI (only where it adds value)
- Pragmatic engineering decisions
- Focus on orchestration over implementation

## Design Decisions

### 1. Mocked External Services

**Why:** The challenge is about coordination, not API integration.

- Music generation → Simulated with genre/mood selection
- Stripe billing → Mocked with simple status tracking
- Social media → Mocked with post formatting

Real APIs would add complexity without demonstrating better architecture.

### 2. Selective RAG Usage

**Music Agent:**
- Uses RAG to avoid repeating recent genres
- Retrieves mood patterns by time of day
- **Why:** Context prevents repetitive output

**Marketing Agent:**
- Uses RAG to retrieve successful post templates
- Finds hashtags by genre
- **Why:** Learning from examples improves quality

**Billing Agent:**
- No RAG, pure deterministic logic
- **Why:** Subscription billing doesn't benefit from LLM usage

### 3. Local Knowledge Base

Instead of a vector database, this uses a simple JSON file:
```json
{
  "recent_genres": ["lofi", "jazz"],
  "mood_mapping": {"morning": "uplifting", "evening": "calm"},
  "marketing_templates": [...]
}
```

**Why:** For 200 lines, in-memory state is sufficient to demonstrate RAG concepts.

### 4. No LLM API Calls

This prototype uses **simulated LLM responses** (predefined logic).

**Why:**
- Avoids API costs during evaluation
- Makes the code runnable without credentials
- Demonstrates the architecture, not the model

In production, the `_simulate_llm()` function would be replaced with actual OpenAI/Anthropic calls.

## Architecture

```
┌─────────────────────────────────────┐
│     Autonomous Music Company        │
└─────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼──┐ ┌────▼─────┐
│ Music │ │Bill │ │Marketing │
│ Agent │ │Agent│ │  Agent   │
└───┬───┘ └──┬──┘ └────┬─────┘
    │        │         │
    └────────┼─────────┘
             │
    ┌────────▼────────┐
    │   Knowledge     │
    │      Base       │
    │   (RAG Store)   │
    └─────────────────┘
```

## How to Run

```bash
python prototype.py
```

Expected output:
```
=== Music Agent ===
Generated: "Morning Light" (Pop, Uplifting)
RAG Context: Avoided [lofi, jazz] (recently used)

=== Billing Agent ===
Processed 5 subscriptions: $5.00

=== Marketing Agent ===
Posted: "🎵 New Pop track: Morning Light! #Pop #Music"
RAG Context: Retrieved template with 850+ engagement
```

## What This Demonstrates

✅ Multi-agent coordination  
✅ Selective RAG application  
✅ Context-aware decision making  
✅ Pragmatic engineering  
✅ Knowing when NOT to use AI  

## What's Missing (Intentionally)

❌ Real audio generation  
❌ Payment processing  
❌ Social media APIs  
❌ Database persistence  
❌ Error handling  
❌ Testing  
❌ Production infrastructure  

These would be added in a real product, but they don't demonstrate better architecture for this challenge.

## Key Insight

**The $1 subscription price is a hint.**

CloudWalk wants to see if candidates can build simple, elegant systems instead of over-architected solutions. The challenge is about judgment, not features.

## Files

- `prototype.py` - 200-line multi-agent system
- `knowledge_base.json` - Simple RAG store
- `README.md` - This file

## Next Steps (If This Were Real)

1. Replace simulated LLM with actual API calls
2. Add vector database (Pinecone/Qdrant) for similarity search
3. Integrate real music APIs (Suno, Riffusion)
4. Add Stripe webhooks for billing
5. Connect Twitter/LinkedIn APIs
6. Add proper error handling and logging
7. Build monitoring and alerting
8. Add tests (unit + integration)

But for an architecture validation? This is sufficient.

---

**Author:** Juan  
**Challenge:** CloudWalk AI Wizard Level 2.3  
**Approach:** Minimal viable architecture demonstration
