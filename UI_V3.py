import streamlit as st
import pandas as pd
from datetime import datetime

# Sample data (replace with actual data loading method)
data = {
    "查核名稱": ["202408-服務完善"] * 8,
    "專員": [4062, 3003, 4001, 3001, 3002, 4033, 4024, 3008],
    "去電號碼": ["09XX-XXX-XXX"] * 8,
    "IB/OB": ["IB"] * 8,
    "基本質檢": ["異常"] * 8,
    "敏感詞": ["NCC", "1999", "1999", "1999", "1999", "1999", "1999", "1999"],
    "關鍵詞": ["中華電信", "", "中華電信", "帳單", "帳單", "帳單", "", ""],
    "長度": ["09”37", "04”31", "07”08", "06”25", "13”08", "05”55", "28”21", "05”07"],
    "日期/時間": [
        "2024-08-10 11:32", "2024-08-10 14:05", "2024-08-10 14:26",
        "2024-08-10 16:34", "2024-08-10 17:46", "2024-08-10 18:49",
        "2024-08-10 18:59", "2024-08-11 17:44"
    ],
    "下載語音轉錄結果": ["📥"] * 8,
    "通話回放": ["▶️"] * 8
}

df = pd.DataFrame(data)
df["日期/時間"] = pd.to_datetime(df["日期/時間"])

st.title("客服智慧助手平台")

# Sidebar Navigation
st.sidebar.title("功能選單")
page = st.sidebar.radio("選擇頁面", ["首頁", "質檢查核", "特定音檔查核", "培訓教案生成", "最佳話術生成", "AI智庫查詢", "系統設定"])

if page == "首頁":
    st.subheader("最近一次查核總覽")
    st.dataframe(df)
    
    st.subheader("最近一個月統計")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("查核項目總數", 10)
    with col2:
        st.metric("查核專員數", 15)
    with col3:
        st.metric("敏感詞次數", 30)
    with col4:
        st.metric("關鍵字次數", 45)
    
    st.subheader("近一年統計")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("查核項目總數", 100)
    with col2:
        st.metric("查核專員數", 50)
    with col3:
        st.metric("敏感詞次數", 300)
    with col4:
        st.metric("關鍵字次數", 450)

elif page == "質檢查核":
    st.header("質檢查核")
    uploaded_rule = st.file_uploader("上傳質檢查核", type=["xlsx", "csv", "txt"])
    if uploaded_rule:
        st.write("查核名稱: 202408-服務完善")
        st.write("關鍵字: 謝謝;服務;需要幫忙")
        st.write("敏感詞: NCC")
        if st.button("開始質檢查核"):
            st.success("查核完成！")
            st.dataframe(df)
            st.download_button("下載查核結果", "dummy_data", file_name="查核結果.csv")

elif page == "特定音檔查核":
    st.header("特定音檔查核")
    uploaded_audio = st.file_uploader("上傳音檔", type=["mp3", "wav"])
    keywords = st.text_area("輸入關鍵詞 (以逗號分隔)")
    sensitive_words = st.text_area("輸入敏感詞 (以逗號分隔)")
    if uploaded_audio and keywords and sensitive_words:
        if st.button("開始查核"):
            st.success("查核完成！")
            st.dataframe(df)

elif page == "培訓教案生成":
    st.header("培訓教案生成功能")
    topic = st.text_input("輸入培訓主題")
    if st.button("生成培訓教案"):
        st.success("培訓教案已生成！")
        st.text_area("生成結果", "這是一個示例教案...", height=200)

elif page == "最佳話術生成":
    st.header("最佳話術生成功能")
    scenario = st.text_input("輸入情境描述")
    if st.button("生成最佳話術"):
        st.success("話術已生成！")
        st.text_area("生成結果", "您好！很高興為您服務...", height=200)

elif page == "AI智庫查詢":
    st.header("AI智庫查詢")
    query = st.text_input("輸入查詢內容")
    if st.button("查詢"):
        st.success("查詢完成！")
        st.text_area("查詢結果", "這是與您的查詢相關的內容...", height=200)

elif page == "系統設定":
    st.header("系統設定")
    st.subheader("角色權限與敏感詞通知設定")
    roles = ["管理員", "主管", "專員"]
    selected_role = st.selectbox("選擇角色", roles)
    permissions = st.multiselect("選擇權限", ["查看報告", "下載數據", "管理設定", "調整權限", "管理敏感詞通知"])
    email_recipients = st.text_area("輸入通知信箱 (以逗號分隔)")
    if st.button("儲存設定"):
        st.write(f"{selected_role} 角色已更新權限: {', '.join(permissions)}")
        st.write(f"已儲存信件通知設定: {email_recipients}")
