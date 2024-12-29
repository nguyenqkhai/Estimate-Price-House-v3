# Estimate-Price-House-v3
Bài tập cuối kỳ môn AI - Dự đoán giá nhà tại khu vực Tp.HCM

Thực hiện: 
  - cralw data từ nhatot.com
    + Các dữ liệu bao gồm: Tên đường,Tên phường,Quận,Giấy tờ pháp lý,Diện tích,Số tầng,Số phòng ngủ,Số nhà vệ sinh,Hướng cửa chính,Loại hình nhà ở,Giá (VNĐ),Giá hiển thị,Giá/m² (VNĐ)
    + Số lượng dữ liệu lấy được: 20000 dòng tương đương 20000 tin ráo bán trên nhatot.com
  - Làm sạch dữ liệu:
    + Bỏ các dòng không hợp lệ
    + Các dòng không có số tầng đặt = 1
    + Cột 'Giấy tờ pháp lý':
      . 1: Đã có sổ
      . khác 1: Chưa có sổ
  - Chia tập dữ liệu vừa làm sạch thành 2 tập:
    + Tập train: 80%
    + Tập test: 20%
  - Thực hiện train với thuật toán xgboost
  - Đánh giá mô hình
    ![image](https://github.com/user-attachments/assets/419e2cf2-ddb2-4e3c-8a47-000c2b373c7d)
Link colab: https://colab.research.google.com/drive/12BuYHNFAIeoHqiWSOwr1ei8n3Q2M0jAe?usp=sharing

  - Viết giao diện bằng thư viện streamlit để tương tác với model
  - Dùng eamlit community cloud để deploy
    
Link dùng thử: https://estimate-price-house-v3-flameo.streamlit.app/
