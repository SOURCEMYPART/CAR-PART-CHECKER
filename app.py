mport streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Car Part Price Checker", layout="centered")
st.title("🔍 Car Part Price Comparison & Profit Calculator")

part_number = st.text_input("Enter Car Part Number:")
your_cost_price = st.number_input("Enter Your Cost Price (£):", min_value=0.0, step=0.01)

def fetch_price(url, find_price, find_name):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        st.markdown("### Debug: EuroCarParts HTML Preview")
        st.code(soup.prettify()[:1500])

        name = soup.select_one(find_name).text.strip()
        price_text = soup.select_one(find_price).text.strip().replace("£", "").replace(",", "")
        price = float(price_text)
        return name, price, url
    except:
        return None, None, url

prices = []

if part_number:
    with st.spinner("Searching prices..."):
        # Euro Car Parts
        euro_url = f"https://www.eurocarparts.com/search/{part_number}"
        euro = fetch_price(euro_url, "span.price__total", "div.product__details a")
        if euro[1]:
            prices.append(("Euro Car Parts", euro[0], euro[1], euro[2]))

        # Halfords (example URL)
        halfords_url = f"https://www.halfords.com/search?q={part_number}"
        halfords = fetch_price(halfords_url, "span.product-price", "h2.product-name")
        if halfords[1]:
            prices.append(("Halfords", halfords[0], halfords[1], halfords[2]))

        # CarParts4Less
        cp4l_url = f"https://www.carparts4less.co.uk/search/{part_number}"
        cp4l = fetch_price(cp4l_url, "span.price", "a.productTitle")
        if cp4l[1]:
            prices.append(("CarParts4Less", cp4l[0], cp4l[1], cp4l[2]))

        # GSF (example scraping, update if structure changes)
        gsf_url = f"https://www.gsfcarparts.com/catalogsearch/result/?q={part_number}"
        gsf = fetch_price(gsf_url, "span.price", "a.product-item-link")
        if gsf[1]:
            prices.append(("GSF", gsf[0], gsf[1], gsf[2]))

    if prices:
        st.subheader("📦 Prices Found:")
        for name, title, price, link in prices:
            st.markdown(f"**{name}**: £{price:.2f} — [{title}]({link})")

        cheapest = min(prices, key=lambda x: x[2])
        margin = ((cheapest[2] - your_cost_price) / your_cost_price) * 100 if your_cost_price else 0

        st.markdown("---")
        st.success(f"💰 **Best Price:** £{cheapest[2]:.2f} from {cheapest[0]}")
        st.markdown(f"📈 **Your Profit Margin:** {margin:.2f}%")

        if margin >= 40:
            st.markdown("✅ Profit margin meets 40%+ goal.")
        else:
            st.warning("⚠️ Profit margin is below 40%. Consider adjusting price.")
    else:
        st.error("❌ No valid prices found.")
