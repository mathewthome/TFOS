# ADR-002: Transaction-Based Data Architecture

**Version:** TFOS v0.1  
**Status:** Accepted  
**Date:** 2026-08-07  
**Author:** TFOS Development Team  
**Mandatory:** Yes — All future development must comply

---

## Title

Transaction-Based Data Architecture

---

## Purpose

To establish a transaction-based data model for TFOS that ensures complete historical accuracy, enables unlimited reporting capabilities, supports full audit trails, and provides the foundation for future analytics and decision support.

---

## Context

Farm operations involve dozens of financial and operational transactions daily. Traditional approaches store year-end summaries (total costs per field, total revenue, etc.) as the primary data source. This approach has fundamental limitations:

1. **Lost Detail:** Once summarized, individual transaction details are gone forever
2. **Audit Trail Gaps:** Cannot trace specific transactions back to source documents
3. **Historical Reporting Limitations:** Cannot restate prior years or analyze transaction patterns
4. **Import Conflicts:** John Deere Operations Center provides transaction-level data; storing only summaries requires discarding source information
5. **Corrections Difficult:** Fixing a mistake means adjusting the summary, losing the original record
6. **Analytics Impossible:** Cannot perform detailed analysis without transaction-level data
7. **Compliance Risk:** Financial audits and tax authorities expect transaction-level documentation

TFOS v0.1 shall establish the correct architecture from day one: **permanent transaction storage with derived summaries**.

---

## Decision

TFOS shall implement a transaction-based data architecture with the following principles:

### Core Principle: Transaction Permanence

**Every business transaction shall be recorded exactly once and never overwritten.**

Transactions are the atomic unit of the financial system. Once recorded, a transaction is immutable. Corrections are handled through adjusting transactions, preserving the complete audit trail.

### Transactions Include

TFOS shall capture transactions for all material business activities:

#### **Operational Transactions**
- **Harvest Records** — Yields, moisture, test weight, quality metrics
- **Planting Records** — Acres planted, varieties, seeding rates, dates
- **Chemical Applications** — Herbicides, insecticides, fungicides with rates and acres
- **Fertilizer Applications** — Liquid or dry, rates, and timing
- **Fuel Purchases** — Diesel, gasoline, propane acquisitions and costs
- **Equipment Repairs** — Maintenance, repairs with parts and labor
- **Equipment Purchases** — Capital equipment acquisitions with cost and date

#### **Financial Transactions**
- **Grain Sales** — Bushels sold, price, date, total revenue
- **Grain Deliveries** — Bushels delivered to storage/customers
- **Loan Payments** — Principal and interest payments to lenders
- **Loan Disbursements** — New loans or loan advances received
- **Operating Expenses** — Seeds, chemicals, supplies, utilities, contracted services
- **Equipment Rentals** — Custom services, equipment rental payments
- **Insurance Payments** — Crop insurance premiums, property insurance
- **Insurance Claims** — Claims received and proceeds

#### **Personal Financial Transactions**
- **Family Withdrawals** — Distributions to owner for personal use
- **Family Income** — Off-farm income, dividends, interest
- **Retirement Contributions** — Contributions to retirement accounts
- **Tax Payments** — Estimated taxes, final taxes, state taxes
- **Personal Expenses** — Family living expenses, medical, education

### Transaction Structure

Every transaction in TFOS shall contain the following fields:

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| **TransactionID** | UUID/Text | Yes | Unique identifier (never reused) |
| **TransactionDate** | Date | Yes | Date transaction occurred |
| **CropYear** | Integer | Yes | Crop year for agricultural transactions (YYYY) |
| **Category** | Text | Yes | Top-level classification (Grain Sales, Fertility, Equipment, etc.) |
| **Subcategory** | Text | Yes | Detailed classification (Corn Sales, Urea Application, Repair Labor, etc.) |
| **RelatedEntityID** | Text | Yes | Foreign key (FieldID, EquipmentID, LoanID, etc.) |
| **Description** | Text | Yes | Human-readable description of transaction |
| **Amount** | Currency | Yes | Monetary value (positive = inflow, negative = outflow) |
| **Units** | Decimal | No | Physical quantity (bushels, gallons, pounds, hours, etc.) |
| **UnitType** | Text | No | Unit label (bu, gal, lb, hr, acre) |
| **Source** | Text | Yes | Data source (Manual, JD Ops Center, Imported, Calculated) |
| **SourceReference** | Text | No | External reference (invoice number, Ops Center record ID) |
| **CreatedDate** | DateTime | Yes | When record was entered |
| **CreatedBy** | Text | Yes | Who entered the record |
| **Notes** | Text | No | Additional context or justification |

### Transaction Types

#### **Primary Transactions** (Original, immutable records)
- Entered once
- Never modified
- Form the permanent audit trail
- Examples: Harvest records from Ops Center, grain sales invoices, loan payment confirmations

#### **Adjusting Transactions** (Corrections and additions)
- Created when errors are discovered
- Reference the original transaction being corrected
- Include explanation of adjustment
- Preserves complete history
- Examples: "Correction to Harvest Record HRV-2026-0147", "Adjustment to grain moisture test"

### Reporting Architecture

**Summary data is calculated from transactions, never stored as primary data.**

#### **Consolidation Tables** (Derived from transactions)
- **Grain Revenue by Field** — Sum of all grain sales transactions by field and crop year
- **Fertility Costs by Field** — Sum of all fertilizer application costs by field
- **Equipment Costs by Field** — Allocation of repair and depreciation costs
- **Field Profitability** — Revenue minus all allocated costs, calculated annually

#### **Financial Statements** (Derived from transactions)
- **Income Statement** — Revenue and expense totals by category
- **Cash Flow Statement** — Cash inflows and outflows by period
- **Balance Sheet** — Assets, liabilities, equity derived from transaction history

#### **Dashboards** (Derived from consolidations)
- **Executive Summary** — KPIs calculated from consolidated data
- **Field Performance** — Yield, profitability, ROI by field
- **Financial Health** — Debt ratios, cash position, net worth trends

**Key Principle:** Every report number is traceable back to underlying transactions.

### Data Integrity Rules

1. **Transaction Immutability** — Once created, a transaction cannot be edited or deleted
2. **Adjustments Only** — Corrections are entered as new adjusting transactions
3. **Referential Integrity** — Every transaction references valid master data (FieldID exists in tblFields)
4. **Date Consistency** — TransactionDate must fall within the stated CropYear
5. **Amount Validation** — Transactions must be reasonable; extreme outliers flagged for review
6. **Source Documentation** — Every transaction includes source reference or explanation

### Historical Data Preservation

**TFOS shall maintain complete, permanent transaction history.**

- No transaction deletion (ever)
- No transaction archiving to separate systems
- No data purging at year-end
- Entire transaction history available for analysis at any time
- Multi-year reporting, trend analysis, and year-over-year comparisons all possible

---

## Benefits

### Complete Audit Trail
- Every transaction is permanently recorded with creation date, creator, and source
- Regulators, auditors, and lenders can verify any number to its source
- Disputes resolved by referencing original documentation
- Tax compliance supported by detailed transaction history

### Unlimited Historical Reporting
- Multi-year trend analysis (e.g., "How has our corn yield changed over 5 years?")
- Year-over-year comparisons (e.g., "2026 costs vs. 2025 same period")
- Historical reconstruction (e.g., "What would profit have been under different pricing?")
- Successor farmer can understand complete historical performance

### Future Analytics Support
- Machine learning models can analyze patterns in transaction history
- Predictive analytics can forecast based on historical performance
- Optimization algorithms can analyze cost structures and identify inefficiencies
- Benchmarking against historical data becomes possible

### Accurate Field Profitability
- Every cost transaction is allocated to specific fields
- Profitability is calculated from detailed cost and revenue transactions
- No guessing or averaging; actual costs and yields per field
- Identifies truly profitable vs. marginal fields

### Accurate Financial Statements
- Balance sheet built from transaction history (not manual account balancing)
- Income statement sums all revenue and expense transactions
- Cash flow statement derived from actual cash transactions
- Discrepancies identified immediately (actual vs. assumed)

### Easy Import from John Deere Operations Center
- Ops Center provides transaction-level data (harvest record, planting record, etc.)
- Direct import into tblHarvestImport, tblPlantingImport, etc.
- No data loss or aggregation during import
- Updates to Ops Center data reflected through adjusting transactions

### Scalable Architecture
- As farm grows (more fields, crops, equipment), transaction model scales naturally
- Adding new transaction types requires only new category entries, not schema changes
- Multi-year analysis doesn't require different tables per year
- Historical data doesn't degrade system performance

### Regulatory & Compliance Support
- FSA, USDA, crop insurance, lenders all expect transaction-level documentation
- Commodity futures margins and risk management calculations based on transaction history
- Tax planning supported by detailed expense tracking
- Succession planning and valuation based on complete financial history

---

## Tradeoffs

### Larger Database

**Tradeoff:** Storing every transaction requires more storage than storing only yearly summaries.

**Data Volume Analysis:**
- Typical Midwest corn/soybean farm: ~500 acres
- Estimated annual transactions: 300-500 (planting, applications, harvest, sales, expenses)
- Per-transaction storage: ~500 bytes
- Annual data: 150-250 KB
- 10-year history: 1.5-2.5 MB
- Excel capacity: 1M+ rows → No practical issue for TFOS v0.1

**Mitigation:**
- Excel worksheet can store 1,048,576 rows (far beyond farming transaction volume)
- No performance degradation for anticipated data volumes (< 50,000 rows)
- Future: Migration to database removes storage concerns entirely
- Compression and archiving strategies available if needed

### Slightly More Complex Reporting

**Tradeoff:** Generating financial statements from transactions requires aggregation formulas; yearly summaries would be simpler.

**Complexity Assessment:**
- Summarization formulas (SUMIF, SUMIFS) are straightforward and well-understood
- Consolidation tables provide intermediate caching, reducing formula complexity
- Power Query can automate complex aggregations in future versions

**Mitigation:**
- Data Dictionary documents all consolidation formulas
- Consolidation tables are provided as templates
- Once built, formulas are reusable across all reports
- Formula complexity is managed in dedicated consolidation worksheets, not in user-facing reports

### Correction Administration

**Tradeoff:** Correcting errors requires creating adjusting transactions, not simply editing the original.

**Concern:** Additional step compared to directly editing a summary.

**Mitigation:**
- User enters "Correction to Transaction XYZ" with explanation
- System can flag corrections for audit review
- Benefits (audit trail, original record preserved) far outweigh minor administrative cost
- User training documents the correction procedure

---

## Tradeoffs Accepted

The following tradeoffs are accepted as mandatory requirements:

1. **Storage Size** — Accepted; negligible for v0.1 and manageable for foreseeable future
2. **Reporting Complexity** — Accepted; complexity concentrated in technical layers, not user-facing
3. **Correction Process** — Accepted; audit benefits outweigh extra administrative step

---

## Implementation Requirements

### Transaction Table Schema

Every transaction table shall follow this standard:

```
tblTransactions (Master Transaction Log)
├── TransactionID (Primary Key)
├── TransactionDate
├── CropYear
├── Category
├── Subcategory
├── RelatedEntityID
├── Description
├── Amount
├── Units
├── UnitType
├── Source
├── SourceReference
├── CreatedDate
├── CreatedBy
└── Notes
```

### Category/Subcategory Taxonomy

**Standard categories and subcategories shall be defined in a reference table (tblTransactionCategories):**

| Category | Subcategories |
|----------|----------------|
| **Grain Revenue** | Corn Sales, Soybean Sales, Corn Delivery, Soybean Delivery, Government Payments, Insurance Proceeds |
| **Fertility** | Anhydrous Ammonia, Urea, MAP/DAP, Micronutrients, Lime, Gypsum |
| **Crop Protection** | Pre-Emerge Herbicide, Post-Emerge Herbicide, Insecticide, Fungicide, Growth Regulator, Seed Treatment |
| **Seed** | Corn Seed, Soybean Seed, Seed Shipping, Seed Treatment |
| **Equipment** | Equipment Purchase, Equipment Repair, Equipment Rental, Parts, Labor |
| **Fuel** | Diesel Purchase, Gasoline Purchase, Propane Purchase, Fuel Shipping |
| **Labor** | Operator Labor, Hired Labor, Contracted Services |
| **Insurance** | Crop Insurance Premium, Property Insurance, Liability Insurance, Insurance Claim |
| **Financing** | Loan Disbursement, Loan Payment, Interest Expense, Line of Credit |
| **Personal** | Family Withdrawal, Off-Farm Income, Tax Payment, Retirement Contribution |
| **Overhead** | Utilities, Office Supplies, Professional Services, Membership Dues |

### Data Entry Validation

The system shall validate:
- TransactionDate is within stated CropYear
- RelatedEntityID exists in master table
- Amount is non-zero and reasonable
- Source is one of: Manual, JD Ops Center, Imported, Calculated
- Required fields are populated

### Consolidation Strategy

Consolidation tables shall be created for:
- Revenue by Field and Crop Year
- Costs by Field, Category, and Crop Year
- Field Profitability by Crop Year
- Financial Statement summaries by period

Consolidation tables shall be marked "Calculated — Do Not Edit"

---

## Mandatory Requirements for Future Development

**All future TFOS development must comply with this decision:**

1. ✅ Every business transaction shall be recorded in a transaction table
2. ✅ Transactions shall never be overwritten; corrections via adjusting transactions only
3. ✅ No summarized data shall be stored as primary data source
4. ✅ All reports shall derive from transaction tables
5. ✅ Complete transaction history shall be maintained indefinitely
6. ✅ Every transaction shall include source documentation
7. ✅ Referential integrity constraints shall be enforced
8. ✅ Consolidation tables shall be calculated, not manually populated

**Non-Compliance Issues:** Any worksheet, formula, or process that deviates from this architecture requires Architecture Review Board (ARB) approval and separate ADR.

---

## Alternatives Considered

### Alternative 1: Summary-Based Architecture
**Approach:** Store only year-end summaries (total costs per field, total revenue, etc.)

**Rejected Because:**
- No audit trail; cannot trace individual transactions
- Historical corrections impossible without losing original data
- John Deere Operations Center data must be discarded
- Future analytics impossible
- Regulatory compliance difficult

### Alternative 2: Hybrid Approach
**Approach:** Store transactions for 2 years, then archive to summaries; older data only available as summaries

**Rejected Because:**
- Still destroys historical detail
- Multi-year analysis limited
- Restatements require re-importing old summaries
- Compliance gaps for older periods

### Alternative 3: Denormalized Transaction Log
**Approach:** Store every field, equipment, cost detail in a single wide transaction table

**Rejected Because:**
- Violates normalization principles (ADR-001)
- Massive data duplication
- Maintenance nightmare
- Performance degradation

---

## Compliance & Governance

### Enforcement

- Code reviews shall verify transaction tables are created before reports
- Architecture reviews required for any approach deviating from this ADR
- Data quality audits shall verify transaction completeness
- No report shall bypass transaction tables to derive data

### Documentation

- Every transaction table shall be documented in Data Dictionary
- Consolidation formulas shall be documented with source transaction tables
- Reports shall include traceability documentation

### Future Extensions

This ADR establishes the foundational architecture. Future ADRs may address:

- **ADR-003:** Consolidation Table Standards
- **ADR-004:** Transaction Correction Procedures
- **ADR-005:** Historical Data Archiving Strategy
- **ADR-006:** Analytics Data Model (OLAP cube or data warehouse)

---

## Implementation Timeline

| Phase | Deliverable | Status |
|-------|-------------|--------|
| v0.1 | tblTransactions schema defined | In Progress |
| v0.1 | Operational transaction tables created (Harvest, Planting, Applications, Costs) | Planned |
| v0.1 | Financial transaction tables created (Grain Sales, Loan Payments, Family) | Planned |
| v0.1 | Consolidation tables built from transactions | Planned |
| v0.2 | Transaction import automation from Ops Center | Future |
| v0.3 | Advanced analytics and reporting | Future |

---

## Related Decisions

- **ADR-001:** Relational Database Architecture — Entity structure and relationships
- **ADR-003:** (Future) Consolidation Table Standards — Standardized aggregation formulas
- **ADR-004:** (Future) Transaction Correction Procedures — Detailed process for adjusting transactions
- **ADR-005:** (Future) Data Integrity & Validation Rules — Constraint and validation engine

---

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-08-07 | TFOS Dev Team | Initial decision |

---

## Sign-Off

**Decision Authority:** Development Team  
**Status:** ✅ **Accepted**  
**Mandatory Compliance:** Yes  
**Effective Date:** 2026-08-07  
**Next Review:** After v0.1 implementation

---

## References

- ADR-001: Relational Database Architecture
- Data Dictionary: Documentation/DataDictionary.md
- Transaction Categories: Reference/TransactionCategories.xlsx
