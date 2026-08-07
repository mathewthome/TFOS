# ADR-001: Relational Database Architecture

**Version:** TFOS v0.1  
**Status:** Accepted  
**Date:** 2026-08-07  
**Author:** TFOS Development Team

---

## Title

Relational Database Architecture

---

## Purpose

To establish a normalized relational data model for the Thome Farm Operating System that ensures data integrity, eliminates redundancy, and provides a single source of truth for all farm operational and financial data.

---

## Context

TFOS is a Microsoft Excel-based financial operating system designed to support comprehensive farm management for Midwest corn and soybean operations. The system must:

1. Track diverse business entities (fields, equipment, loans, budgets, costs, harvests, etc.)
2. Integrate data from multiple sources (John Deere Operations Center, manual entry, financial institutions)
3. Produce consistent, reliable financial statements and profitability reports
4. Maintain data integrity across multiple worksheets and reports
5. Support complex calculations referencing multiple entities

Without a clear relational database architecture, data inconsistency, redundancy, and formula errors become inevitable as the workbook grows in complexity.

---

## Decision

TFOS shall implement a normalized relational data model using the following principles:

### Master Data Entities (Single Source of Truth)

The following entities shall each exist exactly once in the workbook as master tables:

#### **Core Operating Entities**
- **tblFields** — Field master data (identity, acreage, location, soil characteristics, crop rotation)
- **tblEquipment** — Equipment inventory (machinery, implements, specifications, value, status)
- **tblLoans** — Loan obligations (principal, terms, rates, lender information)

#### **Planning & Budget Entities**
- **tblCropBudgets** — Crop-by-crop budget planning (inputs, quantities, costs by expense category)
- **tblOperatingCosts** — Actual operational expenses (inputs purchased, labor, repairs, utilities)

#### **Operational Data Entities (from John Deere Operations Center)**
- **tblHarvestImport** — Harvest records (yield, moisture, test weight, quality metrics)
- **tblPlantingImport** — Planting records (dates, varieties, seeding rates, populations)
- **tblApplicationImport** — Application records (fertilizer, herbicides, insecticides, fungicides)

#### **Financial Entities**
- **tblFamilyFinancials** — Family income and personal expenses
- **tblLoanAmortization** — Calculated loan payment schedules (derived from tblLoans)
- **tblFinancialAccounts** — General ledger accounts for balance sheet

### Relationship Establishment

All relationships between entities shall be established using:

- **Primary Keys:** Unique identifiers for each master entity (FieldID, EquipmentID, LoanID, etc.)
- **Foreign Keys:** References to primary keys in lookup formulas and consolidation tables
- **Data Integrity Rules:** No orphaned records; all references must point to valid master records

### Reporting Architecture

All reports and analysis worksheets shall:

1. **Never duplicate master data** — Reports reference master tables using formulas, not copied values
2. **Use lookup and consolidation tables** — Intermediate tables (tblRevenueByField, tblCostByField, tblFieldProfitability) aggregate master data
3. **Link to master tables** — Every report row includes a foreign key reference enabling drill-down to source data
4. **Derive calculated values** — Profit margins, yields, costs-per-acre are calculated in real time, not stored

### Dashboard Architecture

- All dashboards shall reference consolidated reporting tables (tblFieldProfitability, tblBalanceSheet, tblCashFlow)
- No hardcoded values; all metrics derive from master or reporting tables
- Dashboard updates automatically when underlying data changes

---

## Benefits

### Data Integrity
- **Single Source of Truth:** Each piece of information exists in exactly one master table, eliminating inconsistencies
- **Referential Integrity:** Foreign key relationships prevent orphaned records and invalid references
- **Consistency:** All reports and dashboards derive from identical source data

### Maintainability
- **Clear Structure:** Developers and users understand which table contains which data
- **Reduced Errors:** No duplicate data means no risk of updating one copy but forgetting another
- **Simplified Auditing:** Changes to master data are traceable to a single location

### Scalability
- **Formula Performance:** Lookup formulas are more efficient than complex array operations on duplicated data
- **Growth Potential:** Additional fields, equipment, or loans can be added without restructuring formulas
- **Integration Ready:** Future Power Query or database connections have a clear, normalized model to work with

### Reporting Reliability
- **Accurate Financials:** Balance sheets and cash flows derive from consistent master data
- **Drill-Down Capability:** Users can trace any summary number back to underlying transactions
- **Real-Time Updates:** Reports refresh automatically when master data changes

### User Confidence
- **Trust in Numbers:** Users know reports are calculated from authoritative master data
- **Reduced Questions:** Clear data lineage answers "where does this number come from?"
- **Compliance Ready:** Audit trails and data relationships support regulatory requirements

---

## Tradeoffs

### Complexity
**Tradeoff:** Relational design is more complex than a single flat table of all data.

**Mitigation:** 
- Clear naming conventions (tblFieldName, tblCategoryName)
- Comprehensive data dictionary documenting all entities and relationships
- Structured worksheet layout with master tables in dedicated worksheets
- Formula templates for common operations (lookups, consolidations)

### Performance
**Tradeoff:** Lookup formulas across multiple tables may be slower than direct cell references.

**Mitigation:**
- Excel's native lookup functions (VLOOKUP, INDEX/MATCH) are highly optimized
- Consolidation tables cache results, reducing repeated calculations
- For v0.1, anticipated workbook size (< 50,000 rows) poses no performance issues
- Future: Power Query or external database can replace formulas without model changes

### Learning Curve
**Tradeoff:** Users must understand primary/foreign key concepts to use the system effectively.

**Mitigation:**
- Training documentation and data dictionary are provided
- User-facing worksheets (input forms) hide the relational structure behind simple forms
- Master tables are read-only after initial setup to prevent accidental changes

### Inflexibility
**Tradeoff:** Adding new fields to an entity requires updating formulas referencing that entity.

**Mitigation:**
- Structured Tables expand automatically when new rows are added
- Named ranges reference entire columns, so new data is included without formula changes
- Schema changes are rare; most customization happens through Settings assumptions

---

## Tradeoffs Accepted

The following tradeoffs are accepted as necessary to achieve production-quality software:

1. **Operational Complexity** — Worth the cost of data integrity and maintainability
2. **User Training** — Necessary upfront investment for long-term system reliability
3. **Implementation Time** — Proper architecture saves far more time in maintenance and debugging

---

## Implementation Details

### Data Entry & Updates

- **Master Tables:** Protected from direct editing; updated through controlled data entry worksheets or imports
- **Consolidation Tables:** Calculated from master tables; recalculate automatically
- **Reports & Dashboards:** Read-only views of calculated data; no direct editing

### Import Process

Data from John Deere Operations Center flows into master tables:
1. Harvest data → tblHarvestImport
2. Planting data → tblPlantingImport
3. Application data → tblApplicationImport

Imports maintain referential integrity by validating FieldID and EquipmentID against master tables.

### Calculation Layers

**Layer 1: Master Tables** — Raw operational and financial data  
**Layer 2: Consolidation Tables** — Aggregated by field, expense category, or other dimension  
**Layer 3: Reports** — Analysis and interpretation (profitability, cash flow, balance sheet)  
**Layer 4: Dashboards** — Executive summary and KPIs  

Each layer references the layer below, ensuring consistency.

---

## Future Considerations

### Migration to External Database

As TFOS matures, the normalized relational model can be migrated to a true relational database (SQL Server, PostgreSQL) without changing the data structure. Excel would serve as the front-end interface via Power Query or direct database connections.

### Referential Integrity Constraints

Current implementation uses validation and formula logic. Future versions could implement:
- VBA-based integrity checks (without requiring VBA-based calculations)
- Power Query transformations that enforce relationships
- External database constraints

### Historical Data & Audit Trail

The current model supports adding audit columns (CreatedDate, ModifiedDate, CreatedBy) to all master tables. Future versions could implement:
- Change log tables tracking modifications
- Temporal queries to reconstruct historical states
- Compliance-grade audit trails

### Data Normalization Levels

The current design achieves 3rd Normal Form (3NF):
- 1NF: Atomic values in all cells ✓
- 2NF: No partial dependencies on primary keys ✓
- 3NF: No transitive dependencies ✓

Future versions could enhance to Boyce-Codd Normal Form (BCNF) if specific anomalies arise.

### Performance Optimization

As data volumes grow, optimization strategies include:
- Pivot tables for summary data (caching calculations)
- Named ranges and structured tables for dynamic ranges
- Power Query for complex transformations
- Eventual migration to dedicated database

---

## Alternatives Considered

### Alternative 1: Flat Table Architecture
**Approach:** Store all data in a single wide table with every attribute.

**Rejected Because:**
- Creates massive redundancy (e.g., field name repeated 100s of times)
- High maintenance cost when data changes (must update multiple rows)
- Performance suffers with very wide tables
- Violates fundamental database design principles

### Alternative 2: No Master Data Consolidation
**Approach:** Each report rebuilds calculations from raw input worksheets.

**Rejected Because:**
- Reports become inconsistent if calculations differ
- Maintenance nightmare when formulas need updates
- Difficult to audit where numbers come from
- Users lack confidence in data accuracy

### Alternative 3: Fully Denormalized Design
**Approach:** Optimize for reporting with precalculated values stored throughout the workbook.

**Rejected Because:**
- Data integrity risks from duplicated stored values
- Updates in one place not reflected elsewhere
- Audit trail becomes impossible
- Not scalable as system grows

### Alternative 4: Hybrid Approach
**Approach:** Master tables for some entities (fields, equipment), but flat tables for others (costs).

**Rejected Because:**
- Inconsistent data architecture is harder to learn and maintain
- Some reports would derive from normalized data, others from flat data
- Creates confusion about which is the source of truth

---

## Acceptance Criteria

This architecture decision is accepted when:

1. ✓ All master data entities are defined with primary keys
2. ✓ All reports reference master tables via foreign keys
3. ✓ No data duplication exists between master and reporting tables
4. ✓ Data dictionary documents all entities and relationships
5. ✓ Consolidation tables are calculated from master tables, not populated manually
6. ✓ Dashboards reference consolidation tables, not manual data entry
7. ✓ All formulas are tested for data integrity and consistency

---

## Related Decisions

- **ADR-002** (Future): Settings Architecture — Centralized assumptions separate from master data
- **ADR-003** (Future): Calculated Columns — Rules for when to calculate vs. store values
- **ADR-004** (Future): Data Import Process — Standards for integrating external data sources

---

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-08-07 | TFOS Dev Team | Initial decision |

---

## Sign-Off

**Decision Authority:** Development Team  
**Status:** ✅ Accepted  
**Effective Date:** 2026-08-07  
**Next Review:** After v0.1 completion

---

## References

- Data Dictionary: `tfos_data_dictionary_builder.py`
- Workbook Architecture: `tfos_workbook_builder.py`
- Settings Schema: `tfos_settings_builder.py`
- TFOS v0.1 Requirements: Project README
