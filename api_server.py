from flask import Flask, request, Response
import pandas as pd
import json

df = pd.read_csv("데이터전처리_행정동명매칭only.csv", encoding="utf-8")

app = Flask(__name__)

@app.route("/api/od", methods=["GET"])
def get_od():
    home = request.args.get("Home", "").strip()
    work = request.args.get("Work", "").strip()
    if not home or not work:
        return Response(json.dumps({"error": "missing parameter"}, ensure_ascii=False), mimetype="application/json")
    row = df[(df['O행정동명'] == home) & (df['D행정동명'] == work)]
    if row.empty:
        return Response(json.dumps({"error": "not found"}, ensure_ascii=False), mimetype="application/json")
    result = row.iloc[0]
    return Response(
    json.dumps({
        "home": str(result["O행정동명"]),
        "work": str(result["D행정동명"]),
        "time_pt": int(result["time_pt"]),   # int()로 감싸기
        "time_car": int(result["time_car"])  # int()로 감싸기
    }, ensure_ascii=False),
    mimetype="application/json"
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
