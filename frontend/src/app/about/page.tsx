export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto py-20 px-4">
      <h1 className="text-5xl font-extrabold mb-6 text-primary-700">About InteliDoc</h1>
      <p className="text-xl text-gray-700 mb-8">
        InteliDoc is your ultimate AI-powered assistant for PMO, Product, Program, and GRC teams. Our mission is to transform document chaos into clarity—automatically organizing, summarizing, and governing your files, folders, and knowledge.
      </p>
      <div className="bg-white rounded-2xl shadow-lg p-8 border-t-4 border-primary-200">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">Our Vision</h2>
        <ul className="space-y-4 text-lg text-gray-700">
          <li>• Effortless, AI-driven document and knowledge management</li>
          <li>• Instant summaries, compliance checks, and actionable insights</li>
          <li>• Natural language chat for file organization and project intelligence</li>
          <li>• A beautiful, modern experience for every team</li>
        </ul>
      </div>
      <div className="mt-12 text-gray-500 text-center text-sm">
        &copy; {new Date().getFullYear()} InteliDoc. All rights reserved.
      </div>
    </div>
  )
} 