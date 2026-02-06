import { useEffect, useState } from 'react';
import { employeeAPI, attendanceAPI } from '../services/api';
import type { Employee, Attendance, AttendanceCreate, AttendanceStatus } from '../types';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

export default function AttendancePage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [attendance, setAttendance] = useState<Attendance[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [filterDate, setFilterDate] = useState('');
  const [formData, setFormData] = useState<AttendanceCreate>({
    employee_id: 0,
    date: new Date().toISOString().split('T')[0],
    status: 'Present' as AttendanceStatus,
  });
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [employeesData, attendanceData] = await Promise.all([
        employeeAPI.getAll(),
        attendanceAPI.getAll(),
      ]);
      setEmployees(employeesData);
      setAttendance(attendanceData);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setSubmitting(true);

    try {
      await attendanceAPI.create(formData);
      setFormData({
        employee_id: 0,
        date: new Date().toISOString().split('T')[0],
        status: 'Present' as AttendanceStatus,
      });
      setShowForm(false);
      fetchData();
    } catch (err: any) {
      setFormError(err.response?.data?.detail || 'Failed to mark attendance');
    } finally {
      setSubmitting(false);
    }
  };

  const getEmployeeName = (employeeId: number) => {
    const employee = employees.find((e) => e.id === employeeId);
    return employee ? employee.full_name : 'Unknown';
  };

  const filteredAttendance = filterDate
    ? attendance.filter((a) => a.date === filterDate)
    : attendance;

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} onRetry={fetchData} />;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Attendance</h2>
          <p className="mt-1 text-sm text-gray-500">Track daily attendance records</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary"
          disabled={employees.length === 0}
        >
          {showForm ? 'Cancel' : '+ Mark Attendance'}
        </button>
      </div>

      {employees.length === 0 ? (
        <div className="card">
          <EmptyState
            title="No employees available"
            message="Please add employees before marking attendance"
            action={{ label: 'Go to Employees', onClick: () => window.location.href = '/employees' }}
          />
        </div>
      ) : (
        <>
          {showForm && (
            <div className="card mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Mark Attendance</h3>
              {formError && (
                <div className="mb-4">
                  <ErrorMessage message={formError} />
                </div>
              )}
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                  <div>
                    <label htmlFor="employee" className="block text-sm font-medium text-gray-700 mb-1">
                      Employee *
                    </label>
                    <select
                      id="employee"
                      required
                      value={formData.employee_id}
                      onChange={(e) => setFormData({ ...formData, employee_id: Number(e.target.value) })}
                      className="input-field"
                    >
                      <option value="">Select Employee</option>
                      {employees.map((emp) => (
                        <option key={emp.id} value={emp.id}>
                          {emp.full_name} ({emp.employee_id})
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-1">
                      Date *
                    </label>
                    <input
                      type="date"
                      id="date"
                      required
                      value={formData.date}
                      onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                      className="input-field"
                    />
                  </div>
                  <div>
                    <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
                      Status *
                    </label>
                    <select
                      id="status"
                      required
                      value={formData.status}
                      onChange={(e) => setFormData({ ...formData, status: e.target.value as AttendanceStatus })}
                      className="input-field"
                    >
                      <option value="Present">Present</option>
                      <option value="Absent">Absent</option>
                    </select>
                  </div>
                </div>
                <div className="flex space-x-3">
                  <button
                    type="submit"
                    disabled={submitting}
                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {submitting ? 'Saving...' : 'Mark Attendance'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowForm(false);
                      setFormError(null);
                    }}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          <div className="card mb-6">
            <div className="flex items-center space-x-4">
              <label htmlFor="filterDate" className="text-sm font-medium text-gray-700">
                Filter by Date:
              </label>
              <input
                type="date"
                id="filterDate"
                value={filterDate}
                onChange={(e) => setFilterDate(e.target.value)}
                className="input-field max-w-xs"
              />
              {filterDate && (
                <button
                  onClick={() => setFilterDate('')}
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  Clear Filter
                </button>
              )}
            </div>
          </div>

          {filteredAttendance.length === 0 ? (
            <div className="card">
              <EmptyState
                title="No attendance records"
                message={filterDate ? 'No records found for selected date' : 'Get started by marking attendance'}
                action={!filterDate ? { label: 'Mark Attendance', onClick: () => setShowForm(true) } : undefined}
              />
            </div>
          ) : (
            <div className="card overflow-hidden">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Employee
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {filteredAttendance.map((record) => (
                      <tr key={record.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {new Date(record.date).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                          })}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {getEmployeeName(record.employee_id)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span
                            className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              record.status === 'Present'
                                ? 'bg-green-100 text-green-800'
                                : 'bg-red-100 text-red-800'
                            }`}
                          >
                            {record.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
