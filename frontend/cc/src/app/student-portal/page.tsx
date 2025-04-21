'use client'

import { useState } from 'react'

export default function StudentPortal() {
  const [studentName, setStudentName] = useState('')
  const [age, setAge] = useState('')
  const [gender, setGender] = useState('male')
  const [studentPhoto, setStudentPhoto] = useState<File | null>(null)
  const [marks10, setMarks10] = useState<File | null>(null)
  const [marks12, setMarks12] = useState<File | null>(null)
  const [competitiveExam, setCompetitiveExam] = useState('')
  const [examPdf, setExamPdf] = useState<File | null>(null)
  const [selectedCourse, setSelectedCourse] = useState('')  // New state for selected course

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
    formData.append('course', selectedCourse)  // Add course to form data

    try {
      const response = await fetch('http://127.0.0.1:8000/api/studentPortal', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const result = await response.json()
        console.log('Success:', result)

        const { application_id } = result
        alert(`Application submitted successfully! Your application ID is: ${application_id}`)

        // Reset form
        setStudentName('')
        setAge('')
        setGender('male')
        setStudentPhoto(null)
        setMarks10(null)
        setMarks12(null)
        setCompetitiveExam('')
        setExamPdf(null)
        setSelectedCourse('')  // Reset course selection

      } else {
        console.error('Error:', response.statusText)
      }
    } catch (error) {
      console.error('Request failed', error)
    }
}


  const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB

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
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
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
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
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
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        {/* Select Course */}
        <div>
          <label htmlFor="courseApplied" className="block text-sm font-medium text-gray-700">
            Select Course
          </label>
          <select
            id="courseApplied"
            value={selectedCourse}
            onChange={(e) => setSelectedCourse(e.target.value)}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          >
            <option value="">Select Course</option>
            <option value="CSE">CSE</option>
            <option value="AIML">AIML</option>
            <option value="ECE">ECE</option>
            <option value="BBA">BBA</option>
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
            required
            onChange={(e) => {
              const file = e.target.files?.[0]
              if (file && file.size > MAX_FILE_SIZE) {
                alert('Student photo must be less than 10MB.')
                e.target.value = ''
              } else {
                setStudentPhoto(file || null)
              }
            }}
            className="mt-1 block w-full text-sm text-gray-500 file:py-2 file:px-4 file:border file:border-gray-300 file:rounded-md"
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
            required
            onChange={(e) => {
              const file = e.target.files?.[0]
              if (file && file.size > MAX_FILE_SIZE) {
                alert('10th Marks Sheet must be less than 10MB.')
                e.target.value = ''
              } else {
                setMarks10(file || null)
              }
            }}
            className="mt-1 block w-full text-sm text-gray-500 file:py-2 file:px-4 file:border file:border-gray-300 file:rounded-md"
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
            required
            onChange={(e) => {
              const file = e.target.files?.[0]
              if (file && file.size > MAX_FILE_SIZE) {
                alert('12th Marks Sheet must be less than 10MB.')
                e.target.value = ''
              } else {
                setMarks12(file || null)
              }
            }}
            className="mt-1 block w-full text-sm text-gray-500 file:py-2 file:px-4 file:border file:border-gray-300 file:rounded-md"
          />
        </div>

        {/* Competitive Exam */}
        <div>
          <label htmlFor="competitiveExam" className="block text-sm font-medium text-gray-700">
            Competitive Examination
          </label>
          <select
            id="competitiveExam"
            value={competitiveExam}
            onChange={(e) => setCompetitiveExam(e.target.value)}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          >
            <option value="">Select Exam</option>
            <option value="pessat">PESSAT</option>
            <option value="kcet">KCET</option>
          </select>
        </div>

        {/* Exam PDF */}
        {competitiveExam && (
          <div>
            <label htmlFor="examPdf" className="block text-sm font-medium text-gray-700">
              {competitiveExam === 'pessat' ? 'PESSAT Exam PDF' : 'KCET Exam PDF'}
            </label>
            <input
              type="file"
              id="examPdf"
              accept="application/pdf"
              required
              onChange={(e) => {
                const file = e.target.files?.[0]
                if (file && file.size > MAX_FILE_SIZE) {
                  alert(`${competitiveExam.toUpperCase()} Exam PDF must be less than 10MB.`)
                  e.target.value = ''
                } else {
                  setExamPdf(file || null)
                }
              }}
              className="mt-1 block w-full text-sm text-gray-500 file:py-2 file:px-4 file:border file:border-gray-300 file:rounded-md"
            />
          </div>
        )}

        {/* Submit */}
        <div>
          <button
            type="submit"
            className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  )
}
