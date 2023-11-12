import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Script from 'next/script'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SafeWalk',
  description: 'Safest walk home every time',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
      <script src='https://unpkg.com/maplibre-gl@latest/dist/maplibre-gl.js'></script>
      <link href='https://unpkg.com/maplibre-gl@latest/dist/maplibre-gl.css' rel='stylesheet' />
     </head>
      <body className={inter.className}>{children}</body>
    </html>
  )
}
