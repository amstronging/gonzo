import streamlit as st
import pandas as pd
import urllib.request

st.title("강아지 사료 선택 서비스")
st.header("강아지 정보 입력")


age = st.number_input("강아지 나이 (개월수)", min_value=1, max_value=240, value=12, step=1)
weight = st.number_input("강아지 체중 (kg)", min_value=0.1, max_value=100.0, value=10.0)
activity_level = st.selectbox("활동량을 선택하세요", ["활동이 적음", "적당히 활동적", "매우 활동적"])
breeds = [
    '포메라니안', '푸들', '시추', '비숑 프리제', '골든 리트리버', '래브라도 리트리버', 
    '요크셔 테리어', '불독', '말티즈', '닥스훈트', '치와와', '사모예드', '저먼 셰퍼드', 
    '보더 콜리', '허스키', '비글', '코카 스파니엘', '로트와일러', '도베르만', '차우차우',
    '그레이하운드', '아키타', '웰시코기', '셰틀랜드 쉽독', '샤페이', '달마시안', '오스트레일리안 셰퍼드'
]
breed = st.selectbox("강아지 품종을 선택하세요", breeds)
diseases = [
    '없음', '비만', '관절염', '알레르기', '당뇨', '심장병', '신장병', '간 질환', '소화기 문제',
    '피부 문제', '구강 문제', '암', '눈 질환', '간질', '췌장염', '고혈압', '호흡기 질환', '간질환',
    '소화불량', '간경화', '백내장', '방광염', '갑상선 문제', '빈혈', '신부전', '고지혈증', '탈모',
    '파보바이러스', '홍역', '피부 알레르기', '슬개골 탈구', '고관절 이형성증', '유방암', '자궁축농증',
    '이뇨 문제', '심부전', '치주질환', '전립선 비대증', '간암', '대장염', '장폐색', '심장 비대증',
    '요로 결석', '뇌출혈', '간부전', '고관절 문제'
]
disease_category_mapping = {
    '비만': '종합','관절염': '뼈/관절','알레르기': '피부/모질','당뇨': '종합',
    '심장병': '심장/간','신장병': '신장/요로','간 질환': '심장/간','소화기 문제': '장/유산균',
    '피부 문제': '피부/모질','구강 문제': '치아/구강','암': '면역/항산화','눈 질환': '눈/눈물',
    '간질': '진정/스트레스','췌장염': '종합','고혈압': '심장/간','호흡기 질환': '종합',
    '소화불량': '장/유산균','간경화': '심장/간','백내장': '눈/눈물','방광염': '신장/요로','갑상선 문제': '종합',
    '빈혈': '종합','신부전': '신장/요로','고지혈증': '종합', '탈모': '피부/모질','파보바이러스': '면역/항산화',
    '홍역': '면역/항산화','피부 알레르기': '피부/모질','슬개골 탈구': '뼈/관절','고관절 이형성증': '뼈/관절',
    '유방암': '면역/항산화','자궁축농증': '면역/항산화','이뇨 문제': '신장/요로','심부전': '심장/간','치주질환': '치아/구강','전립선 비대증': '종합','간암': '심장/간',
    '대장염': '장/유산균','장폐색': '장/유산균','심장 비대증': '심장/간','요로 결석': '신장/요로','뇌출혈': '진정/스트레스','간부전': '심장/간',
    '고관절 문제': '뼈/관절'
}
selected_diseases = st.multiselect("강아지가 앓고 있는 질병을 선택하세요 (여러 개 선택 가능)", diseases)

url = 'https://raw.githubusercontent.com/amstronging/gonzo/main/nutrition.xlsx'
# 파일 읽기
df_nut = pd.read_excel(url)


url2 = 'https://raw.githubusercontent.com/amstronging/gonzo/main/dog_food.xlsx'

df_food = pd.read_excel(url2)

# 공백 제거 및 데이터 정리
df_food.columns = df_food.columns.str.strip()

# 브랜드 리스트 생성 및 공백 제거
df_food['브랜드'] = df_food['사료'].apply(lambda x: x.split(' ')[0])  # 브랜드 추출
df_food['제품명'] = df_food['사료'].apply(lambda x: ' '.join(x.split(' ')[1:]))  # 브랜드 제외한 이름 추출
brands = df_food['브랜드'].unique().tolist()

# 브랜드 선택
selected_brand = st.selectbox("사료의 브랜드를 선택하세요", brands)

# 선택된 브랜드의 제품 필터링
filtered_products = df_food[df_food['브랜드'] == selected_brand]
products = filtered_products['제품명'].tolist()  # 제품명만 리스트로 생성

# 제품 선택
selected_product = st.selectbox("사료 제품을 선택하세요", products)

# 선택된 제품의 데이터 추출
selected_food_data = filtered_products[filtered_products['제품명'] == selected_product].iloc[0]



if age < 12:
    age_group = "성장기 강아지"
elif 12 <= age < 84:
    age_group = "성견"
else:
    age_group = "노령견"

activity_coefficients = {
    "성장기 강아지": {"활동이 적음": 2.0, "적당히 활동적": 2.5, "매우 활동적": 3.0},
    "성견": {"활동이 적음": 1.6, "적당히 활동적": 1.8, "매우 활동적": 2.0},
    "노령견": {"활동이 적음": 1.2, "적당히 활동적": 1.4, "매우 활동적": 1.6},
}

BMR = 70 * (weight ** 0.75)

activity_factor = activity_coefficients[age_group][activity_level]
DER = BMR * activity_factor

protein = selected_food_data['조단백']
fat = selected_food_data['조지방']
fiber = selected_food_data['조섬유']
ash = selected_food_data['조회분']
omega6 = selected_food_data['오메가6']
calcium = selected_food_data['칼슘']
omega3 = selected_food_data['오메가 3']
phosphorus = selected_food_data['인']
moisture = selected_food_data['수분']

carbohydrate = 100 - (protein + fat + fiber + ash + omega6 + calcium + omega3 + phosphorus + moisture)

ME = (3.5 * protein) + (8.5 * fat) + (3.5 * carbohydrate)

daily_food_amount = (DER / ME) * 100

meal_amount = daily_food_amount / 3

protein_min_kcal = DER * 0.18
protein_max_kcal = DER * 0.25

fat_min_kcal = DER * 0.35
fat_max_kcal = DER * 0.50

protein_kcal_per_g = 3.5
fat_kcal_per_g = 8.5

protein_min_g = protein_min_kcal / protein_kcal_per_g
protein_max_g = protein_max_kcal / protein_kcal_per_g

fat_min_g = fat_min_kcal / fat_kcal_per_g
fat_max_g = fat_max_kcal / fat_kcal_per_g

daily_protein_provided = daily_food_amount * (protein / 100)
daily_fat_provided = daily_food_amount * (fat / 100)



st.write(f"한 끼 급여량 (하루 3끼 기준): {meal_amount:.2f} g")

if daily_protein_provided < protein_min_g:
    protein_status = "부족"
elif daily_protein_provided > protein_max_g:
    protein_status = "초과"
else:
    protein_status = "충족"

if daily_fat_provided < fat_min_g:
    fat_status = "부족"
elif daily_fat_provided > fat_max_g:
    fat_status = "초과"
else:
    fat_status = "충족"

if selected_diseases:
    # 선택한 질병에 해당하는 카테고리를 필터링
    relevant_categories = [disease_category_mapping[disease] for disease in selected_diseases if disease in disease_category_mapping]
    filtered_df = df_nut[df_nut['카테고리'].isin(relevant_categories)]

    if filtered_df.empty:
        st.write("선택한 질병에 해당하는 영양제를 찾을 수 없습니다.")
    else:
        # 공백 제거
        filtered_df.columns = filtered_df.columns.str.strip()

        # 단백질과 지방 부족 정도 계산
        protein_deficit = protein_min_g - daily_protein_provided
        fat_deficit = fat_min_g - daily_fat_provided

        # 1. 부족, 부족
        if protein_status == "부족" and fat_status == "부족":
            if protein_deficit > fat_deficit:
                recommended_protein = filtered_df.sort_values(by='조단백', ascending=False).iloc[0]
                st.write(f"영양제 추천: {recommended_protein['영양제']}")
            elif fat_deficit > protein_deficit:
                recommended_fat = filtered_df.sort_values(by='조지방', ascending=False).iloc[0]
                st.write(f"영양제 추천: {recommended_fat['영양제']}")
            else:
                recommended_combined = filtered_df.sort_values(by=['조단백', '조지방'], ascending=False).iloc[0]
                st.write(f"영양제 추천: {recommended_combined['영양제']}")

        # 2. 부족, 충족
        elif protein_status == "부족" and fat_status == "충족":
            recommended_low_fat = filtered_df.sort_values(by='조지방', ascending=True).iloc[0]
            st.write(f"영양제 추천: {recommended_low_fat['영양제']}")

        # 3. 부족, 초과
        elif protein_status == "부족" and fat_status == "초과":
            recommended_low_fat = filtered_df.sort_values(by='조지방', ascending=True).iloc[0]
            st.write(f"영양제 추천: {recommended_low_fat['영양제']}")

        # 4. 충족, 부족
        elif protein_status == "충족" and fat_status == "부족":
            recommended_low_protein = filtered_df.sort_values(by='조단백', ascending=True).iloc[0]
            st.write(f"영양제 추천: {recommended_low_protein['영양제']}")

        # 5. 충족, 충족
        elif protein_status == "충족" and fat_status == "충족":
            recommended_least = filtered_df.sort_values(by=['조단백', '조지방'], ascending=True).iloc[0]
            st.write(f"영양제 추천: {recommended_least['영양제']}")

        # 6. 충족, 초과
        elif protein_status == "충족" and fat_status == "초과":
            recommended_least = filtered_df.sort_values(by=['조단백'], ascending=True).iloc[0]
            st.write(f"영양제 추천: {recommended_least['영양제']}")

        # 7. 초과, 부족
        elif protein_status == "초과" and fat_status == "부족":
            recommended_low_protein = filtered_df.sort_values(by='조단백', ascending=True).iloc[0]
            st.write(f"영양제 추천: {recommended_low_protein['영양제']}")

        # 8. 초과, 충족
        elif protein_status == "초과" and fat_status == "충족":
            recommended_least = filtered_df.sort_values(by=['조지방'], ascending=True).iloc[0]
            st.write(f"영양제 추천: {recommended_least['영양제']}")

        # 9. 초과, 초과
        elif protein_status == "초과" and fat_status == "초과":
            recommended_zero = filtered_df.loc[(filtered_df['조단백'] == 0) & (filtered_df['조지방'] == 0)]
            if recommended_zero.empty:
                recommended_closest = filtered_df.sort_values(by=['조단백', '조지방'], ascending=True).iloc[0]
                st.write(f"영양제 추천: {recommended_closest['영양제']}")
            else:
                recommended_zero = recommended_zero.iloc[0]
                st.write(f"영양제 추천: {recommended_zero['영양제']}")
