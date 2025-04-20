'use client'

import { useState } from 'react'

export default function StudentPortal() {
  const [studentName, setStudentName] = useState('')
  const [age, setAge] = useState('')
  const [gender, setGender] = useState('male')
  const [studentPhoto, setStudentPhoto] = useState(null)
  const [marks10, setMarks10] = useState(null)
  const [marks12, setMarks12] = useState(null)
  const [competitiveExam, setCompetitiveExam] = useState('')
  const [examPdf, setExamPdf] = useState(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
  
    const formData = new FormData()
    formData.append('studentName', studentName)
    formData.append('age', age)
    formData.append('gender', gender)
    if (studentPhoto) formData.append('studentPhoto', studentPhoto)
    if (marks10) formData.append('marks10', marks10)
    if (marks12) formData.append('marks12', marks12)
    formData.append('competitiveExam', competitiveExam)
    if (examPdf) formData.append('examPdf', examPdf)
  
    try {
      const response = await fetch('http://127.0.0.1:8000/api/studentPortal', {
        method: 'POST',
        body: formData,
      })
  
      if (response.ok) {
        const result = await response.json()
        console.log('Success:', result)
  
        // Reset all form fields
        setStudentName('')
        setAge('')
        setGender('male')
        setStudentPhoto(null)
        setMarks10(null)
        setMarks12(null)
        setCompetitiveExam('')
        setExamPdf(null)
  
        // Show alert
        alert('Application submitted successfully!')
      } else {
        console.error('Error:', response.statusText)
      }
    } catch (error) {
      console.error('Request failed', error)
    }
  }
  

  return (
    <div className="max-w-lg mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Student Portal</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Student Name */}
        <div>
          <label htmlFor="studentName" className="block text-sm font-medium text-gray-700">
            Student Name
          </label>
          <input
            type="text"
            id="studentName"
            value={studentName}
            onChange={(e) => setStudentName(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            required
          />
        </div>

        {/* Age */}
        <div>
          <label htmlFor="age" className="block text-sm font-medium text-gray-700">
            Age
          </label>
          <input
            type="number"
            id="age"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            required
          />
        </div>

        {/* Gender */}
        <div>
          <label htmlFor="gender" className="block text-sm font-medium text-gray-700">
            Gender
          </label>
          <select
            id="gender"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            required
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        {/* Student Photo */}
        <div>
          <label htmlFor="studentPhoto" className="block text-sm font-medium text-gray-700">
            Student Photo
          </label>
          <input
            type="file"
            id="studentPhoto"
            accept="image/*"
            onChange={(e) => setStudentPhoto(e.target.files ? e.target.files[0] : null)}
            className="mt-1 block w-full text-sm text-gray-500 file:py-2 file:px-4 file:border file:border-gray-300 file:rounded-md"
            required
          />
        </div>

        {/* 10th Marks Sheet */}
        <div>
          <label htmlFor="marks10" className="block text-sm font-medium text-gray-700">
            10th Marks Sheet (PDF)
          </label>
          <input
            type="file"
            id="marks10"
            accept="application/pdf"
            onChange={(e) => setMarks10(e.target.files ? e.target.files[0] : null)}
            className="mt-1 block w-full text-sm text-gray-500 file:py-2 file:px-4 file:border file:border-gray-300 file:rounded-md"
            required
          />
        </div>

        {/* 12th Marks Sheet */}
        <div>
          <label htmlFor="marks12" className="block text-sm font-medium text-gray-700">
            12th Marks Sheet (PDF)
          </label>
          <input
            type="file"
            id="marks12"
            accept="application/pdf"
            onChange={(e) => setMarks12(e.target.files ? e.target.files[0] : null)}
            className="mt-1 block w-full text-sm text-gray-500 file:py-2 file:px-4 file:border file:border-gray-300 file:rounded-md"
            required
          />
        </div>

        {/* Competitive Examination */}
        <div>
          <label htmlFor="competitiveExam" className="block text-sm font-medium text-gray-700">
            Competitive Examination
          </label>
          <select
            id="competitiveExam"
            value={competitiveExam}
            onChange={(e) => setCompetitiveExam(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            required
          >
            <option value="">Select Exam</option>
            <option value="pessat">PESSAT</option>
            <option value="kcet">KCET</option>
          </select>
        </div>

        {/* Competitive Exam PDF (conditional rendering) */}
        {competitiveExam && (
          <div>
            <label htmlFor="examPdf" className="block text-sm font-medium text-gray-700">
              {competitiveExam === 'pessat' ? 'PESSAT Exam PDF' : 'KCET Exam PDF'}
            </label>
            <input
              type="file"
              id="examPdf"
              accept="application/pdf"
              onChange={(e) => setExamPdf(e.target.files ? e.target.files[0] : null)}
              className="mt-1 block w-full text-sm text-gray-500 file:py-2 file:px-4 file:border file:border-gray-300 file:rounded-md"
              required
            />
          </div>
        )}

        {/* Submit Button */}
        <div>
          <button
            type="submit"
            className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  )
}
