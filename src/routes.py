from flask import Blueprint, render_template, jsonify, request
import sys
import platform
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Render the dashboard UI."""
    return render_template('index.html')

@bp.route('/api/health')
def health():
    """Return application health statistics."""
    return jsonify({
        'status': 'healthy',
        'database': 'connected_mock',
        'environment': 'development',
        'uptime': '99.99%',
        'cpu_load': '12.4%',
        'memory_usage': '48.2 MB'
    })

@bp.route('/api/info')
def info():
    """Return application metadata and runtime info."""
    return jsonify({
        'app_name': 'AeroDash Flask Core',
        'version': '1.0.0',
        'python_version': sys.version,
        'platform': platform.platform(),
        'port': 19191,
        'features': [
            'Modular Architecture',
            'Sleek Glassmorphism Dashboard',
            'Full Automated Testing Suite',
            'Health Check API Monitoring',
            'Stock Market Watchlist',
            'Afternoon Duty Scheduler'
        ]
    })

@bp.route('/api/stocks')
def stocks():
    """Return watchlist stock market quotes."""
    return jsonify([
        {
            'symbol': '2330.TW',
            'name': '台積電',
            'price': 875.0,
            'change': 15.0,
            'change_percent': '+1.74%',
            'direction': 'up',
            'volume': '24,198'
        },
        {
            'symbol': 'NVDA',
            'name': '輝達 (NVIDIA)',
            'price': 950.00,
            'change': 28.50,
            'change_percent': '+3.10%',
            'direction': 'up',
            'volume': '41,082,190'
        },
        {
            'symbol': 'AAPL',
            'name': '蘋果 (Apple)',
            'price': 190.20,
            'change': -1.80,
            'change_percent': '-0.94%',
            'direction': 'down',
            'volume': '52,891,040'
        },
        {
            'symbol': '2454.TW',
            'name': '聯發科',
            'price': 1210.0,
            'change': 20.0,
            'change_percent': '+1.68%',
            'direction': 'up',
            'volume': '3,892'
        }
    ])

@bp.route('/api/schedule')
def schedule():
    """Return afternoon work timetable and company info."""
    return jsonify({
        'company': '緯創資通股份有限公司 (Wistron Corp.)',
        'time_window': '下午 13:30 - 18:00',
        'department': '雲端架構研發部',
        'location': '新北市汐止區新台五路一段180號 (汐止研發總部)',
        'task_title': 'AWS 雲端架構部署與微服務監控',
        'status': 'on_duty',
        'timeline': [
            {
                'id': 1,
                'time': '13:30 - 14:00',
                'task': '研發部門同步與工作指派會議 (Team Sync)',
                'status': 'completed'
            },
            {
                'id': 2,
                'time': '14:00 - 15:30',
                'task': '設定 AWS ECS 容器服務與 Auto Scaling 策略',
                'status': 'in_progress'
            },
            {
                'id': 3,
                'time': '15:30 - 17:00',
                'task': '優化 Flask 服務連接埠 19191 內部負載均衡與緩存',
                'status': 'pending'
            },
            {
                'id': 4,
                'time': '17:00 - 18:00',
                'task': '撰寫部署維護日誌與團隊交接',
                'status': 'pending'
            }
        ]
    })

@bp.route('/feature3', methods=['GET', 'POST'])
def feature3():
    """Handle Feature 3 file upload to S3 without hardcoded credentials."""
    bucket_name = os.environ.get('S3_BUCKET_NAME', 'ckc101-18')
    region_name = os.environ.get('AWS_DEFAULT_REGION', 'ap-east-2')
    
    if request.method == 'POST':
        # Check if file part exists
        if 'file' not in request.files:
            error_msg = '檔案欄位缺失！'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({'success': False, 'error': error_msg}), 400
            return render_template('feature3.html', error=error_msg, bucket_name=bucket_name, region_name=region_name)
            
        file = request.files['file']
        
        # Check if user selected no file
        if file.filename == '':
            error_msg = '尚未選擇任何檔案！'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({'success': False, 'error': error_msg}), 400
            return render_template('feature3.html', error=error_msg, bucket_name=bucket_name, region_name=region_name)
            
        try:
            # Initialize S3 client without credentials (automatically resolves EC2 IAM Role credentials)
            s3_client = boto3.client('s3', region_name=region_name)
            
            # Direct in-memory stream upload (prevents disk space pollution on host machine)
            s3_client.upload_fileobj(
                file,
                bucket_name,
                file.filename,
                ExtraArgs={
                    'ContentType': file.content_type
                }
            )
            
            # S3 public URL format for ap-east-2 region
            file_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{file.filename}"
            success_msg = f"檔案 '{file.filename}' 已成功安全上傳至 S3！"
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({
                    'success': True,
                    'message': success_msg,
                    'filename': file.filename,
                    'file_url': file_url
                })
                
            return render_template('feature3.html', success=success_msg, file_url=file_url, filename=file.filename, bucket_name=bucket_name, region_name=region_name)
            
        except (NoCredentialsError, PartialCredentialsError) as e:
            error_msg = 'AWS 憑證解析失敗！請確認 EC2 Instance Profile 或 IAM 角色配置正確。'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({'success': False, 'error': error_msg, 'details': str(e)}), 403
            return render_template('feature3.html', error=error_msg, bucket_name=bucket_name, region_name=region_name)
        except ClientError as e:
            error_msg = f"AWS S3 服務錯誤：{e.response['Error']['Message']}"
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({'success': False, 'error': error_msg, 'details': str(e)}), 500
            return render_template('feature3.html', error=error_msg, bucket_name=bucket_name, region_name=region_name)
        except Exception as e:
            error_msg = f"上傳錯誤：{str(e)}"
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({'success': False, 'error': error_msg}), 500
            return render_template('feature3.html', error=error_msg, bucket_name=bucket_name, region_name=region_name)
            
    return render_template('feature3.html', bucket_name=bucket_name, region_name=region_name)


