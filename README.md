# ShopFlow — CodeAtlas Demonstration Repository

**ShopFlow** is a compact, multi-module Python e-commerce microservice built specifically to demonstrate all core capabilities of **CodeAtlas**:
- **Code Graph Visualisation**: Clear inter-module dependencies and function call trees.
- **Hybrid & Semantic Search**: Rich docstrings and typed functions for vector retrieval.
- **Code Intelligence Tools**: Function explanations and automated unit test generation.
- **Bug Finder & Code Review**: Three deterministic, planted bugs with clear root causes.
- **Duplicate Code Finder**: Near-identical shipping calculation functions with $>85\%$ similarity.

---

## 📂 Repository Layout

```
shopflow/
├── shopflow/
│   ├── __init__.py
│   ├── models.py          # Data models: Customer, Item, Order
│   ├── discounts.py       # Planted Bug 1: ZeroDivisionError in tier discount
│   ├── payments.py        # Planted Bug 2: TypeError with unhandled NoneType tax
│   ├── inventory.py       # Planted Bug 3: Mutable default argument leaking state
│   ├── shipping.py        # Planted Duplicates: standard vs express shipping (>85% match)
│   └── order_service.py   # High-level orchestrator connecting all modules
├── tests/
│   ├── __init__.py
│   ├── test_discounts.py  # Failing test reproducing Bug 1
│   ├── test_payments.py   # Failing test reproducing Bug 2
│   ├── test_inventory.py  # Failing test reproducing Bug 3
│   └── test_shipping.py   # Passing tests for shipping
├── requirements.txt
└── README.md
```

---

## 🪲 The 3 Planted Bugs & Deterministic Error Traces

### Bug 1: VIP Tier 1 Zero-Division Error
* **File**: `shopflow/discounts.py`
* **Function**: `apply_tier_discount(order_total, tier_level)`
* **The Root Cause**: 
  The formula divides by `(tier_level - 1)` to compute the tier bonus. When a Bronze VIP (`tier_level = 1`) checks out, it divides by zero.
* **Failing Test**: `tests/test_discounts.py::test_bronze_tier_discount_planted_bug`
* **Exact Error Message**:
  ```
  ZeroDivisionError: division by zero
  >   tier_bonus = 0.05 / (tier_level - 1)
  E   ZeroDivisionError: division by zero
  ```
* **Correct Fix**:
  ```python
  # Safe rate calculation
  base_rate = 0.05 * tier_level
  ```

---

### Bug 2: NoneType Currency / Tax Multiplier Crash
* **File**: `shopflow/payments.py`
* **Function**: `process_payment(amount, currency, user_profile)`
* **The Root Cause**:
  The function accesses `user_profile.get("tax_rate")` without a default value or `None` check. Guest checkouts or profiles without explicit tax settings return `None`, crashing when multiplied with `amount`.
* **Failing Test**: `tests/test_payments.py::test_guest_payment_tax_planted_bug`
* **Exact Error Message**:
  ```
  TypeError: unsupported operand type(s) for *: 'float' and 'NoneType'
  >   tax_amount = amount * tax_rate
  E   TypeError: unsupported operand type(s) for *: 'float' and 'NoneType'
  ```
* **Correct Fix**:
  ```python
  tax_rate = user_profile.get("tax_rate") or 0.0
  ```

---

### Bug 3: Mutable Default Argument State Leakage
* **File**: `shopflow/inventory.py`
* **Function**: `reserve_stock(item_id, quantity, reserved_list=[])`
* **The Root Cause**:
  In Python, default arguments are evaluated once at function definition time. Reusing the default list across multiple calls mutates the identical list object in memory, contaminating separate customer orders.
* **Failing Test**: `tests/test_inventory.py::test_stock_reservation_isolation_planted_bug`
* **Exact Error Message**:
  ```
  AssertionError: assert 2 == 1
  + where 2 = len([('item_101', 2), ('item_101', 3)])
  ```
* **Correct Fix**:
  ```python
  def reserve_stock(item_id: str, quantity: int, reserved_list: Optional[list] = None) -> list:
      if reserved_list is None:
          reserved_list = []
  ```

---

## 👯 Planted Duplicate Code (For Duplicate Finder Demo)
* **File**: `shopflow/shipping.py`
* **Functions**: `calculate_standard_shipping` and `calculate_express_shipping`
* **Structure**: Both functions share identical line count, variable names, fragility checks, and rounding logic, varying only in base and multiplier rates.
* **CodeAtlas Detection**:
  In the **Analyse** tab, clicking **Find Duplicates** flags these two functions with **>85% structural similarity**.

---

## 🎬 Step-by-Step Live Demo Script

Follow this structured script during your evaluation:

### Act 1: Terminal Demonstration (Failing Baseline)
1. Open PowerShell or terminal in the demo repository directory.
2. Run pytest to show the 3 failing tests:
   ```powershell
   $env:PYTHONPATH="."; pytest tests/
   ```
3. Highlight to the evaluators:
   - 4 tests pass (`test_coupon_discount`, `test_gold_tier_discount`, `test_card_validation`, `test_availability_check`, shipping tests).
   - Exactly 3 tests fail deterministically with clear tracebacks.

### Act 2: Fresh Ingestion into CodeAtlas
1. Launch CodeAtlas via `start.bat`.
2. Open the web interface at `http://localhost:5173`.
3. In the sidebar or top bar, click **Import Repository**.
4. Enter the repository URL (or local Git URL).
5. Watch the real-time status pill transition:
   $$\text{cloning} \longrightarrow \text{scanning} \longrightarrow \text{parsing} \longrightarrow \text{indexing} \longrightarrow \text{ready}$$
6. Notice the instant indexing completed via local FastEmbed.

### Act 3: Visual Codebase Mapping (Map Tab)
1. Switch to the **Map** tab.
2. Demonstrate the **File Dependency Map**:
   - Point out how `order_service.py` is the central hub connected to `models.py`, `discounts.py`, `inventory.py`, `shipping.py`, and `payments.py`.
   - Click and drag nodes to demonstrate the spring-force physics simulation.
3. Switch to the **Function Call Graph**:
   - Show how `checkout_order()` links directly to `apply_tier_discount()`, `reserve_stock()`, and `process_payment()`.

### Act 4: Hybrid Search & Retrieval (Search Tab)
1. Navigate to the **Search** tab.
2. Search for: `"calculate discount for VIP tier"`.
3. Highlight that CodeAtlas uses **Hybrid Search** (combining FAISS vector semantic similarity + BM25 lexical token match + AST symbol match via Reciprocal Rank Fusion).
4. Notice `apply_tier_discount` in `shopflow/discounts.py` ranked #1 with matching code snippet and line numbers.

### Act 5: AI Code Intelligence (Analyse Tab)
1. Navigate to the **Analyse** tab.
2. **Bug Review**:
   - Select `shopflow/discounts.py` and choose `apply_tier_discount`.
   - Click **Run Bug Audit** / **Review Code**.
   - Show how the AI immediately detects the potential `ZeroDivisionError` when `tier_level == 1`.
   - Repeat for `process_payment` to see the unhandled `NoneType` tax warning.
3. **Duplicate Finder**:
   - Click **Find Duplicates**.
   - Show the detected pair: `calculate_standard_shipping` and `calculate_express_shipping` with **~88% similarity**.
4. **Generate Tests**:
   - Select `calculate_coupon_code` or `calculate_standard_shipping` and click **Generate Tests**.
   - Show production-ready `pytest` unit tests generated on the fly.

### Act 6: Interactive Q&A Copilot (Ask Tab)
1. Navigate to the **Ask** tab.
2. Ask the assistant:
   > *"Explain the end-to-end checkout flow in ShopFlow and what dependencies are required for inventory reservation."*
3. Show the LLM's cited references to `shopflow/order_service.py` and `shopflow/inventory.py`.

---

## 🛠️ Verification Commands

```powershell
# Run all tests (3 should fail deterministically)
python -m pytest tests/

# Run single test for Bug 1
python -m pytest tests/test_discounts.py -k "test_bronze_tier_discount_planted_bug"

# Run single test for Bug 2
python -m pytest tests/test_payments.py -k "test_guest_payment_tax_planted_bug"

# Run single test for Bug 3
python -m pytest tests/test_inventory.py -k "test_stock_reservation_isolation_planted_bug"
```

