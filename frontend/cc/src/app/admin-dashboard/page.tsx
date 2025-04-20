'use client';

import { useState } from 'react';

export default function AdminDashboard() {
  const [departmentsData, setDepartmentsData] = useState([]);
  const [studentApplications, setStudentApplications] = useState([]);
  const itemsToShow = 5;

  // Fetch seat information (triggered by button click)
  const fetchSeatInformation = async () => {
    const response = await fetch('http://127.0.0.1:8000/api/seatInfo', {
      method: 'GET',
    });

    const data = await response.json();
    setDepartmentsData(data);
  };

  // Fetch student applications (triggered by button click)
  const fetchStudentApplications = async () => {
    const response = await fetch('http://127.0.0.1:8000/api/studentApplications', {
      method: 'GET',
    });

    const data = await response.json();
    // Add a status field with the value 'unverified' for all students
    const applicationsWithStatus = data.applications.slice(0, itemsToShow).map((student) => ({
      ...student,
      status: 'unverified', // Add default status
    }));
    setStudentApplications(applicationsWithStatus);
  };

  // Function to handle document verification
  const verifyDocuments = async (applicationId) => {
    const response = await fetch(`http://127.0.0.1:8000/api/studentApplications/${applicationId}/verify`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status: 'verified' }), // Update status to 'verified'
    });

    if (response.ok) {
      // Update the local state to reflect the change
      setStudentApplications((prevApplications) =>
        prevApplications.map((student) =>
          student.id === applicationId ? { ...student, status: 'verified' } : student
        )
      );
    }
  };

  return (
    <main className="p-8 space-y-10">
      <h1 className="text-3xl font-bold text-center">Admin Dashboard</h1>

      {/* Seat Information Section */}
      <div className="border-2 border-gray-300 rounded-xl p-6 mb-10 bg-white shadow-md max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold text-blue-700">Seat Information</h2>
          <button
            onClick={fetchSeatInformation}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Fetch Seat Information
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {departmentsData.length > 0 ? (
            departmentsData.map((dept) => (
              <div
                key={dept.course_name}
                className="border rounded-xl shadow-md p-6 bg-gray-50 hover:shadow-lg transition-all"
              >
                <h3 className="text-xl font-semibold text-blue-600 mb-4">{dept.course_name}</h3>
                <p><strong>Total Seats:</strong> {dept.total_seats}</p>
                <p><strong>Seats Available:</strong> {dept.available_seats}</p>
              </div>
            ))
          ) : (
            <div className="text-gray-500 col-span-full text-center">No seat info loaded yet.</div>
          )}
        </div>
      </div>

      {/* Student Applications Section */}
      <div className="border-2 border-gray-300 rounded-xl p-6 max-w-4xl mx-auto bg-white shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-center text-blue-700">Student Applications</h2>
          <button
            onClick={fetchStudentApplications}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Fetch Student Applications
          </button>
        </div>

        <div className="space-y-4">
          {studentApplications.map((student, index) => (
            <div key={index} className="flex justify-between items-center p-4 border rounded-lg bg-gray-100 shadow-sm">
              <div>
                <p><strong>Application ID:</strong> {student.id}</p>
                <p><strong>Exam Type:</strong> {student.exam}</p>
                <p><strong>Status:</strong> {student.status}</p> {/* Display status */}
              </div>
              <button
                onClick={() => verifyDocuments(student.id)}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Verify Documents
              </button>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
