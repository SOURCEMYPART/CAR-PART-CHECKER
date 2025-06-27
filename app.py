
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Car Part Price Checker", layout="centered")
st.title("🔍 Car Part Price Checker 🔧")

# --- Get Euro Car Parts Price ---
def get_euro_price(part_number):
    try:
        url = f"https://www.eurocarparts.com/search/{part_number}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Debug: Save HTML sample
        st.text("🔍 Euro Car Parts HTML Sample:")
        st.code(response.text[:1000], language="html")

        # Try common price class
        price_tag = soup.find("span", class_="product-price__price")
        if not price_tag:
            price_tag = soup.find("div", class_="price")  # Fallback class

        if price_tag:
            return price_tag.get_text(strip=True)
        else:
            return "❌ Price not found (HTML structure may have changed)"
    except Exception as e:
        return f"⚠️ EuroCarParts Error: {e}"

# --- Get Halfords Price ---
def get_halfords_price(part_number):
    try:
        url = f"https://www.halfords.com/search?q={part_number}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Debug: Save HTML sample
        st.text("🔍 Halfords HTML Sample:")
        st.code(response.text[:1000], language="html")

        # Try finding a price
        price_tag = soup.find("span", class_="product-card-price__current-price")
        if not price_tag:
            price_tag = soup.find("div", class_="price")  # Fallback

        if price_tag:
            return price_tag.get_text(strip=True)
        else:
            return "❌ Price not found (HTML structure may have changed)"
    except Exception as e:
        return f"⚠️ Halfords Error: {e}"

# --- Main UI ---
part_number = st.text_input("Enter Car Part Number:")

if part_number:
    st.subheader("💰 Live Prices")

    euro_price = get_euro_price(part_number)
    halfords_price = get_halfords_price(part_number)

    st.markdown(f"**🔧 Euro Car Parts:** {euro_price}")
    st.markdown(f"**🛠️ Halfords:** {halfords_price}")
