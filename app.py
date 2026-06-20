import streamlit as st
import plotly.graph_objects as go
from extractor import extract_text
from analyser import analyse_report
import json

st.set_page_config(
    page_title="ASX Financial Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 ASX Financial Report Intelligence Platform")
st.subheader("AI Powered Annual Report Analysis for ASX Companies")
st.write("Upload any ASX company annual report PDF and get instant AI powered financial insights.")

st.divider()

mode = st.radio(
    "Select Mode",
    ["Single Company Analysis", "Compare Two Companies"],
    horizontal=True
)

st.divider()

def display_analysis(analysis, title=""):
    if title:
        st.subheader(title)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**🏢 Company:** {analysis.get('company_name', 'Unknown')}")
    with col2:
        st.write(f"**📅 Financial Year:** {analysis.get('financial_year', 'Unknown')}")
    with col3:
        sentiment = analysis.get("sentiment", "neutral")
        emoji = "🟢" if sentiment == "positive" else "🔴" if sentiment == "negative" else "🟡"
        st.write(f"**📈 Sentiment:** {emoji} {sentiment.capitalize()}")

    st.divider()

    st.subheader("💰 Financial Metrics")
    metrics_data = {
        "Revenue": analysis.get("revenue", "N/A"),
        "Net Profit": analysis.get("profit", "N/A"),
        "Revenue Growth": analysis.get("revenue_growth", "N/A"),
        "EBITDA": analysis.get("ebitda", "N/A"),
        "Dividend Per Share": analysis.get("dividend", "N/A"),
        "Employees": analysis.get("employees", "N/A"),
    }
    for label, value in metrics_data.items():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"**{label}**")
        with col2:
            st.write(value)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚠️ Key Risks")
        for risk in analysis.get("risks", []):
            st.warning(f"• {risk}")
    with col2:
        st.subheader("🚀 Growth Opportunities")
        for opp in analysis.get("opportunities", []):
            st.success(f"• {opp}")

    st.divider()

    st.subheader("⭐ Key Highlights")
    for highlight in analysis.get("key_highlights", []):
        st.info(f"• {highlight}")

    st.divider()

    st.subheader("📊 Risk Analysis Chart")
    risks = analysis.get("risks", [])
    if risks:
        fig = go.Figure(go.Bar(
            x=risks,
            y=[5, 4, 3, 2, 1][:len(risks)],
            marker_color=["#FF4B4B", "#FF7F7F", "#FFB3B3", "#FFD9D9", "#FFF0F0"][:len(risks)],
            text=["High", "Medium-High", "Medium", "Low-Medium", "Low"][:len(risks)],
            textposition="auto"
        ))
        fig.update_layout(
            title="Risk Priority Matrix",
            xaxis_title="Risk Factor",
            yaxis_title="Risk Level",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("📝 Executive Summary")
    st.info(analysis.get("executive_summary", "No summary available"))

    st.divider()

    st.subheader("🔮 Future Outlook")
    st.success(analysis.get("outlook", "No outlook available"))

    st.divider()

    st.download_button(
        label="⬇️ Download Analysis as JSON",
        data=json.dumps(analysis, indent=2),
        file_name=f"{analysis.get('company_name', 'analysis')}_report.json",
        mime="application/json"
    )


if mode == "Single Company Analysis":
    uploaded_file = st.file_uploader("Upload ASX Annual Report (PDF)", type="pdf")

    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")

        if st.button("🔍 Analyse Report", type="primary"):
            with st.spinner("📄 Extracting report text..."):
                text = extract_text(uploaded_file)

            if not text:
                st.error("Could not extract text from this PDF.")
            else:
                with st.spinner("🤖 AI is analysing the report..."):
                    try:
                        analysis = analyse_report(text)
                        st.success("✅ Analysis complete!")
                        st.divider()
                        display_analysis(analysis)
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")

elif mode == "Compare Two Companies":
    col1, col2 = st.columns(2)

    with col1:
        file1 = st.file_uploader("Upload First Company Report", type="pdf", key="file1")
    with col2:
        file2 = st.file_uploader("Upload Second Company Report", type="pdf", key="file2")

    if file1 and file2:
        st.success(f"✅ Uploaded: {file1.name} and {file2.name}")

        if st.button("🔍 Compare Companies", type="primary"):
            with st.spinner("📄 Extracting reports..."):
                text1 = extract_text(file1)
                text2 = extract_text(file2)

            with st.spinner("🤖 AI is analysing both reports..."):
                try:
                    analysis1 = analyse_report(text1)
                    analysis2 = analyse_report(text2)

                    st.success("✅ Comparison complete!")
                    st.divider()

                    st.subheader("📊 Head to Head Comparison")

                    headers = ["Metric", analysis1.get("company_name", "Company 1"), analysis2.get("company_name", "Company 2")]
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{headers[0]}**")
                    with col2:
                        st.write(f"**{headers[1]}**")
                    with col3:
                        st.write(f"**{headers[2]}**")

                    metrics = [
                        ("Financial Year", "financial_year"),
                        ("Sentiment", "sentiment"),
                        ("Revenue", "revenue"),
                        ("Net Profit", "profit"),
                        ("Revenue Growth", "revenue_growth"),
                        ("EBITDA", "ebitda"),
                        ("Dividend Per Share", "dividend"),
                        ("Employees", "employees"),
                    ]

                    for label, key in metrics:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**{label}**")
                        with col2:
                            st.write(analysis1.get(key, "N/A"))
                        with col3:
                            st.write(analysis2.get(key, "N/A"))

                    st.divider()

                    sentiment_map = {"positive": 3, "neutral": 2, "negative": 1}
                    fig = go.Figure(go.Bar(
                        x=[analysis1.get("company_name", "Company 1"), analysis2.get("company_name", "Company 2")],
                        y=[
                            sentiment_map.get(analysis1.get("sentiment", "neutral"), 2),
                            sentiment_map.get(analysis2.get("sentiment", "neutral"), 2)
                        ],
                        marker_color=["#00CC88", "#FF4B4B"],
                        text=[analysis1.get("sentiment", "neutral"), analysis2.get("sentiment", "neutral")],
                        textposition="auto"
                    ))
                    fig.update_layout(
                        title="Sentiment Comparison",
                        yaxis=dict(tickvals=[1, 2, 3], ticktext=["Negative", "Neutral", "Positive"]),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    st.divider()

                    col1, col2 = st.columns(2)
                    with col1:
                        display_analysis(analysis1, f"📋 {analysis1.get('company_name', 'Company 1')} Full Analysis")
                    with col2:
                        display_analysis(analysis2, f"📋 {analysis2.get('company_name', 'Company 2')} Full Analysis")

                except Exception as e:
                    st.error(f"Comparison failed: {str(e)}")