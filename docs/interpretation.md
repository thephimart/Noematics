# Interpretation: Mechanical Specification

Interpretation is the core operation of Noematics. This document provides the precise mechanical specification.

---

## Definition

```
interpret(noema, round_context) → InterpretationDelta
```

---

## Properties

| Property | Specification |
|----------|---------------|
| **Purity** | Pure function: `f(noema, ctx) → delta` with no side effects |
| **Output** | Returns a **delta**, not full state — enables compositional reasoning |
| **Idempotence** | `interpret(x) ∘ interpret(x) = interpret(x)` |
| **Commutativity** | `interpret(a) ∘ interpret(b) = interpret(b) ∘ interpret(a)` |

---

## Data Structures

```python
@dataclass
class InterpretationDelta:
    """Delta produced by interpretation — never full state"""
    query_delta: str          # What information is now needed (append-only)
    key_delta: str            # What information is now offered (append-only)
    field_membership: Optional[str] = None  # None = no change
    metadata_delta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class InterpretationInput:
    """Complete input to interpretation function"""
    noema: "Noema"
    round_context: "RoundContext"
    received_messages: List["AgentMessage"]
    
@dataclass  
class InterpretationResult:
    """Complete output of interpretation"""
    delta: InterpretationDelta
    local_state_update: Dict[str, Any]
    messages_to_route: List["RoutingDecision"]
```

---

## Pseudocode Algorithm

```
function interpret(input: InterpretationInput) → InterpretationResult:
    
    # Step 1: Analyze received messages
    relevant_info = extract_relevant_content(input.received_messages)
    
    # Step 2: Update local understanding (pure state transformation)
    current_q = input.noema.query_vector
    current_k = input.noema.key_vector
    
    new_q = refine_query(current_q, relevant_info, input.round_context.goal)
    new_k = refine_key(current_k, relevant_info, input.round_context.goal)
    
    # Step 3: Determine information needs
    information_gap = compute_information_gap(
        new_q, 
        input.round_context.goal,
        input.received_messages
    )
    
    # Step 4: Determine field membership (may be None = no change)
    target_field = determine_field_membership(
        new_k,
        input.round_context.available_fields
    )
    
    # Step 5: Build routing decisions
    routing = determine_routing_targets(
        information_gap,
        input.round_context.neighbor_noemata
    )
    
    # Step 6: Compose delta
    delta = InterpretationDelta(
        query_delta=diff(current_q, new_q),      # What changed in query
        key_delta=diff(current_k, new_k),        # What changed in key
        field_membership=target_field,           # May be None
        metadata_delta={"round": input.round_context.round_number}
    )
    
    return InterpretationResult(
        delta=delta,
        local_state_update={"query": new_q, "key": new_k},
        messages_to_route=routing
    )
```

---

## Conflict Resolution

When multiple interpretations produce conflicting field memberships:

```
resolve_conflict(deltas: List[InterpretationDelta]) → InterpretationDelta:
    
    # Priority: explicit field_membership > None
    non_null = [d for d in deltas if d.field_membership is not None]
    
    if len(non_null) == 0:
        return merge_deltas(deltas)  # All None = no conflict
    elif len(non_null) == 1:
        return non_null[0]
    else:
        # Multiple explicit memberships — use highest round number
        return max(non_null, key=lambda d: d.metadata_delta.get("round", 0))
```

---

## Key Questions Answered

- **Is interpretation pure?** Yes — same inputs always produce same outputs
- **Are deltas allowed?** Yes — deltas enable compositional reasoning
- **Can interpretations commute?** Yes — deltas must be order-independent
- **How are conflicts surfaced?** Via field_membership conflicts resolved by round number priority
