import streamlit as st
import pandas as pd
import joblib
import numpy as np

model = joblib.load("model_estimate_price_house_v5.pkl")
encoder = joblib.load("encoder_v5.pkl")

numeric_columns = ['Diện tích', 'Số tầng', 'Số phòng ngủ', 'Số nhà vệ sinh']
categorical_columns = ['Hướng cửa chính', 'Loại hình nhà ở', 'Tên phường', 'Quận']

# Hằng số cho tên phường để tránh trùng lặp
WARD_01 = "Phường 01"
WARD_02 = "Phường 02"
WARD_03 = "Phường 03"
WARD_04 = "Phường 04"
WARD_05 = "Phường 05"
WARD_06 = "Phường 06"
WARD_07 = "Phường 07"
WARD_08 = "Phường 08"
WARD_09 = "Phường 09"
WARD_10 = "Phường 10"
WARD_11 = "Phường 11"
WARD_12 = "Phường 12"
WARD_13 = "Phường 13"
WARD_14 = "Phường 14"
WARD_15 = "Phường 15"
WARD_16 = "Phường 16"
WARD_17 = "Phường 17"
WARD_18 = "Phường 18"
WARD_19 = "Phường 19"
WARD_21 = "Phường 21"
WARD_22 = "Phường 22"
WARD_24 = "Phường 24"
WARD_25 = "Phường 25"
WARD_26 = "Phường 26"
WARD_27 = "Phường 27"
WARD_28 = "Phường 28"

district_to_wards = {
    "Quận 1": [
        "Phường Tân Định", "Phường Đa Kao", "Phường Bến Nghé",
        "Phường Bến Thành", "Phường Nguyễn Thái Bình", "Phường Phạm Ngũ Lão",
        "Phường Cầu Ông Lãnh", "Phường Cô Giang", "Phường Nguyễn Cư Trinh",
        "Phường Cầu Kho"
    ],
    "Quận 2": [
        "Phường Thảo Điền", "Phường An Phú", "Phường Bình An",
        "Phường Bình Trưng Đông", "Phường Bình Trưng Tây", "Phường Bình Khánh",
        "Phường An Khánh", "Phường Cát Lái", "Phường Thạnh Mỹ Lợi",
        "Phường An Lợi Đông", "Phường Thủ Thiêm"
    ],
    "Quận 3": [
        WARD_08, WARD_07, WARD_14, WARD_12,
        WARD_11, WARD_13, WARD_06, WARD_09,
        WARD_10, WARD_04, WARD_05, WARD_03,
        WARD_02, WARD_01
    ],
    "Quận 4": [
        WARD_12, WARD_13, WARD_09, WARD_06, WARD_08,
        WARD_10, WARD_05, WARD_18, WARD_14, WARD_04,
        WARD_03, WARD_16, WARD_02, WARD_15, WARD_01
    ],
    "Quận 5": [
        WARD_04, WARD_09, WARD_03, WARD_12, WARD_02,
        WARD_08, WARD_15, WARD_07, WARD_01, WARD_11,
        WARD_14, WARD_05, WARD_06, WARD_10, WARD_13
    ],
    "Quận 6": [
        WARD_14, WARD_13, WARD_09, WARD_06, WARD_12,
        WARD_05, WARD_11, WARD_02, WARD_01, WARD_04,
        WARD_08, WARD_03, WARD_07, WARD_10
    ],
    "Quận 7": [
        "Phường Tân Thuận Đông", "Phường Tân Thuận Tây", "Phường Tân Kiểng",
        "Phường Tân Hưng", "Phường Bình Thuận", "Phường Tân Quy",
        "Phường Phú Thuận", "Phường Tân Phú", "Phường Tân Phong", "Phường Phú Mỹ"
    ],
    "Quận 8": [
        WARD_08, WARD_02, WARD_01, WARD_03, WARD_11,
        WARD_09, WARD_10, WARD_04, WARD_13, WARD_12,
        WARD_05, WARD_14, WARD_06, WARD_15, WARD_16,
        WARD_07
    ],
    "Quận 9": [
        "Phường Long Bình", "Phường Long Thạnh Mỹ", "Phường Tân Phú",
        "Phường Hiệp Phú", "Phường Tăng Nhơn Phú A", "Phường Tăng Nhơn Phú B",
        "Phường Phước Long B", "Phường Phước Long A", "Phường Trường Thạnh",
        "Phường Long Phước", "Phường Long Trường", "Phường Phước Bình",
        "Phường Phú Hữu"
    ],
    "Quận 10": [
        WARD_15, WARD_13, WARD_14, WARD_12, WARD_11,
        WARD_10, WARD_09, WARD_01, WARD_08, WARD_02,
        WARD_04, WARD_07, WARD_05, WARD_06, WARD_03
    ],
    "Quận 11": [
        WARD_15, WARD_05, WARD_14, WARD_11, WARD_03,
        WARD_10, WARD_13, WARD_08, WARD_09, WARD_12,
        WARD_07, WARD_06, WARD_04, WARD_01, WARD_02,
        WARD_16
    ],
    "Quận 12": [
        "Phường Thạnh Xuân", "Phường Thạnh Lộc", "Phường Hiệp Thành",
        "Phường Thới An", "Phường Tân Chánh Hiệp", "Phường An Phú Đông",
        "Phường Tân Thới Hiệp", "Phường Trung Mỹ Tây", "Phường Tân Hưng Thuận",
        "Phường Đông Hưng Thuận", "Phường Tân Thới Nhất"
    ],
    "Quận Bình Thạnh": [
        WARD_13, WARD_11, WARD_27, WARD_26, WARD_12,
        WARD_25, WARD_05, WARD_07, WARD_24, WARD_06,
        WARD_14, WARD_15, WARD_02, WARD_01, WARD_03,
        WARD_17, WARD_21, WARD_22, WARD_19, WARD_28
    ],
    "Quận Bình Tân": [
        "Phường Bình Hưng Hòa", "Phường Bình Hưng Hòa A", "Phường Bình Hưng Hòa B",
        "Phường Bình Trị Đông", "Phường Bình Trị Đông A", "Phường Bình Trị Đông B",
        "Phường Tân Tạo", "Phường Tân Tạo A", "Phường An Lạc", "Phường An Lạc A"
    ],
    "Quận Gò Vấp": [
        WARD_15, WARD_13, WARD_17, WARD_06, WARD_16,
        WARD_12, WARD_14, WARD_10, WARD_05, WARD_07,
        WARD_04, WARD_01, WARD_09, WARD_08, WARD_11,
        WARD_03
    ],
    "Quận Phú Nhuận": [
        WARD_04, WARD_05, WARD_09, WARD_07, WARD_03,
        WARD_01, WARD_02, WARD_08, WARD_15, WARD_10,
        WARD_11, WARD_17, WARD_14, WARD_12, WARD_13
    ],
    "Quận Tân Bình": [
        WARD_02, WARD_04, WARD_12, WARD_13, WARD_01,
        WARD_03, WARD_11, WARD_07, WARD_05, WARD_10,
        WARD_06, WARD_08, WARD_09, WARD_14, WARD_15
    ],
    "Quận Tân Phú": [
        "Phường Tân Sơn Nhì", "Phường Tây Thạnh", "Phường Sơn Kỳ",
        "Phường Tân Quý", "Phường Tân Thành", "Phường Phú Thọ Hòa",
        "Phường Phú Thạnh", "Phường Phú Trung", "Phường Hòa Thạnh",
        "Phường Hiệp Tân", "Phường Tân Thới Hòa"
    ],
    "Quận Thủ Đức": [
        "Phường Linh Xuân", "Phường Bình Chiểu", "Phường Linh Trung",
        "Phường Tam Bình", "Phường Tam Phú", "Phường Hiệp Bình Phước",
        "Phường Hiệp Bình Chánh", "Phường Linh Chiểu", "Phường Linh Tây",
        "Phường Linh Đông", "Phường Bình Thọ", "Phường Trường Thọ"
    ],
     "Huyện Hóc Môn": [
        "Thị trấn Hóc Môn", "Xã Tân Hiệp", "Xã Nhị Bình", "Xã Đông Thạnh",
        "Xã Tân Thới Nhì", "Xã Thới Tam Thôn", "Xã Xuân Thới Sơn",
        "Xã Tân Xuân", "Xã Xuân Thới Đông", "Xã Trung Chánh",
        "Xã Xuân Thới Thượng", "Xã Bà Điểm"
    ],
    "Huyện Bình Chánh": [
        "Thị trấn Tân Túc", "Xã Phạm Văn Hai", "Xã Vĩnh Lộc A", "Xã Vĩnh Lộc B",
        "Xã Bình Lợi", "Xã Lê Minh Xuân", "Xã Tân Nhựt", "Xã Tân Kiên",
        "Xã Bình Hưng", "Xã Phong Phú", "Xã An Phú Tây", "Xã Hưng Long",
        "Xã Đa Phước", "Xã Tân Quý Tây", "Xã Bình Chánh", "Xã Quy Đức"
    ],
    "Huyện Nhà Bè": [
        "Thị trấn Nhà Bè", "Xã Phước Kiển", "Xã Phước Lộc",
        "Xã Nhơn Đức", "Xã Phú Xuân", "Xã Long Thới", "Xã Hiệp Phước"
    ],
    "Huyện Cần Giờ": [
        "Thị trấn Cần Thạnh", "Xã Bình Khánh", "Xã Tam Thôn Hiệp",
        "Xã An Thới Đông", "Xã Thạnh An", "Xã Long Hòa", "Xã Lý Nhơn"
    ],
    "Huyện Củ Chi": [
        "Thị trấn Củ Chi", "Xã Phú Mỹ Hưng", "Xã An Phú",
        "Xã Trung Lập Thượng", "Xã An Nhơn Tây", "Xã Nhuận Đức",
        "Xã Phạm Văn Cội", "Xã Phú Hòa Đông", "Xã Trung Lập Hạ",
        "Xã Trung An", "Xã Phước Thạnh", "Xã Phước Hiệp",
        "Xã Tân An Hội", "Xã Phước Vĩnh An", "Xã Thái Mỹ",
        "Xã Tân Thạnh Tây", "Xã Hòa Phú", "Xã Tân Thạnh Đông",
        "Xã Bình Mỹ", "Xã Tân Phú Trung", "Xã Tân Thông Hội"
    ]
}

def preprocess_input(data, encoder, numeric_columns, categorical_columns):
    for col in categorical_columns:
        valid_categories = encoder.categories_[categorical_columns.index(col)]
        # Sửa lambda function để tránh lỗi capture variable
        def validate_category(x, valid_cats=valid_categories):
            return x if x in valid_cats else None
        data[col] = data[col].apply(validate_category)

    if data[categorical_columns].isnull().any().any():
        raise ValueError("Dữ liệu nhập không hợp lệ. Hãy kiểm tra lại các giá trị trong các cột phân loại.")

    encoded_features = pd.DataFrame(encoder.transform(data[categorical_columns]))
    encoded_features.columns = encoder.get_feature_names_out(categorical_columns)

    features = pd.concat([data[numeric_columns], encoded_features], axis=1)
    return features


st.set_page_config(page_title="Dự đoán giá nhà", page_icon="🏠", layout="centered")

st.title("Dự đoán giá nhà 🏡")
st.markdown("""
    Hãy nhập thông tin chi tiết về căn nhà của bạn để dự đoán giá trị của nó.
    Mô hình sử dụng dữ liệu lịch sử để đưa ra dự đoán chính xác.
    """, unsafe_allow_html=True)

if "selected_district" not in st.session_state:
    st.session_state.selected_district = None
if "selected_ward" not in st.session_state:
    st.session_state.selected_ward = None

districts = encoder.categories_[categorical_columns.index("Quận")]
st.session_state.selected_district = st.selectbox(
    "Quận", districts, key="district", help="Chọn quận của căn nhà."
)

wards = district_to_wards.get(st.session_state.selected_district, [])
st.session_state.selected_ward = st.selectbox(
    "Phường", wards, key="ward", help="Chọn phường của căn nhà."
)

with st.form("predict_form"):
    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Diện tích (m²)", min_value=0.0, step=1.0, help="Nhập diện tích của căn nhà.")
        floors = st.number_input("Số tầng", min_value=1, step=1, help="Nhập số tầng của căn nhà.")
        bedrooms = st.number_input("Số phòng ngủ", min_value=0, step=1, help="Nhập số phòng ngủ.")
    with col2:
        bathrooms = st.number_input("Số nhà vệ sinh", min_value=0, step=1, help="Nhập số nhà vệ sinh.")
        main_direction = st.selectbox("Hướng cửa chính", encoder.categories_[0], help="Chọn hướng cửa chính.")
        house_type = st.selectbox("Loại hình nhà ở", encoder.categories_[1], help="Chọn loại hình nhà ở.")

    submit_button = st.form_submit_button("Dự đoán giá nhà")

if submit_button:
    if area <= 0 or area > 1000:
        st.error("Vui lòng nhập diện tích hợp lý.")
    elif floors <= 0 or floors > 20:
        st.error("Vui lòng nhập số tầng hợp lý.")
    elif bedrooms < 1 or bedrooms > 20:
        st.error("Vui lòng nhập số phòng ngủ hợp lý.")
    elif bathrooms < 1 or bathrooms > 20:
        st.error("Vui lòng nhập số nhà vệ sinh hợp lý.")
    elif not st.session_state.selected_district:
        st.error("Vui lòng chọn quận.")
    elif not st.session_state.selected_ward:
        st.error("Vui lòng chọn phường.")
    else:
        new_data = pd.DataFrame({
            "Diện tích": [area],
            "Số tầng": [floors],
            "Số phòng ngủ": [bedrooms],
            "Số nhà vệ sinh": [bathrooms],
            "Hướng cửa chính": [main_direction],
            "Loại hình nhà ở": [house_type],
            "Tên phường": [st.session_state.selected_ward],
            "Quận": [st.session_state.selected_district]
        })

        try:
            X_new = preprocess_input(new_data, encoder, numeric_columns, categorical_columns)
            predicted_price = model.predict(X_new)
            st.success(f"Giá nhà dự đoán: {predicted_price[0]:,.0f} VNĐ", icon="✅")
        except ValueError as e:
            if "Dữ liệu nhập không hợp lệ" in str(e):
                st.error("Xin lỗi, chúng tôi không đủ dữ liệu để dự đoán giá nhà ở khu vực này.", icon="❌")
            else:
                st.error(f"Lỗi: {e}", icon="❌")

st.markdown("""
    ---
    <small>Ứng dụng dự đoán giá nhà được phát triển bởi nhóm DYNASQUAD NGÀY 29/05/2025 ĐÃ ROLLBACK.</small>
    """, unsafe_allow_html=True)
