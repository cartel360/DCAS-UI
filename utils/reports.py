import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def render_reports(df):
    st.markdown("## 🧾 Filter & Explore")

    counties = df['County'].dropna().unique()
    crops = df['crop'].dropna().unique()

    selected_counties = st.multiselect("Filter by County", counties, default=list(counties))
    selected_crops = st.multiselect("Filter by Value Chain", crops, default=list(crops))

    filtered = df[
        df['County'].isin(selected_counties) & df['crop'].isin(selected_crops)
    ]

    st.markdown(f"Showing **{len(filtered):,}** records")

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👥 Gender", 
        "🌽 Value Chains", 
        "🌱 Growth Stage", 
        "📅 Planting Trends", 
        "🗺️ Crop Heatmap & Map", 
        "📨 Messages"
    ])

    with tab1:
        st.subheader("Gender Distribution")
        gender_counts = filtered.groupby(['County', 'Gender'])['FarmerId'].count().reset_index()
        fig = px.bar(gender_counts, x='County', y='FarmerId', color='Gender', barmode='group')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Overall Gender Split (Pie)")
        gender_total = filtered['Gender'].value_counts()
        fig_pie = px.pie(values=gender_total.values, names=gender_total.index, title="Overall Gender Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        st.subheader("Value Chain by Gender")
        vc_gender = filtered.groupby(['County', 'crop', 'Gender'])['FarmerId'].count().reset_index()
        pivot = vc_gender.pivot_table(index='County', columns=['crop', 'Gender'], values='FarmerId', fill_value=0)
        st.dataframe(pivot)

    with tab3:
        st.subheader("Growth Stage Distribution")
        growth_df = filtered.groupby(['County', 'growthStage'])['FarmerId'].count().reset_index()
        fig2 = px.bar(growth_df, x='County', y='FarmerId', color='growthStage', barmode='stack')
        st.plotly_chart(fig2, use_container_width=True)

    with tab4:
        if 'plantingDate' in filtered.columns:
            st.subheader("Planting Trends Over Time")
            filtered['plantingDate'] = pd.to_datetime(filtered['plantingDate'], errors='coerce')
            fig4 = px.histogram(filtered, x='plantingDate', nbins=30, title="Planting Date Distribution")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No planting date column available.")

    with tab5:
        st.subheader("Crop Distribution Heatmap")
        pivot_crop = filtered.pivot_table(index="County", columns="crop", values="FarmerId", aggfunc="count", fill_value=0)
        fig5, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(pivot_crop, annot=True, cmap="YlGnBu", fmt="d", ax=ax)
        st.pyplot(fig5)

        if 'FinalLatitude' in filtered.columns and 'FinalLongitude' in filtered.columns:
            st.subheader("Farmer Locations Map")
            location_df = filtered[['FinalLatitude', 'FinalLongitude']].dropna().rename(
                columns={'FinalLatitude': 'latitude', 'FinalLongitude': 'longitude'}
            )
            st.map(location_df)


    with tab6:
        if any(col for col in df.columns if "Message 1 (English)" in col):
            st.subheader("Message Delivery")
            msg_df = filtered.groupby('County')[['Message 1 (English)']].count().reset_index()
            msg_df = msg_df.rename(columns={'Message 1 (English)': 'English Messages'})
            st.dataframe(msg_df)
            fig3 = px.bar(msg_df, x='County', y='English Messages', title="Messages Sent")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Message translation not available.")
