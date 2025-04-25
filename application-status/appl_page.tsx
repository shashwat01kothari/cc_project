'use client';

import { useState } from 'react';

type StudentInfo = {
  studentName: string;
  age: string;
  gender: string;
  competitiveExam: string;
  documentVerificationStatus: string;
};

export default function Page() {
  const [appNumber, setAppNumber] = useState('');
  const [studentData, setStudentData] = useState<StudentInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [seatConfirmed, setSeatConfirmed] = useState<boolean>(false); // To track if seat is confirmed

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
      } = data;

      setStudentData({
        studentName,
        age,
        gender,
        competitiveExam,
        documentVerificationStatus,
      });
      setError(null);
    } catch (err) {
      setError('Error fetching data');
      setStudentData(null);
    }
  };

  const confirmSeat = async () => {
    if (studentData) {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/confirmSeat?appNumber=${encodeURIComponent(appNumber)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (res.ok) {
          setSeatConfirmed(true); // Mark seat as confirmed
        } else {
          setError('Failed to confirm seat');
        }
      } catch (err) {
        setError('Error confirming seat');
      }
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

          {/* Show Confirm Seat Button if Document is Approved */}
          {studentData.documentVerificationStatus.toLowerCase() === 'approved' && (
            <>
              {/* Button to Confirm Seat */}
              {!seatConfirmed && (
                <button
                  onClick={confirmSeat}
                  className="mt-4 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                >
                  Confirm Seat
                </button>
              )}

              {/* Success message after confirming seat */}
              {seatConfirmed && (
                <p className="mt-2 text-green-600">Seat confirmed successfully!</p>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
