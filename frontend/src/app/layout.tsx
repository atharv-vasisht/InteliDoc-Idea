import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'InteliDoc - AI Requirements & Obligations Intelligence Platform',
  description: 'Turn unstructured documents into structured, actionable requirements or obligations, automatically mapped to your internal processes, policies, or backlog.',
  keywords: 'AI, requirements, obligations, compliance, document processing, automation',
  authors: [{ name: 'InteliDoc Team' }],
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <header className="w-full bg-primary-700 text-white py-4 shadow-md">
          <div className="max-w-7xl mx-auto px-4 flex items-center justify-between">
            <h1 className="text-3xl font-bold tracking-tight">InteliDoc</h1>
            {/* Future: Chat button or chat widget can go here */}
          </div>
        </header>
        <div className="min-h-screen bg-gray-50">
          {children}
        </div>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#10B981',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#EF4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </body>
    </html>
  )
} 