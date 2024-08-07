# imports
import streamlit as st
import pandas as pd
import duckdb

# configs
st.set_page_config(layout="wide")

# data import
importdf = pd.read_csv("data/protein_table.csv")

with st.container():

    # inputs
    st.title("Daily Protein Calculator 🥛🍗🍄")

    option_sex = st.selectbox(
        "What sex were you assigned at birth?",
        ("Male", "Female"),
    )

    option_weight = st.number_input(
        "What is your current weight in pounds?", value=150, min_value=50, max_value=500
    )

    # calcs based on inputs

    weight_lb = option_weight

    if option_sex == "Male":
        weight_lb = weight_lb
    else:
        weight_lb = weight_lb * 0.85

    weight_kg = weight_lb / 2.2046
    min_daily_g = round(0.36 * weight_lb, 1)
    low_daily_g = round(1.2 * weight_kg, 1)
    high_daily_g = round(1.7 * weight_kg, 1)

    # text outputs

    st.text(
        f"""Your daily protein intake should be in the range of: {low_daily_g}g to {high_daily_g}g!
    And at a minimum: {min_daily_g}g """
    )

    st.text("Here is what that might look like: ")

    # table calcs
    example_foods = [
        "Costco Chicken breast (boneless skinless)",
        "Ground Turkey",
        "Cod Fillet",
        "Canned Albacore no salt",
        "Portabello mushrooms",
        "Optimum Nutrition Gold Standard Whey Protein Powder",
    ]

    example_servings = [3, 4, 4, 4, 6, 1]

    food_icons = ["🍗", "🦃", "🐟", "🥫", "🍄", "🥛"]

    serving_name = ["breasts", "portions", "fillets", "cans", "portions", "scoops"]

    low_list = []
    high_list = []
    g_oz_list = []

    for food in example_foods:
        pro_g_per_oz = float(importdf.loc[importdf["Item"] == food]["Pr(g)/oz"].item())
        g_oz_list.append(pro_g_per_oz)
        low_daily_oz = int(round(low_daily_g / pro_g_per_oz, 0))
        low_list.append(low_daily_oz)
        high_daily_oz = int(round(high_daily_g / pro_g_per_oz, 0))
        high_list.append(high_daily_oz)

    example_dict = {
        "food": example_foods,
        "serving_name": serving_name,
        "icon": food_icons,
        "g_oz": g_oz_list,
        "low_oz": low_list,
        "high_oz": high_list,
        "serving_oz": example_servings,
    }

    # cast to df
    example_df = (
        pd.DataFrame(example_dict)
        .astype(
            {
                "food": str,
                "serving_name": str,
                "icon": str,
                "g_oz": float,
                "low_oz": float,
                "high_oz": float,
                "serving_oz": float,
            }
        )
        .sort_values(by=["g_oz"], ascending=False)
    )

    example_df_all = duckdb.query(
        """SELECT *,
            round(low_oz / serving_oz)::int as low_servings,
            round(high_oz / serving_oz)::int as high_servings,
            repeat(icon, low_servings) as servings_low_icon,
            repeat(icon, high_servings) as servings_high_icon
        FROM example_df"""
    ).to_df()

    example_df = duckdb.query(
        """SELECT 
            food,
            serving_oz as portion_size,
            serving_oz * g_oz as protein_g_per_portion,
            'About ' || low_servings || ' to ' || high_servings || ' ' || serving_name || ' per day!' as servings,
            servings_low_icon,
            servings_high_icon
        FROM example_df_all
        order by protein_g_per_portion desc
        """
    ).to_df()

    # example portions
    st.dataframe(example_df)

    # product comparison

    st.text(
        """For a more complete list of example products
    with their protein and calorie contents: """
    )
    st.dataframe(importdf)

# source links

left_column, right_column = st.columns(2)

left_column.link_button(
    "Information Source (WebMD)", "https://www.webmd.com/food-recipes/protein"
)

right_column.link_button(
    "Information Source (Calculator.net)",
    "https://www.calculator.net/protein-calculator.html",
)
