import Head from "next/head";
import Link from "next/link";

export default function Home() {
  return (
    <>
      <Head>
        <title>مرحباً بك</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        />
      </Head>

      <style jsx>{`
        .fade-in {
          animation: fadeIn 1s ease-in forwards;
        }

        .scale-in {
          animation: scaleIn 1s ease-out forwards;
        }

        .pulse-on-hover:hover {
          animation: pulse 0.6s infinite;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes scaleIn {
          0% {
            transform: scale(0.7);
            opacity: 0;
          }
          100% {
            transform: scale(1);
            opacity: 1;
          }
        }

        @keyframes pulse {
          0% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
          100% {
            transform: scale(1);
          }
        }
      `}</style>

      <div
        className="min-vh-100 d-flex flex-column justify-content-center align-items-center text-center"
        style={{
          background: "linear-gradient(to right, #d4fc79, #96e6a1)",
          padding: "2rem",
        }}
        dir="rtl"
      >
        <div className="bg-white shadow-lg rounded-4 p-5 fade-in" style={{ maxWidth: "500px", width: "100%" }}>
          <div className="mb-3 scale-in">
            <img
              src="https://cdn-icons-png.flaticon.com/512/3208/3208707.png"
              alt="Network Icon"
              width="80"
              height="80"
            />
          </div>

          <h1 className="mb-3 text-success fw-bold">مرحباً بك في نظام فحص الشبكة</h1>
          <p className="text-muted mb-4">
            هذا النظام يتيح لك التحقق بسرعة من حالة الاتصال للأجهزة عبر الشبكة الداخلية.
          </p>

          <Link href="/ipcheck" className="btn btn-primary btn-lg pulse-on-hover">
            🚀 ابدأ الفحص الآن
          </Link>
        </div>
      </div>
    </>
  );
            }
