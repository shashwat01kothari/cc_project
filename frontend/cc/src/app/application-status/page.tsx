'use client';

import { useState } from 'react';

type StudentInfo = {
  studentName: string;
  age: string;
  gender: string;
  competitiveExam: string;
  documentVerificationStatus: string;
  pendingStatus?: string;
};

export default function Page() {
  const [appNumber, setAppNumber] = useState('');
  const [studentData, setStudentData] = useState<StudentInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleClick = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/getData?appNumber=${encodeURIComponent(appNumber)}`);
      if (!res.ok) {
        setError('Application not found or error occurred');
        setStudentData(null);
        return;
      }

      const data = await res.json();

      const {
        studentName,
        age,
        gender,
        competitiveExam,
        status: documentVerificationStatus,
        pendingStatus,
      } = data;

      setStudentData({
        studentName,
        age,
        gender,
        competitiveExam,
        documentVerificationStatus,
        pendingStatus,
      });
      setError(null);
    } catch (err) {
      setError('Error fetching data');
      setStudentData(null);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      {/* Application Input Section */}
      <div className="mb-6 border p-4 rounded shadow bg-white">
        <div className="flex items-center space-x-2 mb-2">
          <label htmlFor="appNumber" className="font-medium">Application Number:</label>
          <input
            id="appNumber"
            type="text"
            value={appNumber}
            onChange={(e) => setAppNumber(e.target.value)}
            className="border p-1 rounded w-full"
          />
        </div>

        <button
          onClick={handleClick}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Submit
        </button>
      </div>

      {/* Error Message */}
      {error && <p className="text-red-600 mt-4">{error}</p>}

      {/* Application Status Section */}
      {studentData && (
        <div className="mt-4 bg-gray-100 p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Application Status</h2>
          <p><strong>Name:</strong> {studentData.studentName}</p>
          <p><strong>Age:</strong> {studentData.age}</p>
          <p><strong>Gender:</strong> {studentData.gender}</p>
          <p><strong>Competitive Exam:</strong> {studentData.competitiveExam}</p>
          <p><strong>Document Verification Status:</strong> {studentData.documentVerificationStatus}</p>

          {studentData.documentVerificationStatus.toLowerCase() === 'verified' && (
            <p><strong>Pending Status:</strong> {studentData.pendingStatus || 'N/A'}</p>
          )}
        </div>
      )}
    </div>
  );
}
