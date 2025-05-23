# Code Style Guide

> *“Build practical systems first—then polish, harden, and scale.”*

This document distills recurring patterns from our codebases and previous internal style guides into one **unified reference**.  Treat it as the **single source of truth** for day‑to‑day engineering decisions.  Updates are welcome via PR.

---

## 1. Guiding Principles

| Principle                      | What It Means in Practice                                                                           |
| ------------------------------ | --------------------------------------------------------------------------------------------------- |
| **Practicality > Purity**      | Ship working code quickly, refine later. Prefer simple solutions over clever abstractions.          |
| **Explicit > Implicit**        | Make data flow, assumptions, and configuration visible in code—not hidden in magic or global state. |
| **Fail Fast, Recover Cleanly** | Detect problems early in dev; add structured retries and graceful fallbacks in prod.                |
| **Observability by Default**   | Every critical path emits actionable logs/metrics. No silent failures.                              |
| **Config‑Driven Design**       | Behavior, limits, and secrets live in YAML/ .env—not in code.                                       |
| **Modular & Composable**       | Small functions, clear interfaces, layered responsibilities.  Enable plug‑and‑play.                 |
| **Human‑in‑the‑Loop Ready**    | Design pipelines so people can inspect, override, and iterate (e.g., clustering, model outputs).    |

---

## 2. Project Layout

```
repo_root/
│
├── sharp.py              # Thin orchestrator
├── tasks/                # Top‑level user intents
│   └── <task>/run.py     # Each exposes `run(**kwargs)` with docstring contract
├── config/               # YAML + .env templates
├── tr/server/            # Flask routes & Jinja templates
│   └── templates/
└── tests/                # Pytest suites mirror src structure
```

* **One responsibility per folder**. Don’t mix API handlers with business logic.
* **Docstrings at module top** explain intent, deps, and env vars.

---

## 3. Python Coding Conventions

### 3.1 Naming

| Kind        | Style           | Example                  |
| ----------- | --------------- | ------------------------ |
| Module/File | `snake_case.py` | `gpu_router.py`          |
| Function    | `snake_case`    | `get_smart_gpu_server()` |
| Variable    | `snake_case`    | `active_requests`        |
| Constants   | `UPPER_SNAKE`   | `TARGET_TOPICS = 50`     |
| Class       | `CamelCase`     | `GpuHealthChecker`       |

### 3.2 Imports

```python
# Standard lib
import os
import logging

# 3rd‑party
import requests
from tenacity import retry

# Local
from tasks.video_misinfo.run import run
```

* **Never use wildcard imports.**
* Sort with *isort* profile `black`.

### 3.3 Formatting

* **Black** (line length `120`).
* **isort** for import order.
* **ruff** ruleset `pyproject.toml`.

### 3.4 Typing & Docstrings

* Annotate public interfaces and critical helpers.
* Google‑style docstrings:

```python
def allocate_topics(df: pd.DataFrame, target: int) -> list[str]:
    """Rank and return *target* topics by frequency.

    Args:
        df: Pre‑filtered DataFrame with a ``topic`` column.
        target: Desired number of topics.

    Returns:
        Ordered list of topic strings (len == ``target``).
    """
```

Use python 3.9 style typing i.e.

`def extract_and_save_code_block(project_name: Union[str, None] = None) -> str:`

NOT
`def extract_and_save_code_block(project_name: str | None = None) -> str:`

---

## 4. Error Handling & Logging

| Rule                                    | Snippet / Pattern                                                                                  |
| --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Guard inputs early                      | `if not usernames or not isinstance(usernames, list): return error(400, "usernames must be list")` |
| Use built‑in exceptions sparingly       | `raise ValueError("model unsupported")`                                                            |
| Structured retries with *tenacity*      | `@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))`                                           |
| Milestone logs (`INFO`)                 | `logging.info("[router] Loaded %s models", len(models))`                                           |
| Unusual but non‑fatal state (`WARNING`) | `logging.warning("GPU %s exceeded usage", gpu_key)`                                                |
| Unexpected fatal (`ERROR`) with context | Include **key vars** (host, port, request\_id)                                                     |

---

## 5. Concurrency & Parallelism

| Scenario               | Guidance                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------ |
| I/O bound (HTTP calls) | `ThreadPoolExecutor`, max workers from `config.server.max_connections`.              |
| CPU bound              | Prefer external process (Spark) or vectorized pandas; avoid Python threads.          |
| Long‑running services  | Supervise with health‑check thread (`is_serving()`), restart via `subprocess.Popen`. |
| Cancellation           | After success condition, iterate `for f in futures: f.cancel()` to free GPU.         |

---

## 6. Configuration Management

1. **Priority order**: `config/*.yaml` → `.env` → hard‑coded defaults.
2. Load once at startup, expose via `pydantic.BaseSettings` for validation.
3. Never write back to YAML from code.
4. Document every var in `docs/config_reference.md`.

---

## 7. Data Handling

* Use **pandas** for in‑memory transforms ≤ 1 M rows; push heavy joins to **Spark / SQL**.
* Keep DataFrame column names `snake_case`.
* Avoid chained indexing; prefer `.loc` / `.assign`.
* In Spark, tune with:

  * `spark.sql.shuffle.partitions` (default 200 → 800 for large shuffles).
  * Enable `dynamicAllocation.shuffleTracking` if needed.

---

## 8. Web & API Development (Flask)

| Topic           | Rule / Example                                                   |
| --------------- | ---------------------------------------------------------------- |
| Routing         | `/amd_sharp/v1/<model>` maps directly to task folder.            |
| HTTP verbs      | Separate `GET` vs `POST` blocks; no mixed logic.                 |
| Validation      | Early bail‑out with 4xx JSON errors.                             |
| Response schema | Always `{ "status": "ok", "data": … }` or `{ "error": "msg" }`.  |
| CORS & Security | Default deny; enable only what’s needed.                         |
| Gunicorn        | `--worker-class gevent --worker-connections 1000 --timeout 120`. |

---

## 9. Infrastructure & Ops

### 9.1 Redis Key Design

```
sharp_gpu_usage_<host>_<port>     -> JSON blob
sharp_latency_<host>_<port>       -> ZSET of (timestamp, latency_ms)
sharp_active_<host>_<port>        -> INT counter
```

* **Namespace clearly.** No bare keys.
* Provide TTL where appropriate (e.g., latency window 15 min).

### 9.2 GPU Self‑Healing

* Monitor `memory_used / memory_total > 0.95` for 3 min → restart model.
* Use `nvidia-smi --query-gpu=... --format=csv,noheader` in health thread.

---

## 10. LLM & Inference

* Split into **requestor → router → GPU server**.
* Warm preferred models at GPU server startup.
* Use `tenacity` retry w/ jitter on network timeouts.
* Enforce structured prompts & responses (JSONMode) for downstream parsing.

---

## 11. Testing & CI

| Tool           | Purpose                                 |
| -------------- | --------------------------------------- |
| **pytest**     | Unit and integration tests.             |
| **ruff**       | Lint; run with `ruff check --fix .`.    |
| **pre‑commit** | Enforce black/isort/ruff on commits.    |
| **GitHub CI**  | Run test + lint matrix on Python 3.10+. |

---

## 12. Commit & PR Etiquette

1. Small, focused commits; imperative mood (`Fix GPU health restart race`).
2. PR template must include **context**, **screenshots/logs**, and **roll‑back plan**.
3. At least one reviewer outside author’s team.
4. CI **must pass** before merge.

---

## 13. Appendix

### 13.1 Example Config Precedence

```yaml
# config/default.yaml
max_connections: 50
```

```dotenv
# .env
MAX_CONNECTIONS=100
```

In Python:

```python
class Settings(BaseSettings):
    max_connections: int = 25  # fallback

settings = Settings(_env_file=".env", _secrets_dir="config")
```

*Effective value → `100`*

### 13.2 Sample Logging Config (YAML)

```yaml
version: 1
formatters:
  concise:
    format: "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
handlers:
  console:
    class: logging.StreamHandler
    formatter: concise
root:
  level: INFO
  handlers: [console]
```

---

### Keep It Evolving 🚀

If you hit patterns not covered here, propose an addition via PR.  Our best code is the code we can **understand, test, and safely change**.
