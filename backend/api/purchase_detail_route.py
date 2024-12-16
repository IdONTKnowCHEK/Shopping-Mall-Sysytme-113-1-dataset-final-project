from flask import Blueprint, jsonify, request, make_response, json
from models.models import db
from sqlalchemy import text

purchase_detail_bp = Blueprint('purchase_detail', __name__)

@purchase_detail_bp.route('/shop/purchase-details', methods=['GET'])
def get_purchase_details():
    """
    獲取指定店鋪的進貨明細
    ---
    tags:
      - Purchase Details API
    parameters:
      - name: shop_name
        in: query
        type: string
        required: true
        description: 店鋪名稱
    responses:
      200:
        description: 返回進貨明細列表
        examples:
          application/json:
            [
              {
                "serial_number": "1",
                "supplier": "義隆供應商",
                "time": "2023-03-01 12:35:09",
                "goods": "花漾戀愛修容組 GLOW FLEUR CHEEKS",
                "amount": 50
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json: {"error": "Shop name is required"}
    """
    try:
        shop_name = request.args.get('shop_name')
        if not shop_name:
            return jsonify({"error": "Shop name is required"}), 400

        query = text("""
            SELECT Serial_Number, Supplier, Time, Goods, Amount
            FROM Purchase_Detail
            WHERE Store_Name = :shop_name;
        """)
        results = db.session.execute(query, {"shop_name": shop_name}).fetchall()

        purchase_details = []
        for row in results:
            purchase_details.append({
                "serial_number": row[0],
                "supplier": row[1],
                "time": str(row[2]),
                "goods": row[3],
                "amount": row[4]
            })

        json_str = json.dumps(purchase_details, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@purchase_detail_bp.route('/purchase-details-by-date', methods=['GET'])
def get_purchase_details_by_date():
    """
    查詢特定日期的進貨明細
    ---
    tags:
      - Purchase Details API
    parameters:
      - name: date
        in: query
        type: string
        required: true
    responses:
      200:
        description: 返回特定日期的進貨明細
        examples:
          application/json:
            [
              {
                "serial_number": "1",
                "store_name": "商店1",
                "supplier": "供應商A",
                "time": "2023-12-15 10:30:00",
                "goods": "商品A",
                "amount": 50
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Date is required"}
      404:
        description: 找不到進貨明細
        examples:
          application/json:
            {"error": "No purchase details found for date: 2023-12-15"}
    """
    try:
        input_date = request.args.get('date')
        if not input_date:
            return jsonify({"error": "Date is required"}), 400
        
        # 將 date 字串轉為當天的起止時間 (00:00:00 ~ 23:59:59)
        date_start = f"{input_date} 00:00:00"
        date_end = f"{input_date} 23:59:59"

        query = text("""
            SELECT Serial_Number, Store_Name, Supplier, Time, Goods, Amount
            FROM Purchase_Detail
            WHERE Time >= :date_start
              AND Time <= :date_end;
        """)
        results = db.session.execute(query, {"date_start": date_start, "date_end": date_end}).fetchall()

        if not results:
            return jsonify({"error": f"No purchase details found for date: {input_date}"}), 404

        purchase_details = []
        for row in results:
            purchase_details.append({
                "serial_number": row[0],
                "store_name": row[1],
                "supplier": row[2],
                "time": str(row[3]),
                "goods": row[4],
                "amount": row[5]
            })

        json_str = json.dumps(purchase_details, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500