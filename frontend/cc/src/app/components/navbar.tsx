'use client'

import Link from 'next/link'
import { useState } from 'react'
import { Menu, X } from 'lucide-react' // or Heroicons if preferred

export default function Navbar() {
  const [open, setOpen] = useState(false)

  return (
    <nav className="bg-white shadow-md fixed w-full top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        {/* Link for 'Admissions portal' */}
        <Link href="/" className="text-xl font-bold text-blue-600">
          Admissions portal
        </Link>

        <div className="md:hidden">
          <button onClick={() => setOpen(!open)}>
            {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        <ul className="hidden md:flex space-x-6">
          {/* Updated Links for Student portal, Application status, and Admin dashboard */}
          <li><Link href="/student-portal" className="hover:text-blue-500">Student portal</Link></li>
          <li><Link href="/application-status" className="hover:text-blue-500">Application status</Link></li>
          <li><Link href="/admin-dashboard" className="hover:text-blue-500">Admin dashboard</Link></li>
        </ul>
      </div>

      {/* Mobile Menu */}
      {open && (
        <ul className="md:hidden px-4 pb-4 space-y-2 bg-white">
          <li><Link href="/" onClick={() => setOpen(false)}>Home</Link></li>
          <li><Link href="/student-portal" onClick={() => setOpen(false)}>Student portal</Link></li>
          <li><Link href="/application-status" onClick={() => setOpen(false)}>Application status</Link></li>
          <li><Link href="/admin-dashboard" onClick={() => setOpen(false)}>Admin dashboard</Link></li>
        </ul>
      )}
    </nav>
  )
}
