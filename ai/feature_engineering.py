import pandas as pd

def create_features(df: pd.DataFrame):
    # Một số dữ liệu có giá trị giây = 60 (invalid). Dùng errors='coerce'
    # để chuyển các giá trị lỗi thành NaT, tránh crash khi train.
    dt_series = pd.to_datetime(df['fulldatewithtime'], format='mixed', errors='coerce')

    df['hour'] = dt_series.dt.hour
    df['day_of_week'] = dt_series.dt.dayofweek  # Thứ trong tuần (0: Thứ 2, 6: Chủ Nhật)
    df['is_weekend'] = dt_series.dt.dayofweek.isin([5, 6]).astype(int)  # Có phải cuối tuần không

    df['is_night'] = df['hour'].apply(
        lambda x: 1 if x >= 3 or x <= 5 else 0
    )

    df['large_transaction'] = (
        df['amount'] > 10000000
    ).astype(int)

    features = df[
        [   'amount',
            'balance',
            'hour',
            'is_night',
            'large_transaction'
        ]
    ]
    return features