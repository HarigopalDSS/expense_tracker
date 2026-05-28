import streamlit as st
import requests
import pandas as pd
server_loc="http://127.0.0.1:8000"
st.set_page_config(page_title="Expense Tracker", layout="wide")


def call_api(method, path, payload=None):
    try:
        response = requests.request(
            method,
            f"{server_loc}{path}",
            json=payload,
            timeout=8,
        )
        try:
            data = response.json()
        except ValueError:
            data = {"message": "Invalid response from server"}
        return response, data
    except requests.exceptions.RequestException as exc:
        return None, {"message": f"Server connection failed: {exc}"}


st.title("💰EXPENSIVE TRACKER")
st.caption("Frontend loaded successfully")

health_response, _ = call_api("GET", "/view_exp")
if health_response is None:
    st.warning("Backend is not reachable at http://127.0.0.1:8000. UI is active, but API actions may fail.")
else:
    st.success("Backend connection OK")

opt=st.sidebar.selectbox("choose operations:--",["add_expression","view_expression","update_expression","delete_expression","search_expression","sort_expression"])
if opt == "add_expression":
    st.header("➕ ADDING EXPENSES")
    with st.form("add_expression"):
        name = st.text_input("👤Name")
        amount=st.number_input("💵amount")
        category=st.selectbox("category",[ "🍔 Food",
                "✈️ Travel",
                "🏠 Rent",
                "👕costume"])
        date=st.date_input("📅 Enter the date")
        btn=st.form_submit_button("add_expression")
        if btn:
            
            
            new_data = {
                "n":name,
                "a":amount,
                "c":category,
                "d":str(date)
            }
            response, data = call_api("POST", "/add_exp", new_data)
            st.write(data)
            if response and response.status_code == 200:
                st.success("✅THE AMOUNT WAS SUFFICENT")
            else:
                st.error("❌ THE AMOUNT WAS NOT SUFFICENT")
elif opt== "view_expression":
    st.header("📋 VEIW EXPENSES")
    btn=st.button("view data")
    if btn:
        response, data = call_api("GET", "/view_exp")
        if response and isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df)
        elif response and isinstance(data, list):
            st.warning("No employee data found")
        else:
            st.error(data.get("message", "Failed to fetch expenses"))
elif opt == "update_expression":

    st.header("✏️ UPDATED EXPENSES")

    with st.form("update_expression_form"):
        id = st.number_input("Enter Employee ID", min_value=1)

        name = st.text_input("👤 Name")

        amount = st.number_input(
            "💵 Amount",
            min_value=0.0,
            format="%.2f"
        )

        category = st.selectbox(
            "📂 Category",
            [
                "🍔 Food",
                "✈️ Travel",
                "🏠 Rent",
                "👕 Costume"
            ]
        )

        date = st.date_input("📅 Select Date")

        update_btn = st.form_submit_button("Update Expense")

        if update_btn:

            updated_data = {
                "n": name,
                "a": amount,
                "c": category,
                "d": str(date)
            }
            response, data = call_api("PUT", f"/upd_exp/{id}", updated_data)

            if response and response.status_code == 200:
                st.success("✅ Expense Updated Successfully")
                st.write(data)
            elif response:
                st.error("❌ Expense Not Found")
                st.write(data)
            else:
                st.error(data.get("message", "Unable to connect to FastAPI server"))
elif opt  == "delete_expression":
    st.header("DELETE EXPENSES")
    id=st.number_input("🆔enter id", min_value=1)
    if st.button("🗑️ Delete Employee"):
        response, data = call_api("DELETE", f"/delete_exp/{id}")

        st.write(data)

        if response and response.status_code == 200:
            st.success("✅ Employee deleted successfully")
        else:
            st.error("❌Delete failed")
if opt=="search_expression":
    st.header("SEARCH DETAILS")
    id=st.number_input("enter the number")
    if st.button("search expression"):
        response, data = call_api("GET", f"/srh_exp/{id}")
        st.write(data)
        
        if response and response.status_code == 200:
                if "message" not in data:

                    st.success("✅ Expense Found")

                    df = pd.DataFrame([data])

                    st.dataframe(df)

                else:

                    st.warning("⚠️ Expense ID Not Found")

                    st.write(data)

        else:

                st.error("❌ Search Failed")
elif opt== "sort_expression":
    st.header("SORTING EXPRESSIONS")
    sort_by = st.selectbox(
        "🔽 Select Sort Column",
        [
            "id",
            "name",
            "amount",
            "category",
            "expense_date"
        ]
    )

    order = st.selectbox(
        "↕️ Select Order",
        [
            "ASC",
            "DESC"
        ]
    )

    if st.button("📊 Sort Expenses"):

        try:

            response = requests.get(
                f"{server_loc}/sort_exp/{sort_by}/{order}"
            )

            data = response.json()

            st.write(data)

            if response.status_code == 200:

                if len(data) > 0:

                    st.success("✅ Expenses Sorted Successfully")

                    df = pd.DataFrame(data)

                    st.dataframe(df)

                else:

                    st.warning("⚠️ No Data Found")

            else:

                st.error("❌ Sorting Failed")

            except requests.exceptions.ConnectionError:

                st.error("🚫 Unable to connect to FastAPI Server") 