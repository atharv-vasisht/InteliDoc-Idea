import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'
import Link from 'next/link'

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
      <body className={inter.className + ' bg-gradient-to-br from-gray-50 to-blue-50 min-h-screen'}>
        <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-lg shadow-lg border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-primary-700 text-2xl font-extrabold tracking-tight">InteliDoc</span>
            </div>
            <nav className="flex flex-wrap gap-2 sm:gap-4">
              <Link href="/" scroll={true} className="px-3 sm:px-5 py-2 rounded-full bg-primary-700 text-white font-semibold shadow hover:bg-primary-800 transition-all duration-150 text-sm sm:text-base">Home</Link>
              <a href="/#upload" className="px-3 sm:px-5 py-2 rounded-full bg-gray-200 text-primary-700 font-semibold shadow hover:bg-primary-100 hover:text-primary-800 transition-all duration-150 text-sm sm:text-base">Upload</a>
              <a href="/#chat" className="px-3 sm:px-5 py-2 rounded-full bg-gray-200 text-primary-700 font-semibold shadow hover:bg-primary-100 hover:text-primary-800 transition-all duration-150 text-sm sm:text-base">AI Chat</a>
              <Link href="/analytics" className="px-3 sm:px-5 py-2 rounded-full bg-gray-200 text-primary-700 font-semibold shadow hover:bg-primary-100 hover:text-primary-800 transition-all duration-150 text-sm sm:text-base">Analytics</Link>
              <Link href="/cross-platform" className="px-3 sm:px-5 py-2 rounded-full bg-gray-200 text-primary-700 font-semibold shadow hover:bg-primary-100 hover:text-primary-800 transition-all duration-150 text-sm sm:text-base">Cross-Platform</Link>
              <Link href="/about" className="px-3 sm:px-5 py-2 rounded-full bg-gray-200 text-primary-700 font-semibold shadow hover:bg-primary-100 hover:text-primary-800 transition-all duration-150 text-sm sm:text-base">About</Link>
            </nav>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="w-full bg-white/80 border-t border-gray-200 py-4 text-center text-gray-500 text-sm mt-12">
          © {new Date().getFullYear()} InteliDoc. All rights reserved.
        </footer>
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