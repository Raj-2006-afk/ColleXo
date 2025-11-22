import { Routes, Route, Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

import LandingPage from "../pages/LandingPage";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";

import StudentDashboard from "../pages/student/StudentDashboard";
import SocietyListPage from "../pages/student/SocietyListPage";
import MyApplicationsPage from "../pages/student/MyApplicationsPage";

import SHDashboard from "../pages/societyHead/SHDashboard";
import SHSocietyPage from "../pages/societyHead/SHSocietyPage";
import SHFormsPage from "../pages/societyHead/SHFormsPage";
import SHApplicationsPage from "../pages/societyHead/SHApplicationsPage";

import AdminDashboard from "../pages/admin/AdminDashboard";
import AdminSocietiesPage from "../pages/admin/AdminSocietiesPage";
import AdminUsersPage from "../pages/admin/AdminUsersPage";

const ProtectedRoute = ({ children, allowedRoles }) => {
	const { user, loading } = useAuth();

	if (loading) {
		return (
			<div className="flex items-center justify-center min-h-screen">
				<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
			</div>
		);
	}

	if (!user) {
		return <Navigate to="/login" replace />;
	}

	if (allowedRoles && !allowedRoles.includes(user.user_role)) {
		return <Navigate to="/" replace />;
	}

	return children;
};

const AppRouter = () => {
	const { user } = useAuth();

	const getDefaultRoute = () => {
		if (!user) return "/";

		switch (user.user_role) {
			case "admin":
				return "/admin/dashboard";
			case "societyHead":
				return "/society-head/dashboard";
			case "student":
				return "/student/dashboard";
			default:
				return "/";
		}
	};

	return (
		<Routes>
			<Route path="/" element={<LandingPage />} />
			<Route path="/login" element={<LoginPage />} />
			<Route path="/register" element={<RegisterPage />} />

			<Route
				path="/student/dashboard"
				element={
					<ProtectedRoute allowedRoles={["student"]}>
						<StudentDashboard />
					</ProtectedRoute>
				}
			/>
			<Route
				path="/student/societies"
				element={
					<ProtectedRoute allowedRoles={["student"]}>
						<SocietyListPage />
					</ProtectedRoute>
				}
			/>
			<Route
				path="/student/applications"
				element={
					<ProtectedRoute allowedRoles={["student"]}>
						<MyApplicationsPage />
					</ProtectedRoute>
				}
			/>

			<Route
				path="/society-head/dashboard"
				element={
					<ProtectedRoute allowedRoles={["societyHead"]}>
						<SHDashboard />
					</ProtectedRoute>
				}
			/>
			<Route
				path="/society-head/society"
				element={
					<ProtectedRoute allowedRoles={["societyHead"]}>
						<SHSocietyPage />
					</ProtectedRoute>
				}
			/>
			<Route
				path="/society-head/forms"
				element={
					<ProtectedRoute allowedRoles={["societyHead"]}>
						<SHFormsPage />
					</ProtectedRoute>
				}
			/>
			<Route
				path="/society-head/applications"
				element={
					<ProtectedRoute allowedRoles={["societyHead"]}>
						<SHApplicationsPage />
					</ProtectedRoute>
				}
			/>

			<Route
				path="/admin/dashboard"
				element={
					<ProtectedRoute allowedRoles={["admin"]}>
						<AdminDashboard />
					</ProtectedRoute>
				}
			/>
			<Route
				path="/admin/societies"
				element={
					<ProtectedRoute allowedRoles={["admin"]}>
						<AdminSocietiesPage />
					</ProtectedRoute>
				}
			/>
			<Route
				path="/admin/users"
				element={
					<ProtectedRoute allowedRoles={["admin"]}>
						<AdminUsersPage />
					</ProtectedRoute>
				}
			/>

			<Route path="*" element={<Navigate to={getDefaultRoute()} replace />} />
		</Routes>
	);
};

export default AppRouter;
