"use client"
import { useState } from "react";
import Head from "next/head";

export default function IPChecker() {
  const [ipsInput, setIpsInput] = useState("");
  const [location, setLocation] = useState("raqaa"); // raqaa أو kobani
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCheck = async () => {
    const ipList = ipsInput
      .split(" ")
      .map((ip) => ip.trim())
      .filter((ip) => ip.length > 0);

    if (ipList.length === 0) {
      setError("يرجى إدخال عنوان IP واحد على الأقل.");
      return;
    }

    setLoading(true);
    setResults([]);
    setError("");

    try {
      const res = await fetch(`http://localhost:4000/check-${location}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ips: ipList }),
      });

      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        const disconnected = (data.results || []).filter((item) => !item.alive);
        setResults(disconnected);
      }
    } catch (err) {
      setError("حدث خطأ أثناء الاتصال بالخادم.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>فحص IP حسب الموقع</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="container py-5" dir="rtl">
        <h2 className="mb-4 text-center">فحص اتصال عناوين IP</h2>

        <div className="mb-3">
          <label className="form-label">اختر الموقع:</label>
          <select
            className="form-select"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          >
            <option value="raqaa">الرقة</option>
            <option value="kobani">كوباني</option>
          </select>
        </div>

        <div className="mb-3">
          <label htmlFor="ipsInput" className="form-label">
            أدخل عناوين IP مفصولة بمسافة
          </label>
          <textarea
            id="ipsInput"
            className="form-control"
            rows="3"
            value={ipsInput}
            onChange={(e) => setIpsInput(e.target.value)}
            placeholder="مثال: 192.168.1.1 192.168.1.2 10.0.0.1"
          ></textarea>
        </div>

        <button
          onClick={handleCheck}
          className="btn btn-primary"
          disabled={loading}
        >
          {loading ? "جارٍ الفحص..." : "ابدأ الفحص"}
        </button>

        {error && (
          <div className="alert alert-danger mt-3" role="alert">
            {error}
          </div>
        )}

        {!loading && results.length === 0 && ipsInput.trim() && !error && (
          <div className="alert alert-success mt-3">
            كل العناوين متصلة ✅
          </div>
        )}

        {results.length > 0 && (
          <div className="mt-4">
            <h5>العناوين غير المتصلة:</h5>
            <ul className="list-group">
              {results.map(({ ip }) => (
                <li key={ip} className="list-group-item list-group-item-danger">
                  🔴 غير متصل - {ip}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </>
  );
  }
