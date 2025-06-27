
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

st.set_page_config(page_title="Car Part Price Checker", layout="centered")
st.title("🔍 Car Part Price Checker 🔧")

def get_euro_price(part_number):
    try:
        search_url = f"https://www.eurocarparts.com/search/{part_number}"
        resp = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        st.text("🔍 Euro Search Page HTML Sample:")
        st.code(resp.text[:1000], language="html")

        # Find first product link
        link_tag = soup.select_one("a[href*='/p/']")
        if not link_tag:
            return "❌ No product link found on search page"
        product_url = urljoin(search_url, link_tag["href"])

        # Load product detail page
        resp2 = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"})
        resp2.raise_for_status()
        soup2 = BeautifulSoup(resp2.text, "html.parser")
        st.text("🔍 Euro Product Page HTML Sample:")
        st.code(resp2.text[:1000], language="html")

        price_tag = soup2.select_one("span.product-price__price")
        if price_tag:
            return price_tag.get_text(strip=True)
        else:
            return "❌ Price not found on product page (structure may have changed)"

    except Exception as e:
        return f"⚠️ EuroCarParts Error: {e}"

def get_halfords_price(part_number):
    try:
        search_url = f"https://www.halfords.com/search?q={part_number}"
        resp = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        st.text("🔍 Halfords HTML Sample:")
        st.code(resp.text[:1000], language="html")

        price_tag = soup.find("span", class_="product-card-price__current-price")
        if price_tag:
            return price_tag.get_text(strip=True)
        else:
            return "❌ Price not found"

    except Exception as e:
        return f"⚠️ Halfords Error: {e}"

part_number = st.text_input("Enter Car Part Number:")

if part_number:
    st.subheader("💰 Live Prices")
    euro_price = get_euro_price(part_number)
    halfords_price = get_halfords_price(part_number)

    st.markdown(f"**🔧 Euro Car Parts:** {euro_price}")
    st.markdown(f"**🛠️ Halfords:** {halfords_price}")
