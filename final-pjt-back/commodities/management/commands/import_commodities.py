from django.core.management.base import BaseCommand
from commodities.models import Commodities
import pandas as pd
import os

class Command(BaseCommand):
    help = '엑셀 파일에서 Commodities 테이블로 데이터를 불러옵니다.'

    def handle(self, *args, **kwargs):
        # 현재 파일 기준 경로 계산
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(base_dir, 'data')

        gold_path = os.path.join(data_dir, 'Gold_prices.xlsx')
        silver_path = os.path.join(data_dir, 'Silver_prices.xlsx')

        gold_df = pd.read_excel(gold_path, dtype={'Open': str})
        silver_df = pd.read_excel(silver_path, dtype={'Open': str})


        self.stdout.write(self.style.NOTICE('금 데이터 저장 중...'))
        for _, row in gold_df.iterrows():
            Commodities.objects.create(
                date=pd.to_datetime(row['Date']),
                metal_type='gold',
                close=float(str(row['Close/Last']).replace(',', '')),
                open=float(str(row['Open']).replace(',', '')),
                high=float(str(row['High']).replace(',', '')),
                low=float(str(row['Low']).replace(',', '')),
                volume=float(str(row['Volume']).replace(',', ''))
            )

        self.stdout.write(self.style.NOTICE(' 은 데이터 저장 중... (비정상 값 정제 처리)'))

        # 잘못된 값 (예: 날짜포맷) 제거
        silver_df['Open'] = pd.to_numeric(silver_df['Open'], errors='coerce')
        silver_df['High'] = pd.to_numeric(silver_df['High'], errors='coerce')
        silver_df['Low'] = pd.to_numeric(silver_df['Low'], errors='coerce')

        # 숫자로 변환 불가했던 행들을 제거 (NaN 포함 행)
        silver_df.dropna(subset=['Open', 'High', 'Low'], inplace=True)

        for _, row in silver_df.iterrows():
            try:
                Commodities.objects.create(
                    date=pd.to_datetime(row['Date']),
                    metal_type='silver',
                    close=float(str(row['Close/Last']).replace(',', '')),
                    open=float(str(row['Open']).replace(',', '')),
                    high=float(str(row['High']).replace(',', '')),
                    low=float(str(row['Low']).replace(',', '')),
                    volume=float(str(row['Volume']).replace(',', '')),
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"은 데이터 오류 (저장 안함): {e}"))

        self.stdout.write(self.style.SUCCESS('금/은 데이터가 성공적으로 삽입되었습니다.'))
