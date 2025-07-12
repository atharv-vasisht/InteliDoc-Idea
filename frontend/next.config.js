/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['localhost'],
  },
  // Ensure proper handling for Netlify deployment
  experimental: {
    // Enable App Router features
    appDir: true,
  },
}

module.exports = nextConfig 