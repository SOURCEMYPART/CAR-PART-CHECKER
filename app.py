
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Car Part Price Checker", layout="centered")
st.title("🔍 Car Part Price Comparison Dashboard")

part_number = st.text_input("Enter Car Part Number:")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_price_eurocarparts(part_number):
    try:
        url = f"https://www.eurocarparts.com/search/{part_number}"
        if show_debug:
    st.text("🔧 Euro Car Parts HTML:")
    st.code(soup.prettify()[:2000], language="html")
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        price_tag = soup.find("span", class_="value")
        if price_tag:
            return float(price_tag.text.strip().replace("£", "").replace(",", ""))
    except:
        pass
    return None

def get_price_halfords(part_number):
    try:
        url = f"https://www.halfords.com/search?q={part_number}"
        if show_debug:
    st.text("🔧 Euro Car Parts HTML:")
    st.code(soup.prettify()[:2000], language="html")
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        price_tag = soup.find("span", class_="product-card-price__current-value")
        if price_tag:
            return float(price_tag.text.strip().replace("£", "").replace(",", ""))
    except:
        pass
    return None

def get_price_carparts4less(part_number):
    try:
        url = f"https://www.carparts4less.co.uk/search/{part_number}"
        if show_debug:
    st.text("🔧 Euro Car Parts HTML:")
    st.code(soup.prettify()[:2000], language="html")
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        price_tag = soup.find("span", class_="Price")
        if price_tag:
            return float(price_tag.text.strip().replace("£", "").replace(",", ""))
    except:
        pass
    return None

if part_number:
    st.write("Searching live prices...")

    euro_price = get_price_eurocarparts(part_number)
    halfords_price = get_price_halfords(part_number)
    cp4l_price = get_price_carparts4less(part_number)

    st.subheader("📦 Prices Found:")

    if euro_price:
        st.write(f"Euro Car Parts: £{euro_price}")
    else:
        st.write("Euro Car Parts: ❌ Not found")

    if halfords_price:
        st.write(f"Halfords: £{halfords_price}")
    else:
        st.write("Halfords: ❌ Not found")

    if cp4l_price:
        st.write(f"CarParts4Less: £{cp4l_price}")
    else:
        st.write("CarParts4Less: ❌ Not found")

    valid_prices = [p for p in [euro_price, halfords_price, cp4l_price] if p is not None]

    if valid_prices:
        cheapest = min(valid_prices)
        average = sum(valid_prices) / len(valid_prices)

        st.subheader("💰 Summary")
        st.write(f"Cheapest Price: £{cheapest:.2f}")
        st.write(f"Average Price: £{average:.2f}")

        st.subheader("📈 Profit Calculator")
        margin = 30
        sale_price = cheapest * (1 + margin / 100)
        st.write(f"Suggested Selling Price (30% markup): £{sale_price:.2f}")
    else:
        st.warning("No valid prices found from suppliers.")
