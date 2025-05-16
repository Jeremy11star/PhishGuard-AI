import streamlit as st
import pickle
import pandas as pd

# Load the trained model
@st.cache_resource
def load_model():
    with open('phishing_detector.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Extract features from URL for prediction
def extract_url_features(url):
    features = {}
    
    # Length features
    features['url_length'] = len(url)
    
    # Special character features
    features['contains_https'] = 1 if url.startswith('https') else 0
    features['dot_count'] = url.count('.')
    features['hyphen_count'] = url.count('-')
        
    return features

# Main function
def main():
    st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️")
    
    st.title("PhishGuard AI")
    st.subheader("AI-powered Phishing Detection and Awareness Tool")
    
    st.header("URL Phishing Detection")
    st.write("Enter a URL to check if it's potentially a phishing attempt.")
    
    url = st.text_input("URL to check:")
    
    if st.button("Analyze URL"):
        if url:
            with st.spinner("Analyzing URL..."):
                # Extract features
                features = extract_url_features(url)
                features_df = pd.DataFrame([features])
                
                # Make prediction
                model = load_model()
                prediction = model.predict(features_df)[0]
                probability = model.predict_proba(features_df)[0]
                
                # Display result
                if prediction == 1:
                    st.error(f"⚠️ This URL is likely a PHISHING attempt! (Confidence: {probability[1]:.2f})")
                else:
                    st.success(f"✅ This URL appears to be legitimate. (Confidence: {probability[0]:.2f})")
                
                # Show feature explanation
                st.subheader("Why did the AI make this decision?")
                st.write("Here are the features analyzed:")
                st.write(f"- URL length: {features['url_length']} characters")
                st.write(f"- Uses HTTPS: {'Yes' if features['contains_https'] else 'No'}")
                st.write(f"- Number of dots (.): {features['dot_count']}")
                st.write(f"- Number of hyphens (-): {features['hyphen_count']}")
                
                st.info("Our AI analyzes these features to determine risk. Longer URLs with many special characters are often suspicious.")
        else:
            st.warning("Please enter a URL to analyze.")
    
    st.markdown("---")
    
    st.header("About PhishGuard AI")
    st.write("""
    This tool uses machine learning to detect potential phishing URLs. 
    
    
    **How it works:**
    1. Enter a URL you want to check
    2. Our AI analyzes features like URL length, special characters, and domain properties
    3. The system provides an assessment with confidence score
    4. You can see which features influenced the decision
    """)

if __name__ == "__main__":
    main()