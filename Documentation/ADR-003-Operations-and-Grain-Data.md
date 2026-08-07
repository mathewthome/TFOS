# ADR-003: Operational Data Sources

**Version:** TFOS v0.1  
**Status:** Accepted  
**Date:** 2026-08-07  
**Author:** TFOS Development Team  
**Mandatory:** Yes — All future development must comply

---

## Title

Operational Data Sources

---

## Purpose

To establish clear, authoritative data sources for operational field data and grain revenue records in TFOS, eliminating ambiguity about where data originates and ensuring consistency across all reports and analyses.

---

## Context

Farm operational data comes from multiple sources:
- **John Deere Operations Center** provides detailed field operation records (harvest, planting, applications)
- **Manual entry** is required for financial transactions (grain sales, insurance payments, government programs)
- **Imported files** may contain bulk data from equipment manufacturers or service providers

Without a clear data source hierarchy, conflicts arise:
- Is the yield in Operations Center or the spreadsheet the authoritative version?
- If grain sales don't match harvest records, which is correct?
- How are adjustments to field data handled?

This ADR establishes a single source of truth for each data type, enabling reliable reporting and reducing data integrity issues.

---

## Decision

TFOS shall establish a dual-source data architecture:

### Single Source of Truth: John Deere Operations Center

**For operational field data, John Deere Operations Center is the authoritative single source of truth.**

The following records shall be imported directly from John Deere Operations Center:

#### **Harvest Records** (tblHarvestImport)
- Field identification
- Crop harvested
- Harvest date
- Harvesting equipment
- Total bushels harvested
- Yield per acre
- Grain moisture percentage
- Test weight (lbs/bu)
- Damaged kernels percentage
- Foreign material percentage
- Data quality indicators

**Rationale:** Harvest data is captured by automated equipment monitors on the combine. Operations Center data is accurate to field-level detail and includes quality metrics. This is more reliable than manual yield records or farm memory.

#### **Planting Records** (tblPlantingImport)
- Field identification
- Crop planted
- Planting date
- Planting equipment
- Acres planted
- Seed product/variety
- Seeding rate (seeds/acre or lbs/acre)
- Target population
- Hybrid/variety characteristics
- Planting speed/conditions

**Rationale:** Planting data is captured by GPS-enabled planting equipment with real-time monitoring. Operations Center records actual planted acres and rates, essential for yield calculations and input cost allocation.

#### **Chemical Applications** (tblApplicationImport - Herbicides, Insecticides, Fungicides)
- Field identification
- Application date
- Crop growth stage
- Chemical product name and formulation
- Rate applied (oz/acre, gal/acre, etc.)
- Acres treated
- Application equipment
- Weather conditions

**Rationale:** Chemical application records in Operations Center capture actual applications via GPS. This is more reliable than manual spray logs and enables accurate cost allocation to fields.

#### **Fertilizer Applications** (tblApplicationImport - Fertility)
- Field identification
- Application date
- Fertilizer product (anhydrous ammonia, urea, MAP/DAP, micronutrients, etc.)
- Application rate (lbs/acre, gal/acre)
- Acres treated
- Application method (preplant, at-plant, sidedress, foliar)
- Application equipment
- Soil test results (if applicable)

**Rationale:** Fertility applications are a major cost component and affect yield. Operations Center data provides accurate allocation to fields and timing, essential for correlating fertility spend with results.

#### **Field Boundaries** (tblFields - Geometry)
- Field identification
- Boundary coordinates/map
- Acreage calculation
- Field history

**Rationale:** Operations Center maintains accurate field definitions and GPS boundaries. These should be imported to keep field definitions consistent with mapping data.

#### **Equipment Operations** (tblEquipmentOperations - reference data)
- Equipment identification from Operations Center
- Hours/miles logged
- Maintenance alerts
- Fuel consumption monitoring

**Rationale:** Operations Center tracks equipment usage and maintenance. This provides accurate operational cost drivers (fuel consumption, maintenance requirements).

### Data Import Process

Operational data shall be imported from John Deere Operations Center:

1. **Frequency:** As often as user performs data synchronization (daily recommended, weekly minimum)
2. **Method:** Native Ops Center export or API integration (future)
3. **Validation:** Imported records checked against master field and equipment tables
4. **Append:** New records added; existing records updated only if source timestamp is newer
5. **Audit Trail:** Imports logged with date, time, record count, source

### Single Source of Truth: Manual User Entry

**For financial transactions and grain sales, manual user entry is the authoritative source.**

The following records shall be entered manually by the user through standardized data entry forms:

#### **Grain Sales** (tblGrainSales) — PRIMARY REVENUE SOURCE
- Date of sale
- Crop (Corn or Soybeans)
- Buyer identity
- Bushels sold
- Price per bushel
- Basis (if forward contract)
- Futures price reference (for reconciliation)
- Contract type (cash, forward, futures, etc.)
- Settlement/delivery number (for tracking)
- Field allocation (which fields contributed to sale)
- Total sale value
- Notes

**Why Manual Entry:** Grain sales often involve contracts, forward sales, delivery dates, and basis adjustments. This financial transaction data originates from the farmer's business records and is subject to their business decisions. Ops Center may show harvest but not sales; sales contracts exist independently.

**Importance:** Grain sales are the primary revenue source. Accuracy here directly affects reported farm profitability and financial statements.

#### **Grain Contracts** (tblGrainContracts) — CONTRACT TRACKING
- Grain type (Corn, Soybeans)
- Bushels under contract
- Price or basis
- Contract date
- Delivery window
- Buyer
- Futures reference (if applicable)
- Status (Open, Partial, Delivered)
- Notes

**Why Manual Entry:** Contracts are business commitments outside of Operations Center. Tracking contracts ensures obligations are met and revenue is recognized appropriately.

#### **Grain Deliveries** (tblGrainDeliveries) — DELIVERY TRACKING
- Grain type
- Bushels delivered
- Delivery date
- Location (elevator, buyer's facility, storage)
- Corresponding contract/sale reference
- Receipt/ticket number
- Basis at delivery
- Moisture adjustment
- Drying cost (if applicable)
- Notes

**Why Manual Entry:** Deliveries may occur weeks or months after sale. Tracking delivery separately from sale allows for accrual accounting and inventory management.

#### **Crop Insurance Payments** (tblInsurancePayments)
- Insurance claim ID
- Policy number
- Claim date
- Crop year
- Crop type
- Claimed acres
- Coverage level
- Claim reason (yield loss, prevented planting, etc.)
- Indemnity payment amount
- Date received
- Provider
- Notes

**Why Manual Entry:** Insurance payments are financial transactions initiated by the insurance company in response to specific events. They don't appear in Operations Center and must be manually recorded when payments are received.

#### **Government Program Payments** (tblGovernmentPayments)
- Program name (ARC, PLC, CCP, etc.)
- Crop year
- Crop type
- Enrolled acres
- Payment rate per acre (if applicable)
- Total payment
- Payment date
- FSA county office
- Commodity code
- Contract/reference number
- Notes

**Why Manual Entry:** Government payments are issued outside of farm operations data systems. Farmers receive notices and payments from USDA/FSA that must be manually recorded.

#### **Miscellaneous Farm Income** (tblMiscellaneousIncome)
- Income type (custom work, rental income, agritourism, etc.)
- Description
- Amount
- Date received
- Related entity (if applicable)
- Income source/payer
- Tax classification
- Notes

**Why Manual Entry:** Off-farm income from services, equipment rental, or other sources requires manual entry as it doesn't appear in Operations Center.

#### **Crop Insurance Adjustments** (tblInsuranceAdjustments)
- Policy number
- Adjustment date
- Adjustment amount (positive or negative)
- Reason (final adjustment, amended claim, recovery, etc.)
- Related claim ID
- Notes

**Why Manual Entry:** Insurance adjustments, recoveries, or amendments come through correspondence from the insurance company and must be manually recorded.

### Grain Sales Table Schema

Every grain sale record shall include the following fields (mandatory):

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| **GrainSaleID** | UUID/Text | Yes | Unique identifier (never reused) |
| **SaleDate** | Date | Yes | Date of sale transaction |
| **CropYear** | Integer | Yes | Crop year being sold (YYYY) |
| **Crop** | Text | Yes | Corn or Soybeans |
| **Buyer** | Text | Yes | Name of buyer/merchant |
| **Bushels** | Decimal | Yes | Quantity sold (bushels) |
| **Price** | Currency | Yes | Price per bushel (USD) |
| **Basis** | Currency | No | Basis (if forward contract) |
| **FuturesPrice** | Currency | No | Reference futures price (for validation) |
| **ContractType** | Text | Yes | Cash, Forward, Futures, Contract |
| **SettlementNumber** | Text | No | Invoice/settlement reference |
| **FieldAllocation** | Text | No | Comma-separated FieldIDs contributing to sale |
| **TotalRevenue** | Currency | Yes | Bushels × Price (calculated) |
| **Notes** | Text | No | Additional context |
| **CreatedDate** | DateTime | Yes | When record entered |
| **CreatedBy** | Text | Yes | Who entered record |
| **ModifiedDate** | DateTime | No | When record last updated |

### Grain Revenue Authority

**The tblGrainSales table is the single authoritative source for grain revenue in all financial reports.**

Reports shall calculate grain revenue using:
```
Total Grain Revenue = SUM(tblGrainSales.TotalRevenue) 
                     WHERE CropYear = [Selected Year]
```

All financial statements, dashboards, and profitability analyses derive grain revenue from this table. Reconciliation with Operations Center harvest data is performed separately for yield analysis but does not override grain revenue recording.

### Data Quality & Reconciliation

#### **Reconciliation Process: Harvest vs. Grain Sales**

Operations Center records actual harvest (bushels from field). Grain sales record actual sale (bushels to buyer).

- **Match Expected:** Grain sales ≤ Harvested bushels (some retained for seed, feedstock, or storage)
- **Variance Analysis:** If grain sales > 90% of harvested bushels, likely accurate
- **Variance Investigation:** If grain sales < 50% of harvested bushels, investigate:
  - Was grain stored for future sale?
  - Was grain used for feed or seed?
  - Is harvest data incorrect?
- **Documentation:** All variances > 10% documented with explanation

#### **Validation Rules for Grain Sales**

1. **Price Validation:** Price within 50-200% of recent futures prices (flags extremes)
2. **Bushel Validation:** Bushels ≤ harvested bushels by field (allows storage carryover)
3. **Date Validation:** Sale date ≥ field harvest date
4. **Buyer Validation:** Known buyer (grain elevator, merchant, processor)
5. **Amount Validation:** Sale value ≥ cost of inputs (basic sanity check)

#### **Manual Entry Forms**

User-facing data entry forms shall:
- Provide field dropdowns (select from tblFields)
- Provide crop dropdown (Corn, Soybeans)
- Validate price range with warning for extremes
- Show relevant field harvest data (acres, yield, total bushels) for reference
- Calculate total revenue automatically
- Provide notes field for exceptions or special circumstances
- Support keyboard-only entry for efficiency
- Include submission review/confirmation

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         John Deere Operations Center (Cloud)                 │
├─────────────────────────────────────────────────────────────┤
│  • Harvest Records        • Planting Records                 │
│  • Chemical Applications  • Fertilizer Applications          │
│  • Field Boundaries       • Equipment Operations             │
└─────────────────┬───────────────────────────────────────────┘
                  │ (Import)
                  ▼
┌─────────────────────────────────────────────────────────────┐
│         TFOS v0.1 Master Tables (Excel)                      │
├─────────────────────────────────────────────────────────────┤
│  • tblHarvestImport       • tblPlantingImport                │
│  • tblApplicationImport   • tblFields                        │
│  • tblEquipmentOperations                                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│         User Manual Entry Forms (Excel)                      │
├─────────────────────────────────────────────────────────────┤
│  • Grain Sales Form       • Government Payments Form         │
│  • Insurance Payments Form • Miscellaneous Income Form       │
│  • Grain Contracts Form   • Grain Deliveries Form           │
└─────────────────┬───────────────────────────────────────────┘
                  │ (Submit)
                  ▼
┌─────────────────────────────────────────────────────────────┐
│         Grain Revenue & Financial Tables (Excel)             │
├─────────────────────────────────────────────────────────────┤
│  • tblGrainSales          • tblGrainContracts               │
│  • tblInsurancePayments   • tblGovernmentPayments           │
│  • tblMiscellaneousIncome • tblGrainDeliveries              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│         Consolidation & Analysis Tables (Excel)              │
├─────────────────────────────────────────────────────────────┤
│  • tblRevenueByField      • tblCostByField                   │
│  • tblFieldProfitability  • tblIncomeStatement              │
│  • tblBalanceSheet        • tblCashFlow                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│         Reports & Dashboards (Excel)                        │
├─────────────────────────────────────────────────────────────┤
│  • Field Profitability Report                               │
│  • Financial Statements                                     │
│  • Executive Dashboard                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Benefits

### Data Integrity
- **Single Source of Truth:** Each data element comes from one authoritative source
- **Reduced Conflicts:** No ambiguity about which data to trust
- **Accuracy:** Leverages automated field monitoring (Ops Center) and financial records (manual entry)

### Operational Efficiency
- **Automated Ops Data:** Field operations imported automatically; no manual data entry for harvest, planting, applications
- **Fast Financial Entry:** Standardized forms for grain sales and payments reduce data entry time
- **Reconciliation Ready:** Harvest vs. sales comparison easy to perform; variances easily identified

### Regulatory Compliance
- **Audit Trail:** All data sources documented; imports timestamped
- **Financial Accuracy:** Grain sales recorded from business documents (sales tickets, contracts)
- **Crop Insurance:** Harvest data from Operations Center supports crop insurance claims
- **FSA/USDA:** Operations Center data supports program eligibility claims

### Reporting Reliability
- **Consistent Financials:** Revenue always derives from tblGrainSales
- **Field Profitability:** Costs from Operations Center, revenue from grain sales—complete picture
- **Trend Analysis:** Multi-year operations data enables yield and cost analysis

### Future Extensibility
- **Machine Learning:** Operations Center data enables predictive models for yield, cost, variety selection
- **Optimization:** Historical cost and yield data supports field-by-field optimization recommendations
- **Integration:** Clear data architecture enables future connections to weather, commodity prices, farm management consultants

---

## Tradeoffs

### John Deere Operations Center Dependency

**Tradeoff:** TFOS relies on John Deere Operations Center as the authoritative source for field data.

**Concern:** What if farmer uses different equipment brand? What if Ops Center is unavailable?

**Mitigation:**
- TFOS supports manual entry as fallback for operations data
- Data import format is standard (can accommodate other equipment brands)
- Manual entry forms provided for planting, harvest, applications if Ops Center unavailable
- v0.1 focuses on Deere integration; v0.2 can add other brands

### Manual Entry for Financial Data

**Tradeoff:** Grain sales and payments require manual entry; not automated.

**Concern:** Manual entry introduces data entry errors; not scalable.

**Mitigation:**
- Standardized forms with validation and error checking
- Batch import capability for high volumes (future)
- Reconciliation process identifies discrepancies
- Data entry training and procedures provided
- v0.2 can add automated grain price feeds and insurance data integration

### Dual Data Entry for Grain

**Tradeoff:** Grain data appears in two places: Operations Center (harvest) and manual entry (sales).

**Concern:** Reconciliation complexity; potential inconsistencies.

**Mitigation:**
- Automatic reconciliation reports show variances
- Documented workflow for investigating discrepancies
- Clear authority: Ops Center for production, grain sales for revenue
- Variance thresholds trigger investigation
- Documentation supports audit

---

## Tradeoffs Accepted

The following tradeoffs are accepted:

1. **Ops Center Dependency** — Accepted; provides accurate field-level data unavailable elsewhere
2. **Manual Financial Entry** — Accepted; financial data originates from business documents, not operations data
3. **Dual Data Reconciliation** — Accepted; reconciliation ensures data quality and catches errors

---

## Implementation Requirements

### Import Workflow (from John Deere Operations Center)

1. **Export from Ops Center:**
   - User exports harvest records (CSV or Excel)
   - User exports planting records
   - User exports application records
   - User exports field boundaries

2. **Data Validation:**
   - System checks field names exist in tblFields
   - System validates date ranges
   - System flags missing or invalid data

3. **Merge into Master Tables:**
   - New records appended to tblHarvestImport, tblPlantingImport, tblApplicationImport
   - Existing records updated if source timestamp newer
   - Audit log recorded

4. **Consolidation Update:**
   - Consolidation tables (tblCostByField, tblRevenueByField) recalculate

5. **Report Refresh:**
   - All reports using operational data refresh automatically

### Manual Entry Workflow (Grain Sales, Payments, Income)

1. **User Opens Data Entry Form:**
   - Form presents current crop year, field list, buyer dropdown
   - Shows current harvest data for reference
   - Validates all required fields before submit

2. **User Enters Data:**
   - Selects field, crop, buyer from dropdowns
   - Enters bushels, price, basis
   - Enters settlement/contract reference
   - Submits form

3. **Validation Check:**
   - System validates price within expected range
   - System validates bushels not exceeding harvest
   - System validates date sequence (sale ≥ harvest)
   - Flags any issues for correction

4. **Record Creation:**
   - tblGrainSales record created with unique GrainSaleID
   - CreatedDate, CreatedBy automatically populated
   - Record available for reporting immediately

5. **Consolidation Update:**
   - tblRevenueByField recalculates grain revenue
   - tblFieldProfitability updates profit calculations
   - Financial statements refresh

### Data Quality Governance

- **Import Audit:** Log all imports with date, time, record count
- **Validation Report:** Monthly validation report shows data quality issues
- **Reconciliation Report:** Harvest vs. sales reconciliation shows variances
- **Error Correction:** Process documented for addressing data issues

---

## Mandatory Requirements for Future Development

**All future TFOS development must comply with this decision:**

1. ✅ John Deere Operations Center is authoritative for field operational data
2. ✅ Manual user entry is authoritative for financial transactions
3. ✅ tblGrainSales is the single source of grain revenue for all reports
4. ✅ All reports derive grain revenue from tblGrainSales
5. ✅ Reconciliation process documented and performed regularly
6. ✅ Import workflow includes validation and audit logging
7. ✅ Manual entry forms provided with validation
8. ✅ No hardcoded data entry in spreadsheets; all via forms

**Non-Compliance Issues:** Any report or process that deviates from these sources requires Architecture Review Board (ARB) approval and separate ADR.

---

## Alternatives Considered

### Alternative 1: All Data Manual Entry
**Approach:** Farmer enters all data manually (harvest, planting, applications, sales)

**Rejected Because:**
- Data entry burden excessive
- High error rate from manual entry
- Duplicate entry (harvest then sales)
- Operations Center data not leveraged
- Labor-intensive

### Alternative 2: Ops Center as Revenue Source
**Approach:** Use Operations Center harvest records directly as revenue (bypass grain sales entry)

**Rejected Because:**
- Harvest ≠ Sales (grain stored, used for seed, feed, or sold later)
- Operations Center lacks pricing, buyer, contract information
- Cannot track forward contracts or basis decisions
- Financial data inaccurate if treated as revenue

### Alternative 3: All Data Imported from External Source
**Approach:** Use third-party farm management software to import all data

**Rejected Because:**
- Adds software dependency and cost
- Not all farm data available in third-party systems
- Less control over data quality
- Integration complexity

### Alternative 4: User's Choice of Data Source
**Approach:** Allow farmer to choose between Ops Center and manual entry

**Rejected Because:**
- Inconsistency across reports
- Ambiguity about which is authoritative
- Data conflicts unresolved
- Compliance issues if sources conflict

---

## Integration Roadmap

| Version | Capability | Status |
|---------|-----------|--------|
| v0.1 | Manual import from Ops Center CSV/Excel | Planned |
| v0.1 | Grain sales data entry form | Planned |
| v0.1 | Reconciliation reports | Planned |
| v0.2 | Direct API connection to Ops Center | Planned |
| v0.2 | Batch grain sales import from grain elevator | Planned |
| v0.2 | Crop insurance data integration | Planned |
| v0.3 | FSA/USDA program data integration | Planned |
| v0.3 | Weather data integration | Planned |
| v0.4 | Commodity price feed integration | Planned |

---

## Related Decisions

- **ADR-001:** Relational Database Architecture — Entity structure for operational data
- **ADR-002:** Transaction-Based Data Architecture — Transaction logging and history
- **ADR-004:** (Future) Data Import Standards — Format and validation for imports
- **ADR-005:** (Future) Reconciliation Procedures — Standards for comparing data sources

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
- ADR-002: Transaction-Based Data Architecture
- John Deere Operations Center: https://www.operationscenter.deere.com
- Data Import Format Specification: Documentation/ImportFormats.md
- Grain Sales Entry Form: Forms/GrainSalesEntry.xlsx
- Reconciliation Procedure: Procedures/DataReconciliation.md
