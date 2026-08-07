"""
TFOS v0.1 Settings Worksheet Builder - Refactored
Thome Farm Operating System - Centralized Assumptions Only

Creates the Settings worksheet with ONLY editable assumptions used in formulas.
Focused on Midwest corn and soybean operations.
No master data (fields, equipment, loans, transactions).

Standards:
- Clean, documented code
- All formulas reference these assumptions via named ranges
- Professional formatting
- Categories and descriptions
- Includes Named Range and Editable columns
"""

from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime


class SettingsBuilder:
    """Builder for TFOS Settings worksheet with calculation assumptions only."""
    
    def __init__(self):
        """Initialize workbook and styling."""
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "Settings"
        self.named_ranges = []
        
        # Color scheme
        self.header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        self.category_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        self.header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        self.category_font = Font(name="Calibri", size=11, bold=True, color="1F4E78")
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    def _create_header(self):
        """Create worksheet header and instructions."""
        # Title
        title = self.ws["A1"]
        title.value = "TFOS Settings - Calculation Assumptions"
        title.font = Font(name="Calibri", size=14, bold=True)
        title.alignment = Alignment(horizontal="left", vertical="center")
        self.ws.row_dimensions[1].height = 25
        
        # Generated date
        date_cell = self.ws["A2"]
        date_cell.value = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        date_cell.font = Font(name="Calibri", size=10, italic=True, color="666666")
        
        # Instructions
        instructions_row = 4
        self.ws[f"A{instructions_row}"] = "IMPORTANT: Only edit cells marked Editable = TRUE."
        self.ws[f"A{instructions_row}"].font = Font(name="Calibri", size=10, bold=True)
        
        self.ws[f"A{instructions_row + 1}"] = "All formulas throughout the workbook reference these values using named ranges."
        self.ws[f"A{instructions_row + 1}"].font = Font(name="Calibri", size=10)
        
        self.ws[f"A{instructions_row + 2}"] = "Do not delete rows or change column structure."
        self.ws[f"A{instructions_row + 2}"].font = Font(name="Calibri", size=10, color="FF0000")
        
        return instructions_row + 4
    
    def _format_header_row(self, row_num, headers):
        """Format column headers."""
        for col_idx, header in enumerate(headers, start=1):
            cell = self.ws.cell(row=row_num, column=col_idx, value=header)
            cell.fill = self.header_fill
            cell.font = self.header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = self.border
        
        self.ws.row_dimensions[row_num].height = 30
    
    def _format_category_row(self, row_num):
        """Format category separator row."""
        for col_idx in range(1, 8):
            cell = self.ws.cell(row=row_num, column=col_idx)
            cell.fill = self.category_fill
            cell.font = self.category_font
            cell.border = self.border
        
        self.ws.row_dimensions[row_num].height = 20
    
    def _add_setting(self, row_num, category, setting, value, units, description, named_range, editable=True):
        """
        Add a setting row with all columns.
        
        Args:
            row_num: Row number
            category: Setting category
            setting: Setting name
            value: Current value
            units: Unit of measurement
            description: Setting description
            named_range: Name for Excel named range
            editable: Whether user should edit this value
        """
        # Column A: Category
        cell_a = self.ws.cell(row=row_num, column=1, value=category)
        cell_a.alignment = Alignment(horizontal="left", vertical="center")
        cell_a.border = self.border
        cell_a.font = Font(name="Calibri", size=10)
        
        # Column B: Setting
        cell_b = self.ws.cell(row=row_num, column=2, value=setting)
        cell_b.alignment = Alignment(horizontal="left", vertical="center")
        cell_b.border = self.border
        cell_b.font = Font(name="Calibri", size=10, bold=True)
        
        # Column C: Current Value
        cell_c = self.ws.cell(row=row_num, column=3, value=value)
        cell_c.alignment = Alignment(horizontal="right", vertical="center")
        cell_c.border = self.border
        cell_c.font = Font(name="Calibri", size=10)
        
        # Highlight if editable (light yellow)
        if editable:
            cell_c.fill = PatternFill(start_color="FFFFCC", end_color="FFFFCC", fill_type="solid")
        
        # Column D: Units
        cell_d = self.ws.cell(row=row_num, column=4, value=units)
        cell_d.alignment = Alignment(horizontal="left", vertical="center")
        cell_d.border = self.border
        cell_d.font = Font(name="Calibri", size=10, color="666666")
        
        # Column E: Description
        cell_e = self.ws.cell(row=row_num, column=5, value=description)
        cell_e.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        cell_e.border = self.border
        cell_e.font = Font(name="Calibri", size=10, italic=True)
        
        # Column F: Named Range
        cell_f = self.ws.cell(row=row_num, column=6, value=named_range)
        cell_f.alignment = Alignment(horizontal="left", vertical="center")
        cell_f.border = self.border
        cell_f.font = Font(name="Calibri", size=10, color="0070C0")
        
        # Column G: Editable
        cell_g = self.ws.cell(row=row_num, column=7, value="Yes" if editable else "No")
        cell_g.alignment = Alignment(horizontal="center", vertical="center")
        cell_g.border = self.border
        cell_g.font = Font(name="Calibri", size=10)
        
        # Create named range
        try:
            # Clean the named range name
            clean_name = named_range.replace(" ", "_").replace("-", "_").upper()
            self.wb.named_ranges[clean_name] = f"Settings!$C${row_num}"
            self.named_ranges.append({
                'name': clean_name,
                'cell': f"C{row_num}",
                'setting': setting,
                'value': value
            })
        except Exception as e:
            print(f"Warning: Could not create named range {named_range}: {e}")
        
        self.ws.row_dimensions[row_num].height = 18
        return row_num + 1
    
    def build_crop_prices_section(self, current_row):
        """Build CROP PRICES category settings."""
        # Section header
        self.ws[f"A{current_row}"] = "CROP PRICES"
        self._format_category_row(current_row)
        current_row += 1
        
        crop_price_settings = [
            ("Corn Price", 4.40, "USD/Bushel", "Expected selling price for corn", "CORN_PRICE"),
            ("Soybean Price", 11.00, "USD/Bushel", "Expected selling price for soybeans", "SOYBEAN_PRICE"),
        ]
        
        for setting, value, units, desc, named_range in crop_price_settings:
            current_row = self._add_setting(current_row, "Crop Prices", setting, value, units, desc, named_range, True)
        
        return current_row + 1
    
    def build_average_yields_section(self, current_row):
        """Build AVERAGE YIELDS category settings."""
        # Section header
        self.ws[f"A{current_row}"] = "AVERAGE YIELDS"
        self._format_category_row(current_row)
        current_row += 1
        
        yield_settings = [
            ("Corn Yield", 220, "Bushels/Acre", "Expected corn yield per acre", "CORN_YIELD"),
            ("Soybean Yield", 70, "Bushels/Acre", "Expected soybean yield per acre", "SOYBEAN_YIELD"),
        ]
        
        for setting, value, units, desc, named_range in yield_settings:
            current_row = self._add_setting(current_row, "Average Yields", setting, value, units, desc, named_range, True)
        
        return current_row + 1
    
    def build_financial_section(self, current_row):
        """Build FINANCIAL category settings."""
        # Section header
        self.ws[f"A{current_row}"] = "FINANCIAL"
        self._format_category_row(current_row)
        current_row += 1
        
        financial_settings = [
            ("Minimum Cash Reserve", 100000, "USD", "Minimum cash balance to maintain for operations", "MINIMUM_CASH_RESERVE", True),
            ("Target Debt-to-Asset Ratio", 0.40, "Decimal (40% = 0.40)", "Target leverage ratio for financial health", "TARGET_DEBT_TO_ASSET_RATIO", True),
            ("Operating Loan Interest Rate", 0.065, "Decimal (6.5% = 0.065)", "Interest rate on operating loans", "OPERATING_LOAN_RATE", True),
            ("Equipment Loan Interest Rate", 0.055, "Decimal (5.5% = 0.055)", "Interest rate on equipment financing", "EQUIPMENT_LOAN_RATE", True),
            ("Land Loan Interest Rate", 0.050, "Decimal (5.0% = 0.050)", "Interest rate on land mortgages", "LAND_LOAN_RATE", True),
        ]
        
        for setting, value, units, desc, named_range, editable in financial_settings:
            current_row = self._add_setting(current_row, "Financial", setting, value, units, desc, named_range, editable)
        
        return current_row + 1
    
    def build_inflation_section(self, current_row):
        """Build INFLATION category settings."""
        # Section header
        self.ws[f"A{current_row}"] = "INFLATION"
        self._format_category_row(current_row)
        current_row += 1
        
        inflation_settings = [
            ("General Inflation Rate", 0.03, "Decimal (3% = 0.03)", "Overall inflation assumption for projections", "INFLATION_RATE", True),
            ("Input Cost Inflation", 0.03, "Decimal (3% = 0.03)", "Inflation on seed, fertilizer, chemicals", "INPUT_INFLATION_RATE", True),
            ("Fuel Inflation Rate", 0.04, "Decimal (4% = 0.04)", "Inflation on fuel and energy", "FUEL_INFLATION_RATE", True),
            ("Equipment Cost Inflation", 0.03, "Decimal (3% = 0.03)", "Inflation on machinery and equipment", "EQUIPMENT_INFLATION_RATE", True),
        ]
        
        for setting, value, units, desc, named_range in inflation_settings:
            current_row = self._add_setting(current_row, "Inflation", setting, value, units, desc, named_range, True)
        
        return current_row + 1
    
    def build_investment_section(self, current_row):
        """Build INVESTMENT category settings."""
        # Section header
        self.ws[f"A{current_row}"] = "INVESTMENT & RETURNS"
        self._format_category_row(current_row)
        current_row += 1
        
        investment_settings = [
            ("Investment Return Rate", 0.07, "Decimal (7% = 0.07)", "Expected annual return on invested capital", "INVESTMENT_RETURN_RATE", True),
            ("Land Appreciation Rate", 0.04, "Decimal (4% = 0.04)", "Expected annual appreciation of land value", "LAND_APPRECIATION_RATE", True),
            ("Discount Rate", 0.07, "Decimal (7% = 0.07)", "Used for NPV and time value of money calculations", "DISCOUNT_RATE", True),
        ]
        
        for setting, value, units, desc, named_range in investment_settings:
            current_row = self._add_setting(current_row, "Investment & Returns", setting, value, units, desc, named_range, True)
        
        return current_row + 1
    
    def build_personal_section(self, current_row):
        """Build PERSONAL category settings."""
        # Section header
        self.ws[f"A{current_row}"] = "PERSONAL"
        self._format_category_row(current_row)
        current_row += 1
        
        personal_settings = [
            ("Operator Age", 0, "Years", "Current age of primary operator", "OPERATOR_AGE", True),
            ("Retirement Age", 60, "Years", "Planned retirement age for succession planning", "RETIREMENT_AGE", True),
            ("Years to Retirement", 0, "Years", "Years until planned retirement (calculated)", "YEARS_TO_RETIREMENT", False),
        ]
        
        for setting, value, units, desc, named_range, editable in personal_settings:
            current_row = self._add_setting(current_row, "Personal", setting, value, units, desc, named_range, editable)
        
        return current_row + 1
    
    def build_tax_section(self, current_row):
        """Build TAX category settings."""
        # Section header
        self.ws[f"A{current_row}"] = "TAX RATES"
        self._format_category_row(current_row)
        current_row += 1
        
        tax_settings = [
            ("Federal Income Tax Rate", 0.22, "Decimal (22% = 0.22)", "Marginal federal income tax rate", "FEDERAL_INCOME_TAX_RATE", True),
            ("State Income Tax Rate", 0.05, "Decimal (5% = 0.05)", "Marginal state income tax rate", "STATE_INCOME_TAX_RATE", True),
            ("Property Tax Rate", 0.01, "Decimal (1% = 0.01)", "Annual property tax as % of land value", "PROPERTY_TAX_RATE", True),
        ]
        
        for setting, value, units, desc, named_range in tax_settings:
            current_row = self._add_setting(current_row, "Tax Rates", setting, value, units, desc, named_range, True)
        
        return current_row + 1
    
    def build_insurance_section(self, current_row):
        """Build INSURANCE category settings."""
        # Section header
        self.ws[f"A{current_row}"] = "INSURANCE"
        self._format_category_row(current_row)
        current_row += 1
        
        insurance_settings = [
            ("Crop Insurance Coverage Level", 0.75, "Decimal (75% = 0.75)", "Percentage of expected revenue covered by crop insurance", "CROP_INSURANCE_COVERAGE", True),
            ("Crop Insurance Cost", 0.0, "USD/Acre", "Annual crop insurance premium per acre", "CROP_INSURANCE_COST_PER_ACRE", True),
        ]
        
        for setting, value, units, desc, named_range in insurance_settings:
            current_row = self._add_setting(current_row, "Insurance", setting, value, units, desc, named_range, True)
        
        return current_row + 1
    
    def build_machinery_section(self, current_row):
        """Build MACHINERY category settings."""
        # Section header
        self.ws[f"A{current_row}"] = "MACHINERY"
        self._format_category_row(current_row)
        current_row += 1
        
        machinery_settings = [
            ("Machinery Repair Rate", 0.04, "Decimal (4% = 0.04)", "Annual repair cost as % of machinery value", "MACHINERY_REPAIR_RATE", True),
            ("Machinery Depreciation Years", 10, "Years", "Average useful life of machinery for depreciation", "MACHINERY_DEPRECIATION_YEARS", True),
            ("Tire Replacement Cycle", 3, "Years", "Years between tire replacements", "TIRE_REPLACEMENT_CYCLE", True),
        ]
        
        for setting, value, units, desc, named_range in machinery_settings:
            current_row = self._add_setting(current_row, "Machinery", setting, value, units, desc, named_range, True)
        
        return current_row + 1
    
    def build(self):
        """Build complete Settings worksheet."""
        print("Building TFOS Settings Worksheet (Refactored)...")
        
        # Set column widths
        self.ws.column_dimensions["A"].width = 22
        self.ws.column_dimensions["B"].width = 35
        self.ws.column_dimensions["C"].width = 16
        self.ws.column_dimensions["D"].width = 28
        self.ws.column_dimensions["E"].width = 45
        self.ws.column_dimensions["F"].width = 30
        self.ws.column_dimensions["G"].width = 12
        
        # Create header
        current_row = self._create_header()
        
        # Add header row for table
        headers = ["Category", "Setting", "Current Value", "Units", "Description", "Named Range", "Editable"]
        self._format_header_row(current_row, headers)
        current_row += 1
        
        # Build all sections
        current_row = self.build_crop_prices_section(current_row)
        current_row = self.build_average_yields_section(current_row)
        current_row = self.build_financial_section(current_row)
        current_row = self.build_inflation_section(current_row)
        current_row = self.build_investment_section(current_row)
        current_row = self.build_personal_section(current_row)
        current_row = self.build_tax_section(current_row)
        current_row = self.build_insurance_section(current_row)
        current_row = self.build_machinery_section(current_row)
        
        print(f"✓ Settings worksheet created with {len(self.named_ranges)} named ranges")
        
        return self.wb
    
    def save(self, filename="TFOS_Settings_v0.1.xlsx"):
        """Save workbook to file."""
        self.build()
        self.wb.save(filename)
        print(f"✓ Workbook saved: {filename}")
        
        # Print named ranges summary
        print("\nNamed Ranges Created:")
        print(f"{'Name':<40} {'Cell':<12} {'Value':<20} {'Setting'}")
        print("=" * 100)
        for item in self.named_ranges:
            print(f"{item['name']:<40} {item['cell']:<12} {str(item['value']):<20} {item['setting']}")
        
        return filename


if __name__ == "__main__":
    builder = SettingsBuilder()
    builder.save("TFOS_Settings_v0.1.xlsx")
    print("\nTFOS Settings worksheet (refactored) complete.")
