import Link from "next/link";

export default function Home() {
  return (
    <div className="card">
      <h2>Client Accounting Portal (MVP)</h2>
      <p className="small">
        This is a simple accounting-focused portal: expenses + receipts, income, invoices with partial payments, exports.
      </p>
      <hr />
      <Link href="/login"><button className="primary">Go to Login</button></Link>
    </div>
  );
}
