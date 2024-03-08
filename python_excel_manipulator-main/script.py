import os
import pandas as pd

def extract_scenario_name(filename):
    base_name = os.path.basename(filename)
    if "_operations_results_logs.xlsx" in base_name:
        return base_name.replace("_operations_results_logs.xlsx", "")
    elif "_overall_results.xlsx" in base_name:
        return base_name.replace("_overall_results.xlsx", "")
    else:
        return None

def calculate_revenues(df):
    # Define separate formulas for each revenue type using actual column names
    revenue_formulas = {
        'Day-ahead revenues (€)': ['p_annonce_day_ahead_MW * real_prices_day_ahead_euros_per_MWh'],
        'primary up band revenues (€)': ['p_annonce_reserve_MW_primary_up * real_prices_band_euros_per_MW_primary_up'],
        'primary down band revenues (€)': ['p_annonce_reserve_MW_primary_down * real_prices_band_euros_per_MW_primary_down'],
        'secondary up band revenues (€)': ['p_annonce_reserve_MW_secondary_up * real_prices_band_euros_per_MW_secondary_up'],
        'secondary down band revenues (€)': ['p_annonce_reserve_MW_secondary_down * real_prices_band_euros_per_MW_secondary_down'],
        'secondary up reserve energy revenues (€)': ['e_injection_reserve_MWh_secondary_up * real_prices_energy_reserve_euros_per_MWh_secondary_up'],
        'secondary down reserve energy revenues (€)': ['e_injection_reserve_MWh_secondary_down * real_prices_energy_reserve_euros_per_MWh_secondary_down'],
        'Energy lack balancing revenues (€)': ['e_balancing_overall_lack_MWh * real_prices_energy_lack_balancing_euros_per_MWh'],
        'Energy surplus balancing revenues (€)': ['e_balancing_overall_surplus_MWh * real_prices_energy_surplus_balancing_euros_per_MWh'],
        'secondary up band balancing cost (€)': ['abs(p_balancing_reserve_MW_secondary_up_band_na) * real_prices_band_euros_per_MW_secondary_up'],
        'secondary down band balancing cost (€)': ['abs(p_balancing_reserve_MW_secondary_down_band_na) * real_prices_band_euros_per_MW_secondary_down'],
    }

    # Create a copy of the dataframe to avoid modifying the original
    calculated_df = df.copy()

    # Apply the formulas for each revenue type
    for revenue, formula in revenue_formulas.items():
        calculated_df[revenue] = eval(formula[0], {'p_annonce_day_ahead_MW': df['p_annonce_day_ahead_MW'],
                                                   'p_annonce_reserve_MW_primary_up': df['p_annonce_reserve_MW_primary_up'],
                                                   'p_annonce_reserve_MW_primary_down': df['p_annonce_reserve_MW_primary_down'],
                                                   'p_annonce_reserve_MW_secondary_up': df['p_annonce_reserve_MW_secondary_up'],
                                                   'p_annonce_reserve_MW_secondary_down': df['p_annonce_reserve_MW_secondary_down'],
                                                   'e_injection_reserve_MWh_secondary_up': df['e_injection_reserve_MWh_secondary_up'],
                                                   'e_injection_reserve_MWh_secondary_down': df['e_injection_reserve_MWh_secondary_down'],
                                                   'e_balancing_overall_lack_MWh': df['e_balancing_overall_lack_MWh'],
                                                   'e_balancing_overall_surplus_MWh': df['e_balancing_overall_surplus_MWh'],
                                                   'p_balancing_reserve_MW_secondary_up_band_na': df['p_balancing_reserve_MW_secondary_up_band_na'],
                                                   'p_balancing_reserve_MW_secondary_down_band_na': df['p_balancing_reserve_MW_secondary_down_band_na'],
                                                   'real_prices_day_ahead_euros_per_MWh': df['real_prices_day_ahead_euros_per_MWh'],
                                                   'real_prices_band_euros_per_MW_primary_up': df['real_prices_band_euros_per_MW_primary_up'],
                                                   'real_prices_band_euros_per_MW_primary_down': df['real_prices_band_euros_per_MW_primary_down'],
                                                   'real_prices_band_euros_per_MW_secondary_up': df['real_prices_band_euros_per_MW_secondary_up'],
                                                   'real_prices_band_euros_per_MW_secondary_down': df['real_prices_band_euros_per_MW_secondary_down'],
                                                   'real_prices_energy_reserve_euros_per_MWh_secondary_up': df['real_prices_energy_reserve_euros_per_MWh_secondary_up'],
                                                   'real_prices_energy_reserve_euros_per_MWh_secondary_down': df['real_prices_energy_reserve_euros_per_MWh_secondary_down'],
                                                   'real_prices_energy_lack_balancing_euros_per_MWh': df['real_prices_energy_lack_balancing_euros_per_MWh'],
                                                   'real_prices_energy_surplus_balancing_euros_per_MWh': df['real_prices_energy_surplus_balancing_euros_per_MWh'],
                                                  })

    # Return only the calculated revenue columns
    calculated_revenues = calculated_df[['Scenario'] + list(revenue_formulas.keys())]

    return calculated_revenues



def create_calculations_table(calculated_revenues, overall_df, scenario_name):
    # Create a table for calculated revenues
    calculations_table = pd.DataFrame({
        'CALCULATIONS': list(calculated_revenues.columns)[1:],  # Exclude the 'Scenario' column
        'Calculated Value': calculated_revenues.iloc[:, 1:].sum(axis=0)  # Sum values for each revenue type, excluding the 'Scenario' column
    })

    # Set 'CALCULATIONS' as the index in both DataFrames
    calculations_table.set_index('CALCULATIONS', inplace=True)

    # If the 'Scenario' column is present in overall_df, set it as the index
    if 'Scenario' in overall_df.columns:
        overall_df.set_index('Scenario', inplace=True)
    else:
        # If 'Scenario' is not present, set the index as the first column
        overall_df.set_index(overall_df.columns[0], inplace=True)

    # Check if '0' column is present in overall_df
    if '0' in overall_df.index:
        # Use '0' as the index and transpose the DataFrame
        overall_df = overall_df.T
        # Use iloc to get the correct row (assuming '0' is in the first row)
        overall_df = overall_df.iloc[1:]

    # Merge the calculations_table and overall_df on the index
    merged_df = pd.merge(calculations_table, overall_df, left_index=True, right_index=True, how='left')

    # Calculate percentage difference
    merged_df['Percentage Difference'] = ((merged_df['Calculated Value'] - merged_df.loc[:, 0]) / merged_df.loc[:, 0]).abs() * 100

    # Create a new Excel writer with the scenario_name as the file name
    with pd.ExcelWriter(f"{scenario_name}_comparison.xlsx", engine='xlsxwriter') as writer:
        # Add the sheet with the calculations_table
        calculations_table.to_excel(writer, sheet_name=f"{scenario_name}_comparison", startrow=1, index=False)

        # If there are two scenarios, add an empty sheet for overall_details
        if len(overall_df) > 0:
            pd.DataFrame().to_excel(writer, sheet_name="Overall_Details", index=False)

    # Return the merged_df and an empty DataFrame for overall_details
    return merged_df.reset_index(), pd.DataFrame()


def process_scenario(path, scenario_name):
    all_dataframes = []

    for filename in os.listdir(path):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(os.path.join(path, filename))

            # Extract scenario name from the filename
            current_scenario_name = extract_scenario_name(filename)

            if current_scenario_name == scenario_name and "_operations_results_logs.xlsx" in filename:
                # Add a new column with the scenario name
                df['Scenario'] = current_scenario_name
                all_dataframes.append(df)

    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)

        # Use the scenario name as the output file name
        output_filename = f"{scenario_name}_operations_results_logs.xlsx"

        # Write to Excel with one sheet: scenario_name
        with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
            # Add the sheet with the values
            combined_df.to_excel(writer, sheet_name=scenario_name, index=False)

        # Return the calculated tables for the scenario
        return calculate_revenues(combined_df), pd.DataFrame()
    else:
        print(f"No matching files found for {scenario_name} and '_operations_results_logs.xlsx'.")
        # Return empty DataFrames to avoid NoneType error
        return pd.DataFrame(), pd.DataFrame()




def combine_excel_files(path, num_scenarios):
    all_dataframes = []

    for filename in os.listdir(path):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(os.path.join(path, filename))

            # Extract scenario name from the filename
            scenario_name = extract_scenario_name(filename)

            if scenario_name is not None:
                # Add a new column with the scenario name
                df['Scenario'] = scenario_name
                all_dataframes.append(df)

    combined_df = pd.concat(all_dataframes, ignore_index=True)

    # Load overall results file
    overall_results_file = [f for f in os.listdir(path) if "_overall_results.xlsx" in f]
    if overall_results_file:
        overall_df = pd.read_excel(os.path.join(path, overall_results_file[0]), engine='openpyxl')
    else:
        overall_df = pd.DataFrame()

    # Calculate revenues
    revenues = calculate_revenues(combined_df)

    # Create tables for calculations and overall details
    calculations_table, overall_details = create_calculations_table(revenues, overall_df, "Combined")

    try:
        with pd.ExcelWriter("combined_comparison.xlsx", engine='xlsxwriter') as writer:
            # Add the first sheet with the values for all scenarios
            combined_df.to_excel(writer, sheet_name="Combined_Values", index=False)

            # Add the second sheet with the calculated revenues for all scenarios
            calculations_table.to_excel(writer, sheet_name="Combined_Comparison", startrow=1, index=False)

            # If there are two scenarios, create additional sheets
            if num_scenarios == 2:
                for scenario_name in set(combined_df['Scenario']):
                    process_scenario(path, scenario_name)

                    # Load scenario-specific data
                    combined_df_scenario = pd.read_excel(
                        f"{scenario_name}_operations_results_logs.xlsx",
                        sheet_name=scenario_name
                    )
                    combined_df_scenario.to_excel(writer, sheet_name=f"{scenario_name[:31]}", index=False)

                    # Add the comparison sheet for each scenario
                    calculations_table_scenario, overall_details_scenario = process_scenario(path, scenario_name)
                    calculations_table_scenario.to_excel(writer, sheet_name=f"{scenario_name[:31]}_comparison", startrow=1, index=False)
                    
                    # Add overall_details sheet for each scenario
                    overall_details_scenario.to_excel(writer, sheet_name=f"{scenario_name[:31]}_comparison", startrow=len(calculations_table_scenario) + 3, index=False)
    except Exception as e:
        print(f"Error creating Excel file: {e}")
        
        
if __name__ == "__main__":
    path = input("Enter the path to the directory containing the Excel files: ")

    # Prompt the user to choose the number of scenarios (1 or 2)
    num_scenarios = int(input("Enter the number of scenarios (1 or 2): "))

    if num_scenarios not in [1, 2]:
        print("Invalid input. Please enter 1 or 2.")
    else:
        # Combine Excel files based on the number of scenarios
        combine_excel_files(path, num_scenarios)

        print(f"Comparison files created for {num_scenarios} scenarios.")
