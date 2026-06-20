import streamlit as st
from extractor import extract_text
from analyser import analyse_report

st.set_page_config(
    page_title="ASX Financial Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 ASX Financial Report Intelligence Platform")
st.subheader("AI Powered Annual Report Analysis")
st.write("Upload any ASX company annual report and get instant AI powered insights.")

uploaded_file = st.file_uploader(
    "Upload ASX Annual Report (PDF)",
    type="pdf"
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    
    if st.button("Analyse Report", type="primary"):
        
        with st.spinner("Extracting report text..."):
            text = extract_text(uploaded_file)
        
        if not text:
            st.error("Could not extract text from this PDF. Please try another file.")
        else:
            with st.spinner("AI is analysing the report..."):
                try:
                    analysis = analyse_report(text)
                    
                    st.success("Analysis complete!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🏢 Company")
                        st.write(analysis.get("company_name", "Unknown"))
                        
                        st.subheader("📈 Sentiment")
                        sentiment = analysis.get("sentiment", "neutral")
                        if sentiment == "positive":
                            st.success("Positive")
                        elif sentiment == "negative":
                            st.error("Negative")
                        else:
                            st.warning("Neutral")
                        
                        st.subheader("💰 Revenue")
                        st.write(analysis.get("revenue", "Not found"))
                        
                        st.subheader("💵 Profit")
                        st.write(analysis.get("profit", "Not found"))
                    
                    with col2:
                        st.subheader("⚠️ Key Risks")
                        for risk in analysis.get("risks", []):
                            st.warning(risk)
                        
                        st.subheader("🚀 Growth Opportunities")
                        for opp in analysis.get("opportunities", []):
                            st.success(opp)
                    
                    st.subheader("📝 Executive Summary")
                    st.info(analysis.get("executive_summary", "No summary available"))
                    
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")