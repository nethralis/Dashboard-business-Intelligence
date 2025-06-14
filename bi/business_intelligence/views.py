from django.shortcuts import render
import pandas as pd
import json

def dashboard_view(request):
    base_path = '/root/airflow/dags/BUIN_data/'

    data = {
        'report': pd.read_csv(base_path + 'transaction_report.csv').to_dict(orient='records'),
        'status': pd.read_csv(base_path + 'transaction_status.csv').to_dict(orient='records'),
        'period': pd.read_csv(base_path + 'transaction_period.csv').to_dict(orient='records'),
        'fraud': pd.read_csv(base_path + 'fraud_check.csv').to_dict(orient='records'),
    }

    return render(request, 'business_intelligence/dashboard.html', {
        'report': json.dumps(data['report']),
        'status': json.dumps(data['status']),
        'period': json.dumps(data['period']),
        'fraud': json.dumps(data['fraud']),
    })