import "./globals.css";
import { Navbar } from "@/components/Navbar";

export const metadata = { title: "Client Accounting Portal" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
