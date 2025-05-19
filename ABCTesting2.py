import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

# Load dataset
df = pd.read_csv("Fidobiz_Product_A_B_C_Testing_2025_05_12 (1).csv")

# Function to calculate and print z-tests with rates
def perform_ztests(kpi, base):
    def get_values(cohort):
        success = int(df[f"{cohort}_{kpi}"][0])
        total = int(df[f"{cohort}_{base}"][0])
        rate = (success / total) * 100 if total > 0 else 0
        return success, total, rate

    mild_s, mild_t, mild_r = get_values("MILD")
    comm_s, comm_t, comm_r = get_values("COMMERCIAL")
    aggr_s, aggr_t, aggr_r = get_values("AGGRESSIVE")

    combined_s = comm_s + aggr_s
    combined_t = comm_t + aggr_t
    combined_r = (combined_s / combined_t) * 100 if combined_t > 0 else 0
 
    # A/B test: Mild vs (Commercial + Aggressive)
    z_ab, p_ab = proportions_ztest([mild_s, combined_s], [mild_t, combined_t])

    # Commercial vs Aggressive
    z_ca, p_ca = proportions_ztest([comm_s, aggr_s], [comm_t, aggr_t])

    print(f"\n--- Z-Test for {kpi} (base: {base}) ---")
    print(">> Conversion Rates:")
    print(f"   Mild: {mild_r:.2f}% ({mild_s}/{mild_t})")
    print(f"   Commercial: {comm_r:.2f}% ({comm_s}/{comm_t})")
    print(f"   Aggressive: {aggr_r:.2f}% ({aggr_s}/{aggr_t})")
    print(f"   Combined (Comm + Aggr): {combined_r:.2f}% ({combined_s}/{combined_t})")

    print(">> A/B Test (Mild vs Combined):")
    print(f"   z = {z_ab:.3f}, p = {p_ab:.3f}")
    
    print(">> Commercial vs Aggressive:")
    print(f"   z = {z_ca:.3f}, p = {p_ca:.3f}")
    print("-" * 50)

# KPI Tests: { KPI: Base Column }
kpi_bases = {
    "DISBURSED": "TOTAL",
    "KYB": "TOTAL",
    "DOC": "TOTAL",
    "APPROVED": "TOTAL"
}

# Run all tests
for kpi, base in kpi_bases.items():
    perform_ztests(kpi, base)



