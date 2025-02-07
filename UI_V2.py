import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from datetime import datetime, timedelta

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Thin.ttc'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# Sample data (replace with actual data loading method)
data = {
    "查核名稱":["202408-服務完善"] * 8,
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


data2 = {
    "查核名稱":["自訂查核"] ,
    "敏感詞": ["NCC"],
    "關鍵詞": ["謝謝"],
    "長度": ["09”37"],
    "日期/時間": [
        "2025-02-10 11:32"
    ],
        "下載語音轉錄結果": ["📥"] ,
        "通話回放": ["▶️"] 
}

data3 = {
        "帳號": ["abc123"],
        "角色": ["管理員"],
        "權限": ["管理設定, 查看報告, 下載數據, 查看報告, 下載數據, 查看報告"],
        "敏感詞通知": ["Y"]
    }

months = pd.date_range(start='2023-03-01', end='2024-02-29', freq='ME')
monthly_data = pd.DataFrame({
    '月份': months,
    '查核項目總數': np.random.randint(70, 100, size=12),
    '查核專員數': np.random.randint(35, 50, size=12),
    '敏感詞次數': np.random.randint(220, 300, size=12),
    '關鍵字次數': np.random.randint(330, 450, size=12)
})
# Set 月份 as index before calculations
monthly_data = monthly_data.set_index('月份')

# Calculate percentages
monthly_data['敏感詞占比'] = (monthly_data['敏感詞次數'] / monthly_data['查核項目總數'] * 100).round(1)
monthly_data['關鍵詞占比'] = (monthly_data['關鍵字次數'] / monthly_data['查核項目總數'] * 100).round(1)



df = pd.DataFrame(data)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df["日期/時間"] = pd.to_datetime(df["日期/時間"])
st.title("客服查核系統")


# Sidebar Navigation
st.sidebar.title("功能選單")
page = st.sidebar.radio("選擇頁面", ["首頁", "質檢查核", "特定音檔查核", "系統設定"])

if page == "首頁":

    tab1, tab2, tab3 = st.tabs(["最近一次查核總覽", "當月統計", "當年趨勢"])
        
    with tab1:
        st.subheader("最近一次查核總覽")
        st.dataframe(df)
    with tab2:  
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

        # Create pie chart for sensitive words
        sensitive_words_data = {
            'NCC': 7,
            '個資': 2,
            '違規': 1
        }
        fig1 = plt.figure(figsize=(10, 6))
        plt.pie(sensitive_words_data.values(), labels=sensitive_words_data.keys(), autopct='%1.1f%%')
        plt.title('敏感詞分布')
        st.pyplot(fig1)

    with tab3:

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


        st.subheader("數量趨勢")
        st.area_chart(monthly_data[['查核項目總數', '查核專員數', '敏感詞次數', '關鍵字次數']])
        
        st.subheader("近一年統計趨勢")
        st.dataframe(monthly_data.transpose(), height=400)
        # 添加下載按鈕
        csv = monthly_data.transpose().to_csv().encode('utf-8')
        st.download_button(
            label="下載CSV檔案",
            data=csv,
            file_name="monthly_stats.csv",
            mime="text/csv"
        )

elif page == "質檢查核":
    st.header("質檢查核")
    st.write("上傳質檢查核清單，系統批次轉錄音檔產出查核結果。")
    uploaded_rule = st.file_uploader("上傳質檢查核", type=["xlsx", "csv", "txt"])
    if uploaded_rule is not None:
        st.write("質檢查核清單: ", uploaded_rule.name)
        st.write("查核名稱: ", "202408-服務完善")
        st.write("關鍵字: ", "謝謝;服務;需要幫忙")
        st.write("敏感詞: ", "NCC")
        if st.button("開始質檢查核"):
            st.success("查核完成，查核結果已產出！")
            st.write("查核完成：")
            st.dataframe(df)
            st.download_button("下載查核結果", "dummy_data", file_name="查核結果.csv")

    # Date filter
    start_date = st.date_input("選擇開始日期", df["日期/時間"].min().date())
    end_date = st.date_input("選擇結束日期", df["日期/時間"].max().date())
    filtered_df = df[(df["日期/時間"].dt.date >= start_date) & (df["日期/時間"].dt.date <= end_date)]
    
    selected_agent = st.selectbox("選擇專員", ["全部"] + list(filtered_df["專員"].unique()))
    if selected_agent != "全部":
        filtered_df = filtered_df[filtered_df["專員"] == selected_agent]
    st.dataframe(filtered_df)

elif page == "特定音檔查核":
    st.header("特定音檔查核")
    st.write("選擇特定音檔，設定關鍵詞與敏感詞後產出查核結果。")
    uploaded_audio = st.file_uploader("上傳音檔", type=["mp3", "wav"])
    keywords = st.text_area("輸入關鍵詞 (以逗號分隔),e.g.謝謝")
    sensitive_words = st.text_area("輸入敏感詞 (以逗號分隔),e.g.NCC")
    if uploaded_audio and keywords and sensitive_words:
        st.write("已上傳音檔: ", uploaded_audio.name)
        if st.button("開始查核"):
            st.success("查核完成，結果已產出！")
            st.write("範例查核結果：")
            st.dataframe(df2)

            st.write("對話紀錄：")

            def highlight_text(text, target="謝謝", color="red"):
                return text.replace(target, f'<span style="color: {color}">{target}</span>')
            
            st.write(" SPEAKER_00 (0.0s - 14.4s): 您好，陳先生您好，不好意思，我這邊是中央官民數位天空客服中心。")
            text = " SPEAKER_00 (14.4s - 20.0s): 你好，謝謝。"
            st.markdown(highlight_text(text), unsafe_allow_html=True)

elif page == "系統設定":
    st.header("系統設定")
    st.subheader("角色權限與敏感詞通知設定")
    
    # 預設角色權限資料
    role_data = pd.DataFrame({
        "角色": ["管理員", "主管", "專員"],
        "權限": ["管理設定, 查看報告, 下載數據", "查看報告, 下載數據", "查看報告"]
    })
    st.write("已設定的角色清單")
    st.dataframe(role_data)
    account =st.text_area("輸入帳號,e.g.abc123")
    roles = ["管理員", "主管", "專員"]
    selected_role = st.selectbox("選擇角色", roles)
    permissions = st.multiselect("選擇權限", ["查看報告", "下載數據", "管理設定", "調整權限", "管理敏感詞通知"])
    email_recipients = st.text_area("輸入通知信箱 (以逗號分隔),e.g.abc123@homeplus.net.tw")
    if st.button("儲存設定"):
        st.write(f"{selected_role} 角色已更新權限: {', '.join(permissions)}")
        st.write(f"已儲存信件通知設定: {email_recipients}")
        st.dataframe(df3)
    
