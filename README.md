# Agent Tool Discovery & Semantic Router


```text
ADK Agent -> Tool Requirement -> Semantic Discovery -> MCP/REST/Agent Registry -> Candidates -> Policy -> Schema -> Rank(cost/latency/trust/health) -> Best Tool -> Execute -> Telemetry/Fallback
```

## Quick start
```bash
cp .env.example .env
docker compose up --build -d
curl http://localhost:8000/health
curl -X POST http://localhost:8000/v1/route -H "x-api-key: change-me" -H "content-type: application/json" --data-binary @examples/route.json
```

## 1. Executive summary

A production semantic router turns a natural-language capability requirement into a governed tool invocation. It separates discovery, authorization, compatibility, ranking, execution and telemetry.

## 2. Architecture

ADK Agent -> Tool Requirement -> Semantic Discovery -> MCP/REST/Agent registries -> Candidate Tools -> IAM/Policy -> Schema Compatibility -> Ranking -> Best Tool -> Gateway/Executor -> Telemetry/Fallback.

## 3. Why dynamic routing

Hard-coded tool bindings couple agents to providers. Dynamic routing lets organizations evolve tools, versions, regions and providers without rewriting every agent.

## 4. Google alignment

Google Agent Registry is a centralized catalog for MCP servers, tools, skills, endpoints and agents, supports keyword/prefix/semantic search, endpoint resolution and authentication bindings. Agent Gateway is the runtime enforcement point.

## 5. Tool requirement contract

The request expresses intent, required input/output shape, tags, cost/latency/trust constraints and arguments. This is more stable than naming a provider.

## 6. Registry model

Each capability carries ID, version, kind, endpoint, description, schemas, tags, risk, cost, latency, trust, health and authorization metadata.

## 7. Semantic discovery

Embed the requirement and capability metadata, retrieve top candidates, then apply deterministic compatibility and policy gates.

## 8. Embeddings

The runnable reference uses deterministic hashing embeddings to work offline. Production swaps in an approved embedding model and versioned vector index.

## 9. Schema compatibility

Semantic similarity is insufficient. Required fields, types, enums, output contract and protocol constraints must be compatible.

## 10. IAM filtering

Authorization is a hard gate before ranking. An unauthorized tool is not a low-scoring candidate; it is absent from the eligible set.

## 11. Policy

Combine agent identity, delegated user identity, tenant/project, destination, action, risk, data classification and purpose.

## 12. Semantic governance

Natural-language governance can add intent-sensitive restrictions, but deterministic IAM remains authoritative.

## 13. Ranking

A multi-objective score combines semantic match, schema compatibility, trust, health, latency and cost. Hard constraints remove candidates before scoring.

## 14. Trust

Trust is organizational policy based on publisher, attestation, review, ownership, data handling and incident history—not LLM confidence.

## 15. Health

Health combines availability, error rate, p95 latency, circuit-breaker state and freshness. Persist time-series samples and use EWMA/windows.

## 16. Cost

Cost includes provider charge, model tokens, egress, database/query cost and organization-specific chargeback.

## 17. Latency

Use observed latency distributions by region/operation rather than static metadata alone.

## 18. Fallback

Keep ranked alternates. Fallback only when policy/schema constraints remain satisfied; never bypass authorization to improve availability.

## 19. Circuit breakers

Open unhealthy tools after error thresholds, probe in half-open state and exclude them from ordinary ranking.

## 20. Retries

Retry only retryable failures, with bounded exponential backoff/jitter and idempotency protection.

## 21. Idempotency

Every side-effecting tool invocation needs an idempotency key or reconciliation strategy.

## 22. MCP

Discover tool specifications, validate arguments, authorize destination/tool, invoke through governed transport, validate result and record telemetry.

## 23. MCP 2026 statelessness

Current MCP direction includes stateless self-describing requests; production adapters should negotiate/support the protocol version actually deployed rather than hard-code legacy handshakes.

## 24. REST

REST endpoints require allowlisted host/method/path templates, schema validation, SSRF defenses, OAuth/workload credentials and response validation.

## 25. A2A agents

Agent candidates are capabilities too, but delegation needs task/message contracts, identity propagation, timeout/cancel and loop/depth protection.

## 26. Credential broker

The router chooses a capability but never hands raw long-lived secrets to the model. Credentials are resolved just-in-time from identity/auth bindings.

## 27. Agent identity

Use unique workload identity for each agent and optionally user delegation. Shared service credentials reduce auditability.

## 28. Gateway

All production execution should pass through a policy enforcement point for destination checks, auth, content security, quotas, audit and observability.

## 29. Content security

Inspect tool arguments/responses for injection, sensitive data and prohibited content where policy requires.

## 30. Data residency

Registry/gateway/tool region constraints are part of eligibility, not an afterthought.

## 31. Multi-tenancy

Tenant context comes from trusted identity. Registry views, caches, telemetry and policy decisions are tenant scoped.

## 32. Registry ingestion

Ingest Google/enterprise registries, MCP tools/list, OpenAPI specs and A2A agent cards into a normalized capability model.

## 33. Versioning

Tool versions are immutable capability revisions. Routing policy controls promotion, canarying and retirement.

## 34. Canary routing

Send bounded traffic to a new version only after policy eligibility, with rollback based on errors/quality/latency.

## 35. Quality score

Tool quality can include task success, evaluator score, user feedback and domain-specific correctness.

## 36. Feedback loop

Telemetry updates health/quality priors but must not autonomously expand authorization.

## 37. Telemetry

Emit trace spans for discovery, policy, compatibility, ranking, credential resolution, gateway invocation, retries and fallback.

## 38. Audit

Record requirement, principal, eligible set summary, selected tool/version, policy version, score components and outcome.

## 39. Explainability

Return selection reasons without leaking unauthorized candidates.

## 40. Privacy

Avoid embedding secrets or sensitive raw arguments into globally shared indexes/logs.

## 41. Caching

Cache registry/search results by tenant, policy/version and embedding model. Do not cache credentials.

## 42. Cache invalidation

Registry/policy/health events invalidate candidate and decision caches.

## 43. SQL

SQL stores normalized capability metadata, versions, health summaries, invocation/audit records and routing policies.

## 44. Vector index

Vector search stores capability embeddings plus trusted filter metadata. It is a derived index.

## 45. Event bus

Registry, health and policy changes publish events consumed by indexers/cache invalidators.

## 46. Transactional outbox

When registry metadata changes in SQL, publish derived-index events using an outbox rather than dual writes.

## 47. Reconciliation

Periodically compare registry truth and vector/search projections and repair drift.

## 48. Availability

If semantic search is down, a deterministic keyword/tag fallback can preserve limited discovery without weakening policy.

## 49. Degraded mode

If policy/IAM is unavailable, fail closed for protected tools rather than using stale broad permissions.

## 50. SLOs

Track discovery availability, p95 route latency, policy latency, selection success, invocation success, fallback rate, stale health and audit completeness.

## 51. Metrics

Candidates discovered/filtered, no-match rate, schema rejects, IAM rejects, per-tool selections, cost, latency, health, circuit state and fallback count.

## 52. Capacity

Model tools/tenant, discovery QPS, embedding dimensions, policy QPS, health sample rate, invocation QPS and telemetry retention.

## 53. Rate limits

Limit discovery and execution independently by tenant, agent, user and destination.

## 54. Quotas

Support per-tool and per-tenant spend/QPS/concurrency budgets.

## 55. Concurrency

Use bulkheads so one slow provider cannot exhaust router workers.

## 56. Backpressure

Queue or reject before saturation and expose retry-after information.

## 57. Security threats

Registry poisoning, malicious tool descriptions, prompt injection, SSRF, credential exfiltration, schema smuggling, confused deputy, cross-tenant leakage and fallback bypass.

## 58. Registry admission

Only approved publishers/admin flows register production tools. Validate endpoints, ownership, schemas, labels and signatures/attestation where available.

## 59. Tool descriptions are untrusted

Descriptions aid discovery but cannot override policy or system instructions.

## 60. Confused deputy

Bind delegated user intent, agent identity, destination and requested action to the authorization decision.

## 61. SSRF

REST/MCP egress uses allowlisted destinations, DNS/IP checks and gateway-controlled networking.

## 62. Schema smuggling

Reject unexpected fields when contracts require strict schemas; cap sizes/depths and validate content types.

## 63. Output validation

Treat tool output as untrusted; validate schema and content before returning it to the agent.

## 64. Human approval

High-risk candidates may require approval after selection but before credential resolution/execution. Bind approval to action hash.

## 65. Evaluation

Offline golden requirements measure recall@k, authorized recall, schema precision, top-1 success, cost/latency utility and unsafe-selection rate.

## 66. Online evaluation

Shadow alternative rankings without executing them, compare outcomes and guard against feedback loops.

## 67. Applications

Enterprise analytics, CRM, support, SRE, developer tooling, finance, research and multi-agent delegation.

## 68. Analytics example

Requirement: trusted customer revenue query. Discover BigQuery/CRM/finance-agent candidates, filter IAM, check schema, rank by trust/latency/cost, invoke best.

## 69. SRE example

Discover log, metrics, trace and deployment tools; policy can restrict write/remediation tools while allowing read-only diagnostics.

## 70. Developer example

Discover code search, CI, issue tracker and repository agents dynamically based on task.

## 71. Support example

Route to CRM, knowledge, order and refund tools with user/tenant/data-scope enforcement.

## 72. Finance example

Require higher trust, stronger approvals and audited tool versions for consequential operations.

## 73. ADK integration

Wrap the router as one stable ADK tool: `discover_and_execute(requirement, arguments)`. The ADK agent does not need static bindings to every enterprise capability.

## 74. API

GET /v1/tools lists the local demo catalog; POST /v1/route performs discovery, policy, ranking and optional execution.

## 75. Code map

domain.py contracts; registry.py catalog; embeddings.py discovery vectors; schema.py compatibility; policy.py authorization; discovery.py candidate retrieval; ranking.py multi-objective score; executors.py MCP/REST/A2A boundaries; router.py orchestration; api.py HTTP surface.

## 76. Production services

registry-ingestor, semantic-indexer, discovery-api, policy-adapter, health-collector, ranker, credential-broker, gateway-executor, telemetry, evaluator, reconciliation.

## 77. Kubernetes

Deploy stateless router replicas with workload identity, HPA, PDB, deny-by-default egress except gateway/registry/telemetry, and managed SQL/vector/event dependencies.

## 78. Multi-region

Keep registry/policy locality and residency constraints in eligibility; route execution through regional gateways and prefer healthy local endpoints where policy permits.

## 79. DR

Restore registry SQL, rebuild semantic index, restore policy connectivity, warm health state conservatively and fail closed until authorization is trustworthy.

## 80. Testing

Unit, schema/property, IAM isolation, ranking golden sets, protocol contract, security, load, chaos and DR tests.

## 81. Principal questions

Why policy before ranking? How prevent registry poisoning? How score cost vs trust? How route during health degradation? How support versioned embeddings? How prevent fallback authorization bypass? How reconcile dynamic discovery with deterministic audit?

## 82. Production boundary

The included implementation is executable and substantive, but organization-specific Google Agent Registry APIs, Agent Identity, Gateway, production embeddings, OAuth bindings, OTel and hardened Kubernetes require deployment credentials/configuration and are adapters, not fabricated internal Google code.

## Full local run instructions

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
```

Host mode:
```bash
docker compose up -d postgres redis
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
# change DATABASE_URL hostname to localhost
uvicorn app.main:app --reload
```

Inspect tools:
```bash
curl -H 'x-api-key: change-me' http://localhost:8000/v1/tools
```

Route and execute:
```bash
curl -X POST http://localhost:8000/v1/route \
 -H 'x-api-key: change-me' \
 -H 'Content-Type: application/json' \
 --data-binary @examples/route.json
```

Tests:
```bash
pytest -q
ruff check .
```

## Selection formula

The reference uses a transparent weighted score after hard constraints:

```text
0.45 semantic capability match
0.15 schema compatibility
0.15 trust
0.10 health
0.08 latency utility
0.07 cost utility
```

Weights are configuration/evaluation targets in a real deployment; consequential policy decisions are never encoded merely as ranking weights.

## Production upgrade checklist

```text
[ ] Google/enterprise Agent Registry adapter
[ ] versioned vector index and production embeddings
[ ] OpenAPI + MCP + A2A ingestion
[ ] OIDC/Agent Identity/workload identity
[ ] user delegation
[ ] IAM/ABAC/semantic governance adapter
[ ] Agent Gateway enforcement
[ ] credential broker/auth bindings
[ ] Model Armor/content security
[ ] dynamic health collector
[ ] persistent registry + migrations
[ ] transactional outbox/event consumers
[ ] circuit breaker/retry/idempotency/reconciliation
[ ] approval service for high-risk tools
[ ] OpenTelemetry + metrics + immutable audit
[ ] rate limits/quotas/cost budgets
[ ] regional/residency routing
[ ] hardened Kubernetes/Helm
[ ] golden routing evaluations
[ ] load/chaos/security/DR tests
```

## Final rule

```text
Discovery finds what could work.
Schema proves it can accept the request.
Identity proves who is asking.
Policy decides what may be used.
Ranking chooses among allowed alternatives.
Gateway controls execution.
Telemetry proves what happened.
```

**Semantic similarity can select among authorized capabilities; it must never create authorization.**

# Comprehensive Architecture, Operations & Production Guide

## 83. System context

The Semantic Router is a **decision plane** between an agent and an organization's capability ecosystem. The agent expresses *what it needs done*. The router determines *which approved capability should do it*.

```text
                        USER / APPLICATION
                               |
                           ADK AGENT
                               |
                       Tool Requirement
                               |
                   +-----------v-----------+
                   | Semantic Tool Router  |
                   +-----------+-----------+
                               |
        +----------------------+----------------------+
        |                      |                      |
 Agent Registry          MCP Registries        REST / OpenAPI
        |                      |                      |
        +----------------------+----------------------+
                               |
                    Normalized Capability Catalog
                               |
                    Semantic Candidate Search
                               |
                    Deterministic Hard Gates
                    /          |          \
                IAM/ACL      Schema      Policy
                    \          |          /
                     Eligible Candidate Set
                               |
                    Multi-objective Ranking
          semantic / trust / health / latency / cost
                               |
                    Selected Tool + Fallbacks
                               |
                       Credential Broker
                               |
                         Agent Gateway
                               |
              +----------------+----------------+
              |                |                |
             MCP              REST             A2A
              |                |                |
             Tool             API             Agent
              +----------------+----------------+
                               |
                      Result Validation
                               |
                  Telemetry / Audit / Feedback
```

## 84. Control plane versus execution plane

The **control plane** owns registration, normalized metadata, embeddings, policy metadata, health summaries, versions and routing configuration. The **execution plane** performs governed calls to MCP tools, REST endpoints and agents. Separating these planes prevents catalog/search outages from automatically weakening runtime enforcement.

## 85. Request lifecycle

```text
1. authenticate caller
2. derive trusted tenant / agent / user delegation
3. normalize natural-language requirement
4. discover candidate capabilities
5. enforce tenant/project/region constraints
6. enforce IAM/RBAC/ABAC
7. validate input/output schema compatibility
8. enforce risk/data/purpose policy
9. remove unhealthy/circuit-open candidates
10. rank eligible candidates
11. select primary and bounded fallbacks
12. obtain short-lived credentials
13. execute through gateway
14. validate output
15. record telemetry/audit
16. update health/quality signals asynchronously
```

## 86. Why discovery and authorization are separate

Discovery answers **what can technically satisfy this intent**. Authorization answers **what this principal may use**. Mixing them creates unsafe systems where high semantic similarity can accidentally influence access.

## 87. Normalized capability model

A production capability record should include:

```text
logical capability ID
immutable revision/version
kind: MCP_TOOL / REST / A2A_AGENT / SKILL
publisher / owner
natural-language description
tags / domains
input JSON schema
output JSON schema
endpoint reference
protocol/version
required permissions
risk level
data classification
supported regions
cost model
latency model
trust score inputs
health summary
deprecation state
attestation / provenance
```

## 88. Stable logical IDs

Agents should route to logical capabilities rather than physical URLs. Endpoint changes therefore do not require prompt/application rewrites.

## 89. Capability revisions

Treat tool definitions as immutable revisions. Promotion selects the active/default revision; rollback restores a known prior revision.

## 90. Registry ingestion architecture

```text
Google Agent Registry -----+
Enterprise Registry -------+
MCP tools/list ------------+--> Normalizer --> Admission --> SQL Truth
OpenAPI -------------------+                       |
A2A Agent Card ------------+                       +--> Outbox
Internal Catalog ----------+                              |
                                                           +--> Semantic Index
                                                           +--> Cache Invalidation
```

## 91. Registry admission

Before a capability becomes routable, validate publisher, endpoint ownership, protocol, schema, allowed domains, data handling, required permissions and organizational approval.

## 92. Registry poisoning

An attacker may register a tool with a description designed to win semantic search. Admission, publisher trust and policy prevent description text from becoming authority.

## 93. Description sanitization

Tool descriptions are discovery metadata. They are never interpreted as system instructions.

## 94. Semantic representation

Embed a canonical document built from capability name, description, tags, schema field descriptions and declared skills. Do not embed secrets or credentials.

## 95. Embedding version

Persist:

```text
embedding_model
embedding_model_version
embedding_dimension
canonicalization_version
indexed_at
```

so the index can be rebuilt reproducibly.

## 96. Semantic index migration

Build index v2 in parallel, shadow queries, compare recall/ranking, then cut traffic over. Never silently mix incompatible embeddings.

## 97. Hybrid discovery

Production discovery can combine:

```text
semantic vector search
keyword/BM25
tags
skill metadata
schema field names
graph relationships
publisher/owner filters
region
protocol
```

## 98. Candidate fan-out

Bound discovery fan-out before expensive IAM/schema evaluation. Typical systems retrieve a moderate top-K and then apply deterministic gates.

## 99. Semantic recall evaluation

Maintain golden natural-language requirements with expected capability sets and measure recall@K, MRR and top-K authorized recall.

## 100. Schema compatibility pipeline

Schema validation is a hard technical gate:

```text
required request fields
 -> type compatibility
 -> enum/range constraints
 -> nested object compatibility
 -> additionalProperties policy
 -> protocol-specific fields
 -> output requirements
```

## 101. Argument synthesis boundary

The router may map caller arguments to a compatible tool schema, but mapping must be typed, validated and bounded. Never allow a model to invent privileged headers or credentials.

## 102. Strict schema mode

High-risk tools should reject unknown fields and cap object depth, string length, arrays and payload size.

## 103. Output contracts

Validate outputs before exposing them to the agent. Invalid outputs are execution failures, not trustworthy context.

## 104. IAM filtering

IAM is a hard eligibility gate. A denied candidate is removed before ranking.

## 105. RBAC

RBAC can express broad organizational roles such as `analytics.reader`, `support.refund`, or `deployment.operator`.

## 106. ABAC

ABAC evaluates attributes such as:

```text
tenant
agent identity
delegated user
project
resource
region
purpose
data classification
risk
time
environment
```

## 107. Delegated user authority

When an agent acts on behalf of a user, bind the user, agent, action and destination into the authorization decision.

## 108. Confused-deputy defense

The router must not let a highly privileged agent use its own credentials to perform an operation the delegated user was not allowed to request.

## 109. Policy decision record

Persist enough information to reconstruct:

```json
{
  "decision": "ALLOW",
  "policy_version": "v42",
  "principal": "...",
  "delegated_user": "...",
  "capability_revision": "...",
  "reason_codes": ["PROJECT_MEMBER", "READ_ONLY"],
  "obligations": ["AUDIT", "REDACT_OUTPUT"]
}
```

## 110. Semantic policy

Semantic classifiers can label intent/risk, but deterministic IAM/policy remains final authority.

## 111. Risk classes

Example:

```text
LOW      read-only public/internal data
MEDIUM   bounded enterprise reads
HIGH     writes / mutations / deployments
CRITICAL money movement / privileged admin / destructive action
```

## 112. Human approval

For high-risk execution:

```text
selected capability
 + normalized arguments
 + principal
 + destination
 + policy version
      |
 canonical action hash
      |
 human approval
      |
 hash revalidation
      |
 execution
```

This prevents approval substitution.

## 113. Ranking architecture

Ranking only operates on eligible candidates.

```text
eligible candidate
   |
   + semantic relevance
   + schema fit
   + publisher/tool trust
   + health
   + latency utility
   + cost utility
   + quality
   + regional preference
   |
 normalized score
```

## 114. Hard constraints versus soft preferences

`max_cost`, required region, required permission, schema compatibility and minimum trust can be hard constraints. "Prefer lower latency" is normally a soft ranking preference.

## 115. Reference score

The runnable implementation uses a transparent weighted score. Production weights should be learned/tuned using offline evaluation and constrained by policy.

## 116. Trust score decomposition

Trust can include:

```text
publisher approval
supply-chain attestation
ownership
security review
incident history
data handling
protocol conformance
production maturity
```

Do not derive trust from semantic similarity.

## 117. Health score

Health should combine recent availability, error rate, timeout rate, p95/p99 latency, circuit state and probe freshness.

## 118. EWMA health

Exponentially weighted moving averages allow recent behavior to influence routing without making one transient failure dominate indefinitely.

## 119. Health freshness

A stale "healthy" signal is unsafe. Penalize or exclude candidates whose health data is too old.

## 120. Circuit breaker state machine

```text
CLOSED
  |
failure threshold
  v
OPEN
  |
cooldown
  v
HALF_OPEN
  | success -> CLOSED
  | failure -> OPEN
```

## 121. Bulkheads

Use separate concurrency pools by provider/tool class so a slow destination cannot exhaust all router workers.

## 122. Cost model

Cost may include direct API charge, query bytes, LLM tokens, egress, compute and internal chargeback.

## 123. Cost estimation

Estimate before execution when possible; record actual cost afterward and feed it into routing telemetry.

## 124. Latency model

Use operation/region-specific distributions. Static `expected_latency_ms` is only a bootstrap value.

## 125. Quality model

Quality can combine evaluator scores, task success, correctness metrics and bounded user feedback.

## 126. Feedback safety

Feedback may change ranking priors but can never expand permissions.

## 127. Fallback list

Keep a ranked list of eligible alternatives at decision time.

## 128. Fallback invariants

Fallback cannot:

```text
bypass IAM
change tenant
relax data classification
ignore required schema
cross prohibited region
skip required approval
```

## 129. Retry versus fallback

Retry the same tool for transient transport failures when safe. Fallback selects a different eligible capability.

## 130. Side effects

For writes, do not blindly fallback after ambiguous failure. The first tool may already have completed the action.

## 131. UNKNOWN outcome

Side-effecting execution can enter:

```text
UNKNOWN
```

when the network fails after dispatch and the router cannot determine whether the provider committed the action.

## 132. Reconciliation

A reconciliation adapter queries provider state using an idempotency key/resource ID and resolves `UNKNOWN` to succeeded, failed or safe-to-retry.

## 133. Idempotency

Generate stable idempotency keys from tenant, workflow/action and logical operation where provider semantics support it.

## 134. Credential broker

The model/router never receives long-lived raw credentials. A broker resolves short-lived credentials after capability selection and policy approval.

## 135. Credential scope

Credentials should be scoped to destination, action, resource and lifetime.

## 136. Credential caching

If credentials are cached, encrypt them, use very short TTLs and key them by identity/scope. Never place credentials in semantic indexes or logs.

## 137. MCP execution

A production MCP adapter handles the negotiated protocol version, headers, tool identity, input schema, authentication, timeouts, output validation and telemetry.

## 138. Stateless MCP

Modern stateless MCP requests can be independently routed, but the router should remain protocol-version aware rather than assume all servers behave identically.

## 139. MCP tool identity

Use stable server/tool identifiers plus revision/protocol metadata to prevent name collisions.

## 140. REST execution

REST adapters use allowlisted endpoint templates, allowed HTTP methods, strict redirects, DNS/IP validation, credential injection outside model-visible payloads and response schemas.

## 141. SSRF defense

Never allow a model-provided URL to become an arbitrary outbound request. Resolve logical endpoint IDs through approved registry metadata.

## 142. DNS rebinding

Resolve/validate network destinations at the enforcement layer and use controlled egress rather than relying only on string URL checks.

## 143. A2A execution

A2A delegation needs stable agent identity, task/message contracts, deadline propagation, cancellation, delegation depth and loop protection.

## 144. Delegation depth

Set a maximum hop count and include a visited-agent chain to prevent agent routing loops.

## 145. Deadline propagation

Every downstream call receives a deadline shorter than the parent request's remaining budget.

## 146. Cancellation

Cancellation should propagate to active downstream tool/agent calls where supported.

## 147. Gateway enforcement

Production execution should flow through an egress/gateway layer that enforces destination, identity, policy, credentials, quotas, content security and telemetry.

## 148. Content security

Inspect requests/results according to organizational policy for prompt injection, sensitive data, malware-like content or prohibited exfiltration.

## 149. Tool output is untrusted

A tool result can itself contain prompt injection. Keep tool content structurally separated from trusted system policy.

## 150. Tenant isolation

Trusted tenant identity scopes registry views, policy decisions, caches, health, telemetry and execution.

## 151. Cross-project governance

A centralized router may discover capabilities across projects, but explicit bindings/policy must authorize each relationship.

## 152. Data residency

Region is part of candidate eligibility. A cheaper tool in a prohibited region is not a valid fallback.

## 153. Routing cache

Cache discovery results using tenant, normalized requirement, registry version and embedding version.

## 154. Decision cache

Cache complete routing decisions only when policy, health and cost freshness requirements permit it.

## 155. Cache invalidation

Invalidate on:

```text
capability revision
policy update
binding change
health/circuit transition
deprecation
embedding migration
regional incident
```

## 156. Persistent registry

Production SQL should own normalized capability metadata and immutable revisions.

## 157. Transactional outbox

Registry updates and event intent commit in one SQL transaction.

## 158. Event topics

```text
registry.capability.created
registry.capability.revised
registry.capability.deprecated
policy.changed
binding.changed
health.changed
routing.feedback
```

## 159. Semantic indexer

An idempotent consumer converts approved capability revisions into vector documents.

## 160. Index reconciliation

Compare SQL active revisions with vector index revisions and repair drift.

## 161. Search degradation

If vector search fails, keyword/tag discovery can provide a reduced candidate set. Policy/schema enforcement remains unchanged.

## 162. Policy degradation

If authoritative policy cannot be evaluated, fail closed for protected tools.

## 163. Health degradation

If health telemetry is unavailable, use conservative defaults and avoid treating unknown health as excellent health.

## 164. Registry degradation

Cached approved metadata may be used for a bounded period if organizational policy permits; execution policy still applies.

## 165. Observability trace

A route trace should contain spans for:

```text
authenticate
normalize_requirement
registry_search
semantic_search
policy_filter
schema_filter
health_filter
rank
credential_resolve
gateway_execute
output_validate
fallback
audit
```

## 166. Metrics

Track:

```text
route requests
discovery latency
candidates before/after gates
IAM rejects
schema rejects
policy rejects
no-match rate
selected tool distribution
fallback rate
circuit state
execution latency
tool error rate
cost
quality
```

## 167. Audit record

Persist the selected capability/revision, principal, policy version, ranking feature summary, execution ID and result state.

## 168. Explainability

Explain why the selected tool won without revealing unauthorized alternatives.

## 169. Privacy-preserving telemetry

Do not log raw secrets, tokens or unnecessary customer payloads. Prefer hashes/IDs and classified structured fields.

## 170. OpenTelemetry

Propagate trace context through the gateway to downstream tools where supported.

## 171. SLO examples

Illustrative targets:

```text
routing availability              99.95%
p95 route decision latency        < 150 ms (cached/normal path)
policy decision availability      99.99%
audit completeness                100% for protected execution
registry projection freshness     < 30 s for 99%
```

Real targets depend on organization and workload.

## 172. Alerting

Alert on no-match spikes, IAM denial spikes, policy failures, outbox backlog, semantic-index lag, circuit storms, fallback spikes and cost anomalies.

## 173. Capacity model

Estimate:

```text
capabilities per tenant
capability revisions/day
route QPS
average candidates/route
policy checks/route
health updates/sec
execution QPS
telemetry retention
embedding dimensions
```

## 174. Horizontal scaling

Router API replicas are stateless. Scale discovery/ranking on request latency/QPS and event workers on lag.

## 175. Rate limiting

Separate limits for discovery, dry-run routing and actual execution.

## 176. Quotas

Support tenant, agent, user, capability and destination quotas for QPS, concurrency and spend.

## 177. Backpressure

Reject or queue before saturation. Preserve capacity for policy/health control traffic.

## 178. Priority

Interactive user routes may have different queues from background agent workloads.

## 179. Multi-region topology

```text
Global Agent
   |
Regional Router
   |
Regional Policy/Registry Cache
   |
Regional Gateway
   |
Allowed regional capabilities
```

## 180. Regional failover

Failover must re-evaluate residency and policy; do not automatically route to another geography.

## 181. Disaster recovery

Restore registry SQL/config, rebuild semantic index, reconnect policy, warm health conservatively, restore gateway connectivity and validate authorization before reopening execution.

## 182. Backup

Back up authoritative registry/policy metadata and audit according to organizational retention. Semantic indexes are rebuildable.

## 183. CI pipeline

```text
lint
unit tests
schema/property tests
policy tests
protocol contract tests
integration tests
security scans
SBOM
container scan
golden routing eval
```

## 184. Unit tests

Test scoring utilities, schema compatibility, policy gates and normalization independently.

## 185. Property tests

Important invariants:

```text
unauthorized candidate is never selected
schema-incompatible candidate is never selected
fallback is always policy eligible
higher semantic score cannot override IAM deny
tenant A cannot observe tenant B candidates
```

## 186. Golden routing tests

Create hundreds/thousands of requirements with expected eligible capability sets and expected top candidates.

## 187. Policy tests

Test user delegation, cross-project bindings, classifications, regions, high-risk approvals and denied destinations.

## 188. Protocol contract tests

Use mock MCP/REST/A2A servers to validate headers, timeouts, schemas, errors and idempotency behavior.

## 189. Security tests

Attempt SSRF, registry poisoning, prompt injection, schema smuggling, credential leakage, tenant spoofing and fallback bypass.

## 190. Load tests

Use realistic skew: popular tools receive much more traffic than long-tail capabilities.

## 191. Chaos tests

Kill semantic index, Redis/cache, policy adapter, registry, health collector and downstream providers independently.

## 192. Evaluation metrics

```text
Recall@K
MRR
Top-1 accuracy
Authorized Recall@K
Schema precision
Unsafe selection rate
No-match correctness
Fallback correctness
Task success
Cost/task
Latency/task
```

## 193. Shadow ranking

Run candidate ranking variants without executing them, compare decisions and outcomes, then promote only after evaluation.

## 194. A/B routing

For safe/read-only traffic, bounded experiments can compare ranking policies. Security eligibility is identical across variants.

## 195. Drift

Watch for changing user language, capability catalog growth, provider health and cost changes that degrade routing quality.

## 196. Application — enterprise analytics

An agent asks for "trusted customer revenue by region." Discovery may find warehouse, CRM and finance-agent capabilities; IAM/schema/policy narrow the set before cost/latency ranking.

## 197. Application — SRE

Route diagnostics to logs/metrics/traces while remediation/deployment tools require stronger roles and approvals.

## 198. Application — developer productivity

Dynamically discover code search, CI, repository, issue-tracker and test capabilities based on the engineering task.

## 199. Application — customer support

Discover CRM, knowledge, order and refund capabilities while enforcing customer scope and approval for refunds.

## 200. Application — finance

Prefer highly trusted audited versions and explicit approvals; do not optimize consequential actions primarily for cost.

## 201. Application — research

Discover search, document, database and specialist-agent capabilities while retaining source/tool provenance.

## 202. Application — multi-agent orchestration

The router can choose a specialist A2A agent when delegation is a better fit than a direct tool.

## 203. Application — migration

During provider migration, register old/new implementations under the same logical capability and canary the new revision.

## 204. Application — regional resilience

Choose among equivalent regional endpoints while preserving residency and authorization.

## 205. ADK integration pattern

Expose one stable orchestration tool to ADK:

```text
discover(requirement)
route(requirement, arguments)
execute(route_id)
```

or a combined `discover_and_execute` for lower-risk workflows.

## 206. Two-phase routing

For high-risk actions, prefer:

```text
discover + explain
      |
human / planner confirms
      |
execute exact route/action hash
```

## 207. Dry-run API

A production router should expose a no-execution route endpoint for planning, debugging and audit.

## 208. Suggested production APIs

```text
POST /v1/discover
POST /v1/routes
GET  /v1/routes/{id}
POST /v1/routes/{id}:execute
POST /v1/routes/{id}:approve
POST /v1/routes/{id}:cancel
GET  /v1/capabilities/{id}
GET  /v1/capabilities/{id}/revisions
GET  /v1/health
GET  /v1/audit
```

## 209. API idempotency

Mutation/execution APIs accept idempotency keys and return stable execution IDs.

## 210. Error taxonomy

```text
NO_CAPABILITY
POLICY_DENIED
SCHEMA_INCOMPATIBLE
REGION_DENIED
COST_LIMIT
TRUST_LIMIT
TOOL_UNHEALTHY
APPROVAL_REQUIRED
CREDENTIAL_FAILURE
EXECUTION_TIMEOUT
EXECUTION_UNKNOWN
OUTPUT_INVALID
```

## 211. Code walkthrough — `domain.py`

Defines the typed requirement, capability, principal and route-result contracts that keep model-facing intent separate from provider-specific execution.

## 212. Code walkthrough — `registry.py`

Provides the normalized local catalog used by the runnable implementation. Production replaces/augments it with Agent Registry, MCP/OpenAPI/A2A ingestors.

## 213. Code walkthrough — `embeddings.py`

Implements deterministic local embeddings so the project runs offline. This is a development adapter, not a claim of production semantic quality.

## 214. Code walkthrough — `discovery.py`

Builds candidate sets from requirement/capability representations before deterministic gates.

## 215. Code walkthrough — `schema.py`

Checks whether the requirement arguments are compatible with a capability contract.

## 216. Code walkthrough — `policy.py`

Performs authorization/risk eligibility. Its placement before ranking is an intentional security invariant.

## 217. Code walkthrough — `ranking.py`

Combines semantic, schema, trust, health, latency and cost into an explainable score for already-eligible candidates.

## 218. Code walkthrough — `executors.py`

Contains provider-neutral MCP/REST/A2A execution boundaries. Organization-specific credentials and gateway configuration remain deployment adapters.

## 219. Code walkthrough — `router.py`

Orchestrates discovery -> policy -> schema -> ranking -> execution/fallback.

## 220. Code walkthrough — `api.py`

Exposes the HTTP interface for catalog inspection and routing.

## 221. Code walkthrough — `models.py`

Provides persistent-model foundations for capability and routing metadata where the reference uses SQL.

## 222. Code walkthrough — `db.py`

Owns SQLAlchemy engine/session configuration.

## 223. Code walkthrough — `config.py`

Centralizes environment-driven configuration.

## 224. Code walkthrough — `main.py`

Bootstraps the FastAPI service and health endpoint.

## 225. Docker architecture

The included Compose environment is intended for local validation. It starts the router and its local persistence/cache dependencies without requiring Google credentials.

## 226. Local run — Docker

```bash
unzip agent-tool-discovery-semantic-router-comprehensive.zip
cd agent-tool-discovery-semantic-router

cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
```

## 227. Inspect demo catalog

```bash
curl \
  -H 'x-api-key: change-me' \
  http://localhost:8000/v1/tools
```

## 228. Route example

```bash
curl -X POST http://localhost:8000/v1/route \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/route.json
```

## 229. Host development

```bash
docker compose up -d postgres redis

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"

# Update DATABASE_URL/REDIS_URL hostnames in .env to localhost.

uvicorn app.main:app --reload
```

## 230. Run tests

```bash
pytest -q
ruff check .
```

## 231. Inspect database

```bash
docker compose exec postgres \
  psql -U postgres -d router
```

Use `\dt` to inspect the tables present in the current implementation.

## 232. View logs

```bash
docker compose logs -f api
docker compose logs -f postgres
docker compose logs -f redis
```

## 233. Stop local environment

```bash
docker compose down
```

Use `docker compose down -v` only when you intentionally want to remove local persistent volumes.

## 234. Kubernetes starter

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/api.yaml
```

These manifests are starter deployment artifacts, not a claim of a complete hardened enterprise cluster.

## 235. Production Kubernetes

Add workload identity, Services, ConfigMaps, managed secrets, HPA, PDB, NetworkPolicies, topology spread, ingress/service mesh, OTel collector and managed SQL/vector/event dependencies.

## 236. Network policy

Router pods should normally reach only approved registry/policy/gateway/telemetry dependencies. Direct unrestricted internet egress undermines gateway enforcement.

## 237. Non-root runtime

Use non-root containers, read-only filesystem, seccomp and dropped Linux capabilities.

## 238. Supply chain

Generate SBOMs, pin base images/dependencies, scan images, sign artifacts and verify signatures/admission policy.

## 239. Production readiness matrix

| Concern | Runnable reference | Production target |
|---|---|---|
| Natural-language requirement | Yes | Typed/versioned API |
| Local capability catalog | Yes | Agent Registry + enterprise ingestors |
| Semantic discovery | Deterministic offline embeddings | Versioned production embeddings/vector index |
| Schema checks | Yes | Full JSON Schema/OpenAPI/MCP contract validation |
| IAM gate | Reference policy | Agent Identity/IAM/ABAC |
| Ranking | Yes | Evaluation-tuned feature model |
| Trust/health/cost | Metadata-based | Dynamic collectors + policy |
| MCP/REST/A2A | Execution boundaries | Gateway-mediated protocol adapters |
| Credentials | Deployment boundary | Short-lived credential broker |
| Fallback | Reference flow | Circuit/idempotency/reconciliation aware |
| Telemetry | Architecture | OpenTelemetry + metrics + immutable audit |
| Persistence | SQL foundations | Alembic + HA managed SQL |
| Eventing | Architecture | Outbox + Kafka/Pub/Sub consumers |
| Kubernetes | Starter | Hardened Helm/platform |
| Multi-region | Architecture | Residency-aware regional control plane |

## 240. Production implementation sequence

```text
1. trusted OIDC / workload identity
2. Agent Registry adapter
3. normalized persistent capability revisions
4. Alembic migrations
5. production embedding + vector index
6. OpenAPI/MCP/A2A ingestors
7. IAM/RBAC/ABAC policy adapter
8. Agent Gateway execution
9. short-lived credential broker
10. dynamic health collector
11. circuit breakers / bulkheads
12. persistent route/execution records
13. idempotency / UNKNOWN / reconciliation
14. high-risk approval service
15. outbox + event consumers
16. telemetry / OTel / immutable audit
17. quotas / budgets / rate limiting
18. evaluation and shadow ranking
19. hardened Kubernetes / Helm
20. regional DR and chaos exercises
```

## 241. Principal-level questions


```text
Why does IAM run before ranking?
Why isn't semantic similarity enough for tool selection?
How do you prevent registry poisoning?
How do you normalize MCP, REST and A2A capabilities?
How do you compare trust, health, cost and latency?
How do you prevent fallback from bypassing authorization?
What happens when a side-effecting tool times out after dispatch?
How do you reconcile UNKNOWN execution?
How do you re-embed millions of capabilities without downtime?
How do you handle policy/registry/vector outages?
How do you preserve regional residency during failover?
How do you audit a dynamic decision deterministically?
How do you evaluate routing quality offline?
How do you prevent a tool response from prompt-injecting the agent?
```

## 242. Design trade-off — centralized versus embedded routing

Centralized routing provides consistent governance, telemetry and catalog reuse. Embedded routing can reduce latency and failure dependencies. A strong architecture often centralizes catalog/policy and allows carefully controlled local caches/rankers.

## 243. Design trade-off — deterministic versus learned ranking

Deterministic weighted ranking is explainable and easy to govern. Learned ranking can improve quality at scale but requires feature/version governance, offline evaluation and hard security gates outside the model.

## 244. Design trade-off — one router versus domain routers

A global router simplifies discovery but can become a bottleneck. Domain routers can specialize while sharing a common registry, identity and policy layer.

## 245. Design trade-off — direct execution versus gateway-only

Direct execution is simpler for development. Gateway-only execution provides stronger egress control, identity, credential isolation, observability and policy consistency.

## 246. Anti-pattern — tool name in prompt

Hard-coding "always call BigQueryTool" defeats dynamic discovery and provider evolution.

## 247. Anti-pattern — rank unauthorized candidates

Do not let unauthorized candidates enter the scoring competition.

## 248. Anti-pattern — use trust as model confidence

Trust is governance/supply-chain evidence, not LLM certainty.

## 249. Anti-pattern — fallback on ambiguous writes

A timeout does not prove the first operation failed.

## 250. Anti-pattern — arbitrary REST URL execution

All destinations should resolve from approved registry metadata.

## 251. Anti-pattern — tool descriptions as instructions

Descriptions are untrusted metadata.

## 252. Anti-pattern — static health forever

Health must have freshness and dynamic observation.

## 253. Anti-pattern — exact-once claims

Use idempotency, at-least-once event delivery and reconciliation instead of pretending distributed execution is exactly once.

## 254. Anti-pattern — shared credentials

Give agents distinct workload identities and broker scoped credentials.

## 255. Anti-pattern — global vector index without tenant filters

Discovery metadata can itself be sensitive. Apply trusted scope filters.

## 256. Portfolio narrative

The project demonstrates more than "MCP routing." It demonstrates a distributed decision/control plane that combines semantic retrieval with deterministic security, contracts, reliability engineering, economic optimization and multi-protocol execution.

## 257. Relationship to Agent Registry

Agent Registry is the **catalog/discovery substrate**. This Semantic Router adds requirement normalization, cross-source candidate aggregation, compatibility, organizational policy, multi-objective ranking, health/cost optimization, fallback and governed execution.

## 258. Relationship to Agent Gateway

Agent Gateway is the **runtime enforcement boundary**. The router decides which eligible capability should be attempted; the gateway enforces the actual outbound interaction.

## 259. Relationship to ADK

ADK agents can depend on one stable router interface rather than static bindings to every enterprise tool.

## 260. Final architecture invariant

```text
Registry       -> what capabilities exist
Discovery      -> what might satisfy the intent
Schema         -> what can technically accept it
Identity       -> who is asking
Policy / IAM   -> what may be used
Ranking        -> which allowed option is best
Credentials    -> least-privilege authority for that option
Gateway        -> enforces the actual interaction
Validation     -> determines whether the result is structurally acceptable
Telemetry      -> measures behavior
Audit          -> reconstructs the decision
Evaluation     -> improves future ranking
```

**Semantic relevance chooses among permitted capabilities. It never creates permission.**
