import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# Page Configuration
# ==============================

st.set_page_config(
    page_title="BigMart Sales Prediction",
    page_icon="🛒",
    layout="wide"
)

# ==============================
# Load Model
# ==============================

with open("bigmart_best_model.pkl", "rb") as f:
    model, sklearn_version = pickle.load(f)

# ==============================
# Sidebar Portfolio
# ==============================

st.sidebar.title("👨‍💻 About Me")

st.sidebar.markdown("""
### Abhishek Shelke

🎓 **Master's in Computer Science**  
ASM's CSIT, Pimpri  
Savitribai Phule Pune University

💡 **Interests**
- Artificial Intelligence
- Machine Learning
- Data Science
""")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🔗 Connect")

st.sidebar.markdown(
"""
[LinkedIn](https://www.linkedin.com/in/abhishek-s-b98895249)

[GitHub](https://github.com/Redskull2525)
"""
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 📊 Project

**BigMart Sales Prediction**

This ML model predicts sales of a product in a BigMart outlet using multiple product and outlet features.
""")

# ==============================
# Main Title
# ==============================

st.title("🛒 BigMart Sales Prediction")

st.markdown(
f"""
This app predicts **Item Outlet Sales** using a trained Machine Learning model.

Model trained using **scikit-learn v{sklearn_version}**
"""
)

st.divider()

# ==============================
# Input Layout
# ==============================

col1, col2 = st.columns(2)

with col1:

    Item_Identifier = st.text_input("Item Identifier", "FDA15")

    Item_Weight = st.number_input(
        "Item Weight",
        min_value=0.0,
        value=12.5
    )

    Item_Fat_Content = st.selectbox(
        "Item Fat Content",
        ["Low Fat", "Regular"]
    )

    Item_Visibility = st.slider(
        "Item Visibility",
        0.0,
        0.3,
        0.1
    )

    Item_Type = st.selectbox(
        "Item Type",
        [
            "Dairy", "Soft Drinks", "Meat", "Fruits and Vegetables",
            "Household", "Baking Goods", "Snack Foods",
            "Frozen Foods", "Breakfast", "Health and Hygiene",
            "Hard Drinks", "Canned", "Breads",
            "Starchy Foods", "Others", "Seafood"
        ]
    )

with col2:

    Item_MRP = st.number_input(
        "Item MRP",
        min_value=0.0,
        value=150.0
    )

    Outlet_Identifier = st.selectbox(
        "Outlet Identifier",
        [
            "OUT027","OUT013","OUT049","OUT035","OUT046",
            "OUT017","OUT045","OUT018","OUT019","OUT010"
        ]
    )

    Outlet_Size = st.selectbox(
        "Outlet Size",
        ["Small", "Medium", "High"]
    )

    Outlet_Location_Type = st.selectbox(
        "Outlet Location Type",
        ["Tier 1", "Tier 2", "Tier 3"]
    )

    Outlet_Type = st.selectbox(
        "Outlet Type",
        [
            "Supermarket Type1",
            "Supermarket Type2",
            "Supermarket Type3",
            "Grocery Store"
        ]
    )

    Outlet_Age = st.slider(
        "Outlet Age (Years)",
        0,
        40,
        15
    )

# ==============================
# Prediction
# ==============================

if st.button("🔍 Predict Sales"):

    input_df = pd.DataFrame([{
        "Item_Identifier": Item_Identifier,
        "Item_Weight": Item_Weight,
        "Item_Fat_Content": Item_Fat_Content,
        "Item_Visibility": Item_Visibility,
        "Item_Type": Item_Type,
        "Item_MRP": Item_MRP,
        "Outlet_Identifier": Outlet_Identifier,
        "Outlet_Size": Outlet_Size,
        "Outlet_Location_Type": Outlet_Location_Type,
        "Outlet_Type": Outlet_Type,
        "Outlet_Age": Outlet_Age
    }])

    prediction = model.predict(input_df)[0]

    st.success(f"📈 Predicted Item Outlet Sales: ₹ {prediction:,.2f}")

# ==============================
# Feature Importance Section
# ==============================

st.divider()

st.subheader("📊 Model Insights")

try:
    importances = model.named_steps['regressor'].feature_importances_

    feature_names = model.named_steps['preprocessor'].get_feature_names_out()

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    })

    importance_df = importance_df.sort_values(by="Importance", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(importance_df["Feature"], importance_df["Importance"])
    ax.invert_yaxis()

    st.pyplot(fig)

except:
    st.info("Feature importance not available for this model.")

# ==============================
# Footer
# ==============================

st.divider()

st.markdown(
"""
Built with ❤️ using **Streamlit & Scikit-Learn**

© 2026 Abhishek Shelke
"""
)
