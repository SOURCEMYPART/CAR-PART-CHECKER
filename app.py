
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import json

st.set_page_config(page_title="Car Part Price Checker", layout="centered")
st.title("🔍 Car Part Price Comparison & Profit Calculator")

part_number = st.text_input("Enter Car Part Number:")
your_cost_price = st.number_input("Enter Your Cost Price (ex VAT) (£):", min_value=0.0, step=0.01)
postcode = st.text_input("Enter Postcode (for stock check):", value="LU2 0GU")

vat_rate = 0.20
your_cost_price_inc_vat = your_cost_price * (1 + vat_rate)

def fetch_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text(separator='\n')
        m = re.search(r"£\s*([0-9]+(?:\.[0-9]{1,2}))", text)
        price = float(m.group(1)) if m else None
        title = soup.title.text.strip() if soup.title else url
        return title, price, url
    except:
        return None, None, url

def check_stock_graphql(part_number, postcode):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "Origin": "https://www.eurocarparts.com",
        "Referer": f"https://www.eurocarparts.com/p/{part_number}",
        "x-app-ver": "skyrocket"
    }

    graphql_query = {
        "operationName": "GetStockAvailability",
        "variables": {
            "sku": part_number,
            "postcode": postcode.replace(" ", "")
        },
        "query": '''
        query GetStockAvailability($sku: String!, $postcode: String!) {
            stockAvailability(sku: $sku, postcode: $postcode) {
                branchName
                branchId
                available
                quantity
            }
        }
        '''
    }

    try:
        res = requests.post("https://www.eurocarparts.com/api/graphql", headers=headers, data=json.dumps(graphql_query), timeout=10)
        stock_data = res.json().get("data", {}).get("stockAvailability", [])
        result = {}
        for branch in stock_data:
            name = branch.get("branchName")
            qty = branch.get("quantity")
            available = branch.get("available")
            result[name] = (available, qty)
        return result
    except Exception as e:
        return {"Error": (False, None)}

prices = []

if part_number:
    with st.spinner("Searching prices..."):
        euro_url = f"https://www.eurocarparts.com/search/{part_number}"
        euro = fetch_price(euro_url)
        if euro[1]:
            prices.append(("Euro Car Parts", euro[0], euro[1], euro[2]))

        halfords_url = f"https://www.halfords.com/search?q={part_number}"
        halfords = fetch_price(halfords_url)
        if halfords[1]:
            prices.append(("Halfords", halfords[0], halfords[1], halfords[2]))

        cp4l_url = f"https://www.carparts4less.co.uk/search/{part_number}"
        cp4l = fetch_price(cp4l_url)
        if cp4l[1]:
            prices.append(("CarParts4Less", cp4l[0], cp4l[1], cp4l[2]))

        gsf_url = f"https://www.gsfcarparts.com/catalogsearch/result/?q={part_number}"
        gsf = fetch_price(gsf_url)
        if gsf[1]:
            prices.append(("GSF", gsf[0], gsf[1], gsf[2]))

    if prices:
        st.subheader("📦 Prices Found:")
        for name, title, price, link in prices:
            st.markdown(f"**{name}**: £{price:.2f} — [{title}]({link})")

        cheapest = min(prices, key=lambda x: x[2])
        margin = ((cheapest[2] - your_cost_price_inc_vat) / your_cost_price_inc_vat) * 100 if your_cost_price else 0

        st.markdown("---")
        st.success(f"💰 **Best Price:** £{cheapest[2]:.2f} from {cheapest[0]}")
        st.markdown(f"💼 **Your Cost (inc. VAT):** £{your_cost_price_inc_vat:.2f}")
        target_price = your_cost_price_inc_vat * 1.40
        st.markdown(f"🚀 **Target Selling Price (40% Markup):** £{target_price:.2f}")
        st.markdown(f"📈 **Your Profit Margin:** {margin:.2f}%")

        if margin >= 40:
            st.markdown("✅ Profit margin meets 40%+ goal.")
        else:
            st.warning("⚠️ Profit margin is below 40%. Consider adjusting price.")
    else:
        st.error("❌ No valid prices found.")

    st.subheader("🏬 Euro Car Parts Live Stock Check (GraphQL)")
    stock_info = check_stock_graphql(part_number, postcode)
    for loc, (avail, qty) in stock_info.items():
        status = f"✅ In stock ({qty} pcs)" if avail else "❌ Out of stock"
        st.write(f"**{loc}:** {status}")
